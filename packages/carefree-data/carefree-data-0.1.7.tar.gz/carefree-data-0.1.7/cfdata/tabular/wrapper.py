import os
import copy
import logging

import numpy as np

from typing import *
from cftool.misc import timing_context, SavingMixin

from .misc import *
from .recognizer import *
from .converters import *
from .processors import *
from ..base import DataBase
from ..types import np_int_type


class TabularSplit(NamedTuple):
    split: "TabularData"
    remained: "TabularData"
    split_indices: np.ndarray
    remained_indices: np.ndarray


# TODO : Add outlier detection
class TabularData(DataBase):
    def __init__(self,
                 *,
                 task_type: TaskTypes = TaskTypes.NONE,
                 time_series_config: TimeSeriesConfig = None,
                 label_name: str = None,
                 string_label: Union[bool, None] = None,
                 numerical_label: Union[bool, None] = None,
                 categorical_label: Union[bool, None] = None,
                 column_names: Dict[int, str] = None,
                 valid_columns: List[int] = None,
                 string_columns: List[int] = None,
                 numerical_columns: List[int] = None,
                 categorical_columns: List[int] = None,
                 process_methods: Union[str, None, Dict[int, str]] = "auto",
                 default_numerical_process: str = "normalize",
                 default_categorical_process: str = "one_hot",
                 label_process_method: str = None,
                 numerical_threshold: float = None,
                 trigger_logging: bool = False,
                 verbose_level: int = 1):
        if task_type.is_clf:
            if numerical_label:
                raise ValueError("numerical labels are invalid in CLASSIFICATION tasks")
        elif task_type.is_reg:
            if string_label:
                raise ValueError("string labels are invalid in REGRESSION tasks")
            if categorical_label:
                raise ValueError("categorical labels are invalid in REGRESSION tasks")
        self._task_type = task_type
        self._time_series_config = time_series_config
        self.label_name = label_name
        self.string_label = string_label
        self.numerical_label = numerical_label
        self.categorical_label = categorical_label
        self._column_names = column_names
        self._valid_columns = valid_columns
        self._string_columns = string_columns
        self._numerical_columns = numerical_columns
        self._categorical_columns = categorical_columns
        self._process_methods = process_methods
        self._default_numerical_process = default_numerical_process
        self._default_categorical_process = default_categorical_process
        self._label_process_method = label_process_method
        self._numerical_threshold = numerical_threshold
        self._is_file = self._is_arr = False
        self._num_classes = None
        self._label_idx = self._has_column_names = None
        self._delim = self._quote_char = None
        self._raw = self._converted = self._processed = None
        self._recognizers = self._converters = self._processors = None
        self._verbose_level = verbose_level
        self._init_logging(verbose_level, trigger=trigger_logging)
        self.excludes = set()

    def __len__(self):
        return len(self._processed.x)

    def __getitem__(self, indices: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        x, y = self.processed.xy
        y_batch = None if y is None else y[indices]
        return x[indices], y_batch

    def __eq__(self, other: "TabularData"):
        if self.raw != other.raw:
            return False
        if self.converted != other.converted:
            return False
        return self.processed == other.processed

    @property
    def ts_config(self) -> Union[TimeSeriesConfig, None]:
        if self._time_series_config is None:
            return
        id_name = self._time_series_config.id_column_name
        time_name = self._time_series_config.time_column_name
        id_idx = self._time_series_config.id_column_idx
        time_idx = self._time_series_config.time_column_idx
        if id_idx is None:
            if id_name is None:
                raise ValueError("either `id_column_name` or `id_column` should be provided")
            for k, v in self.column_names.items():
                if v == id_name:
                    id_idx = k
                    break
        if time_idx is None:
            if time_name is None:
                raise ValueError("either `time_column_name` or `time_column` should be provided")
            for k, v in self.column_names.items():
                if v == time_name:
                    time_idx = k
                    break
        id_column = self.raw.xT[id_idx]
        time_column = self.raw.xT[time_idx]
        return TimeSeriesConfig(id_name, time_name, id_idx, time_idx, id_column, time_column)

    @property
    def cache_excludes(self):
        return {"_recognizers", "_converters", "_processors"}

    @property
    def data_tuple_base(self) -> Type[NamedTuple]:
        return DataTuple

    @property
    def data_tuple_attributes(self) -> List[str]:
        return ["_raw", "_converted", "_processed"]

    @property
    def raw(self) -> DataTuple:
        return self._raw

    @property
    def converted(self) -> DataTuple:
        return self._converted

    @property
    def processed(self) -> DataTuple:
        return self._processed

    @property
    def recognizers(self) -> Dict[int, Recognizer]:
        return self._recognizers

    @property
    def converters(self) -> Dict[int, Converter]:
        return self._converters

    @property
    def processors(self) -> Dict[int, Processor]:
        return self._processors

    @property
    def raw_dim(self) -> int:
        return len(self._raw.x[0])

    @property
    def processed_dim(self) -> int:
        return self._processed.x.shape[1]

    @property
    def task_type(self) -> TaskTypes:
        if not self._task_type.is_none:
            return self._task_type
        if self._recognizers[-1] is None:
            return TaskTypes.NONE
        self._task_type = TaskTypes.from_column_type(
            self._recognizers[-1].info.column_type,
            is_time_series=self.is_ts,
        )
        return self._task_type

    @property
    def column_names(self) -> Dict[int, str]:
        if self._column_names is None:
            self._column_names = {}
        for i in range(self.raw_dim):
            self._column_names.setdefault(i, str(i))
        return self._column_names

    def _get_prior_dict(self, attr: str, ts_value: Union[bool, None]) -> Dict[int, Union[bool, None]]:
        prior_dict_attr = f"{attr}_dict"
        prior_dict = getattr(self, prior_dict_attr, None)
        if prior_dict is None:
            prior_columns = getattr(self, attr, None)
            prior_dict = {
                i: None if prior_columns is None else i in prior_columns
                for i in range(self.raw_dim)
            }
            setattr(self, prior_dict_attr, prior_dict)
        ts_config = self.ts_config
        if ts_config is not None:
            prior_dict[ts_config.id_column_idx] = ts_value
            prior_dict[ts_config.time_column_idx] = ts_value
        return prior_dict

    @property
    def prior_valid_columns(self) -> Dict[int, Union[bool, None]]:
        return self._get_prior_dict("_valid_columns", True)

    @property
    def prior_string_columns(self) -> Dict[int, Union[bool, None]]:
        return self._get_prior_dict("_string_columns", None)

    @property
    def prior_numerical_columns(self) -> Dict[int, Union[bool, None]]:
        return self._get_prior_dict("_numerical_columns", False)

    @property
    def prior_categorical_columns(self) -> Dict[int, Union[bool, None]]:
        return self._get_prior_dict("_categorical_columns", None)

    @property
    def is_clf(self) -> bool:
        return self.task_type.is_clf

    @property
    def is_reg(self) -> bool:
        return self.task_type.is_reg

    @property
    def is_ts(self) -> bool:
        return self.ts_config is not None

    @property
    def is_file(self) -> bool:
        return self._is_file

    @property
    def splitter(self) -> DataSplitter:
        splitter = DataSplitter(time_series_config=self.ts_config, shuffle=False)
        return splitter.fit(self.to_dataset())

    @property
    def ts_indices(self) -> Set[int]:
        ts_config = self.ts_config
        return set() if ts_config is None else {ts_config.id_column_idx, ts_config.time_column_idx}

    @property
    def num_classes(self) -> int:
        if self.is_reg:
            return 0
        if self._num_classes is None:
            self._num_classes = self._processed.y.max().item() + 1
        return self._num_classes

    # Core

    @staticmethod
    def _flatten(data: data_type) -> data_type:
        if isinstance(data, np.ndarray):
            return data.ravel()
        flattened = []
        for elem in data:
            flattened.extend(elem)
        return flattened

    def _get_ts_sorting_indices(self):
        self.ts_sorting_indices = np.hstack(self.splitter._time_indices_list_in_use)[::-1].copy()

    def _core_fit(self) -> "TabularData":
        ts_indices = self.ts_indices
        with timing_context(self, "convert"):
            # convert features
            features = self._raw.xT
            converted_features = []
            self._recognizers, self._converters = {}, {}
            for i, flat_arr in enumerate(features):
                column_name = self.column_names[i]
                is_valid = self.prior_valid_columns[i]
                is_string = self.prior_string_columns[i]
                is_numerical = self.prior_numerical_columns[i]
                is_categorical = self.prior_categorical_columns[i]
                if i == self.raw_dim - 1 == len(self.excludes):
                    if i > 0:
                        self.log_msg(
                            f"last column {column_name} is forced to be valid "
                            "because previous columns are all excluded", self.warning_prefix,
                            verbose_level=2, msg_level=logging.WARNING
                        )
                    is_valid = True
                kwargs = {
                    "is_valid": is_valid,
                    "is_string": is_string,
                    "is_numerical": is_numerical,
                    "is_categorical": is_categorical,
                }
                if self._numerical_threshold is not None:
                    kwargs["numerical_threshold"] = self._numerical_threshold
                with timing_context(self, "fit recognizer"):
                    recognizer = self._recognizers[i] = Recognizer(column_name, **kwargs).fit(flat_arr)
                if not recognizer.info.is_valid:
                    self.log_msg(recognizer.info.msg, self.warning_prefix, 2, logging.WARNING)
                    self.excludes.add(i)
                    continue
                if i not in ts_indices:
                    with timing_context(self, "fit converter"):
                        converter = self._converters[i] = Converter.make_with(recognizer)
                    converted_features.append(converter.converted_input)
            # convert labels
            if self._raw.y is None:
                converted_labels = self._recognizers[-1] = self._converters[-1] = None
            else:
                with timing_context(self, "fit recognizer"):
                    recognizer = self._recognizers[-1] = Recognizer(
                        self.label_name,
                        is_label=True,
                        task_type=self._task_type,
                        is_valid=True,
                        is_string=self.string_label,
                        is_numerical=self.numerical_label,
                        is_categorical=self.categorical_label,
                        numerical_threshold=1.
                    ).fit(self._flatten(self._raw.y))
                with timing_context(self, "fit converter"):
                    converter = self._converters[-1] = Converter.make_with(recognizer)
                converted_labels = converter.converted_input.reshape([-1, 1])
        converted_x = np.vstack(converted_features).T
        with timing_context(self, "process"):
            # process features
            self._processors = {}
            processed_features = []
            previous_processors = []
            idx = 0
            while idx < self.raw_dim:
                if idx in self.excludes or idx in ts_indices:
                    idx += 1
                    continue
                column_type = self._converters[idx].info.column_type
                if self._process_methods is None:
                    method = None
                elif isinstance(self._process_methods, str):
                    method = self._process_methods
                else:
                    method = self._process_methods.get(idx, "auto")
                if method is None:
                    method = "identical"
                elif method == "auto":
                    if idx in ts_indices:
                        method = "identical"
                    elif column_type is ColumnTypes.NUMERICAL:
                        method = self._default_numerical_process
                    else:
                        method = self._default_categorical_process
                processor = self._processors[idx] = processor_dict[method](previous_processors.copy())
                previous_processors.append(processor)
                columns = converted_x[..., processor.input_indices]
                with timing_context(self, "fit processor"):
                    processor.fit(columns)
                with timing_context(self, "process with processor"):
                    processed_features.append(processor.process(columns))
                idx += processor.input_dim
            # process labels
            if converted_labels is None:
                processed_labels = self._processors[-1] = None
            else:
                column_type = self._converters[-1].info.column_type
                method = None
                if self._label_process_method is not None:
                    method = self._label_process_method
                if method is None:
                    method = "normalize" if column_type is ColumnTypes.NUMERICAL else "identical"
                with timing_context(self, "fit processor"):
                    processor = self._processors[-1] = processor_dict[method]([]).fit(converted_labels)
                with timing_context(self, "process with processor"):
                    processed_labels = processor.process(converted_labels)
        if self.task_type.is_clf and converted_labels is not None:
            converted_labels = converted_labels.astype(np_int_type)
            processed_labels = processed_labels.astype(np_int_type)
        self._converted = DataTuple(converted_x, converted_labels)
        self._processed = DataTuple(np.hstack(processed_features), processed_labels)
        self._valid_columns = [col for col in range(self.raw_dim) if col not in self.excludes]
        self._valid_columns_dict = self.ts_sorting_indices = None
        if self.is_ts:
            self._get_ts_sorting_indices()
        return self

    def _read_from_file(self,
                        file_path: str,
                        *,
                        label_idx: int = None,
                        contains_labels: bool = True,
                        has_column_names: bool = None,
                        quote_char: str = None,
                        delim: str = None) -> "TabularData":
        self._is_file = True
        self._label_idx, self._has_column_names = label_idx, has_column_names
        self._delim, self._quote_char = delim, quote_char
        with timing_context(self, "read_file"):
            x, y = self.read_file(file_path, contains_labels=contains_labels)
        self._raw = DataTuple.with_transpose(x, y)
        return self._core_fit()

    def _read_from_arr(self,
                       x: data_type,
                       y: data_type) -> "TabularData":
        self._is_arr = True
        self._raw = DataTuple.with_transpose(x, y)
        return self._core_fit()

    def _transform_labels(self,
                          raw: DataTuple) -> Tuple[np.ndarray, np.ndarray]:
        if raw.y is None:
            converted_labels = transformed_labels = None
        else:
            converted_labels = self._converters[-1].convert(self._flatten(raw.y))
            transformed_labels = self._processors[-1].process(converted_labels.reshape([-1, 1]))
        if self.task_type.is_clf:
            if converted_labels is not None:
                converted_labels = converted_labels.astype(np_int_type)
                transformed_labels = transformed_labels.astype(np_int_type)
        return converted_labels, transformed_labels

    def _transform(self,
                   raw: DataTuple,
                   return_converted: bool) -> Union[DataTuple, Tuple[DataTuple, DataTuple]]:
        # transform features
        features = raw.xT
        ts_indices = self.ts_indices
        converted_features = np.vstack([
            self._converters[i].convert(flat_arr)
            for i, flat_arr in enumerate(features)
            if i not in self.excludes and i not in ts_indices
        ])
        idx = 0
        processed = []
        while idx < self.raw_dim:
            if idx in self.excludes or idx in ts_indices:
                idx += 1
                continue
            processor = self._processors[idx]
            input_indices = processor.input_indices
            columns = processor.process(converted_features[input_indices].T)
            processed.append(columns)
            idx += processor.input_dim
        transformed_features = np.hstack(processed)
        # transform labels
        converted_labels, transformed_labels = self._transform_labels(raw)
        # aggregate
        transformed = DataTuple(transformed_features, transformed_labels)
        if not return_converted:
            return transformed
        converted = DataTuple(converted_features.T, converted_labels)
        return converted, transformed

    def _get_raw(self,
                 x: Union[str, data_type],
                 y: data_type = None,
                 *,
                 contains_labels: bool = True) -> DataTuple:
        if self._is_file:
            if isinstance(x, str):
                if y is not None:
                    raise ValueError(f"x refers to file_path but y is still provided ({y}), which is illegal")
                x, y = self.read_file(x, contains_labels=contains_labels)
        return DataTuple.with_transpose(x, y)

    # API

    def read_file(self,
                  file_path: str,
                  *,
                  contains_labels: bool = True) -> Tuple[raw_data_type, raw_data_type]:
        ext = os.path.splitext(file_path)[1][1:]
        set_default = lambda n, default: n if n is not None else default
        if ext == "txt":
            has_column_names, delim, quote_char = map(
                set_default,
                [self._has_column_names, self._delim, self._quote_char],
                [False, " ", None]
            )
        elif ext == "csv":
            has_column_names, delim, quote_char = map(
                set_default,
                [self._has_column_names, self._delim, self._quote_char],
                [True, ",", '"']
            )
        else:
            raise NotImplementedError(f"file type '{ext}' not recognized")
        self._delim, self._quote_char = delim, quote_char
        with open(file_path, "r") as f:
            first_row = None
            if has_column_names:
                first_row = column_names = f.readline().strip().split(delim)
                self._column_names = {i: name for i, name in enumerate(column_names)}
            data = []
            for line in f:
                line = ["nan" if not elem else elem for elem in line.strip().split(delim)]
                if quote_char is not None:
                    startswith_quote = [elem.startswith(quote_char) for elem in line]
                    endswith_quote = [elem.endswith(quote_char) for elem in line]
                    merge_start, merge_intervals = None, []
                    for i, (startswith, endswith) in enumerate(zip(startswith_quote, endswith_quote)):
                        if startswith and not endswith:
                            merge_start = i
                            continue
                        if endswith and not startswith and merge_start is not None:
                            merge_intervals.append((merge_start, i + 1))
                            merge_start = None
                            continue
                    idx, new_line = 0, []
                    for start, end in merge_intervals:
                        if start > idx:
                            new_line += line[idx:start]
                        new_line.append(delim.join(line[start:end]))
                        idx = end
                    if idx < len(line):
                        new_line += line[idx:len(line)]
                    line = new_line
                if first_row is None:
                    first_row = line
                else:
                    assert len(first_row) == len(line), "num_features are not identical"
                data.append(line)
        if not contains_labels:
            if self._raw is not None and len(data[0]) == len(self._raw.x[0]) + 1:
                raise ValueError("file contains labels but 'contains_labels=False' passed in")
            return data, None

        if self._column_names is None or self.label_name is None:
            if self._label_idx is None:
                self._label_idx = -1
        else:
            reverse_column_names = dict(map(reversed, self._column_names.items()))
            self._label_idx = reverse_column_names.get(self.label_name)
            if self._label_idx is None:
                raise ValueError(
                    f"'{self.label_name}' is not included in column names "
                    f"({[self._column_names[i] for i in range(len(self._column_names))]})"
                )
        if self._label_idx < 0:
            self._label_idx = len(data[0]) + self._label_idx
        x = [line[:self._label_idx] + line[self._label_idx+1:] for line in data]
        y = [line[self._label_idx:self._label_idx+1] for line in data]
        return x, y

    def read(self,
             x: Union[str, data_type],
             y: Union[int, data_type] = None,
             *,
             contains_labels: bool = True,
             **kwargs) -> "TabularData":
        if isinstance(x, str):
            self._read_from_file(x, label_idx=y, contains_labels=contains_labels, **kwargs)
        else:
            if isinstance(y, int):
                y = None
            self._read_from_arr(x, y)
        self.log_timing()
        return self

    def split(self,
              n: Union[int, float],
              *,
              order: str = "auto") -> TabularSplit:
        if order == "auto":
            split = self.splitter.split(n)
            split_indices = split.corresponding_indices
            remained_indices = split.remaining_indices
        else:
            if order not in {"bottom_up", "top_down"}:
                raise NotImplementedError(f"`order` should be either 'bottom_up' or 'top_down', {order} found")
            base_indices = np.arange(self._raw.x.shape[0])
            if order == "bottom_up":
                split_indices, remained_indices = base_indices[-n:], base_indices[:-n]
            else:
                split_indices, remained_indices = base_indices[:n], base_indices[n:]
        raw, converted, processed = self._raw, self._converted, self._processed
        p1, p2 = map(copy.copy, [self] * 2)
        p1._raw, p1._converted, p1._processed = map(
            DataTuple.split_with,
            [raw, converted, processed], [split_indices] * 3
        )
        p2._raw, p2._converted, p2._processed = map(
            DataTuple.split_with,
            [raw, converted, processed], [remained_indices] * 3
        )
        p1.ts_sorting_indices = np.arange(len(p1))
        p2.ts_sorting_indices = np.arange(len(p2))
        return TabularSplit(p1, p2, split_indices, remained_indices)

    def copy_to(self,
                x: Union[str, data_type],
                y: data_type = None,
                *,
                contains_labels: bool = True) -> "TabularData":
        copied = copy.copy(self)
        raw = copied._raw = self._get_raw(x, y, contains_labels=contains_labels)
        copied._converted, copied._processed = self._transform(raw, True)
        if copied.is_ts:
            copied._get_ts_sorting_indices()
        return copied

    def transform(self,
                  x: Union[str, data_type],
                  y: data_type = None,
                  *,
                  contains_labels: bool = True,
                  return_converted: bool = False) -> Union[DataTuple, Tuple[DataTuple, DataTuple]]:
        raw = self._get_raw(x, y, contains_labels=contains_labels)
        return self._transform(raw, return_converted)

    def transform_labels(self,
                         y: data_type,
                         *,
                         return_converted: bool = False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        raw = DataTuple(None, y)
        converted_labels, transformed_labels = self._transform_labels(raw)
        if not return_converted:
            return transformed_labels
        return converted_labels, transformed_labels

    def recover_labels(self,
                       y: np.ndarray,
                       *,
                       inplace: bool = False) -> np.ndarray:
        process_recovered = self._processors[-1].recover(y, inplace=inplace)
        convert_recovered = self.converters[-1].recover(process_recovered.ravel(), inplace=inplace)
        return convert_recovered.reshape([-1, 1])

    @classmethod
    def load(cls,
             folder: str,
             *,
             compress: bool = True,
             verbose_level: int = 0) -> "TabularData":
        data = cls(verbose_level=verbose_level)
        SavingMixin.load(data, folder, compress=compress)
        is_file, is_arr = data._is_file, data._is_arr
        data.read(*data._raw[:2])
        data._is_file, data._is_arr = is_file, is_arr
        return data

    def to_dataset(self) -> TabularDataset:
        return TabularDataset(*self.processed.xy, task_type=self.task_type)

    @classmethod
    def from_dataset(cls,
                     dataset: TabularDataset,
                     **kwargs) -> "TabularData":
        task_type = kwargs.pop("task_type", dataset.task_type)
        return cls(task_type=task_type, **kwargs).read(*dataset.xy)

    @classmethod
    def simple(cls,
               task_type: TaskTypes,
               **kwargs) -> "TabularData":
        return cls(
            default_numerical_process="identical",
            default_categorical_process="identical",
            task_type=task_type, verbose_level=0,
            **kwargs
        )


__all__ = ["TabularData"]
