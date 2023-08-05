import numpy as np

from typing import *
from cftool.misc import *

from abc import *
from .misc import *
from ..types import *
from .wrapper import TabularData


class KFold:
    """
    Util class which can perform k-fold data splitting:

    1. X = {x1, x2, ..., xn} -> [X1, X2, ..., Xk]
    2. Xi ∩ Xj = ∅, ∀ i, j = 1,..., K
    3. X1 ∪ X2 ∪ ... ∪ Xk = X

    * Notice that `KFold` does not always hold the principles listed above, because `DataSplitter`
    will ensure that at least one sample of each class will be kept. In this case, when we apply
    `KFold` to an imbalance dataset, `KFold` may slightly violate principle 2. and 3.

    Parameters
    ----------
    k : int, number of folds
    dataset : TabularDataset, dataset which we want to split
    **kwargs : used to initialize `DataSplitter` instance

    Examples
    ----------
    >>> import numpy as np
    >>>
    >>> from cfdata.types import np_int_type
    >>> from cfdata.tabular.misc import TaskTypes
    >>> from cfdata.tabular.toolkit import KFold
    >>> from cfdata.tabular.wrapper import TabularDataset
    >>>
    >>> x = np.arange(12).reshape([6, 2])
    >>> # create an imbalance dataset
    >>> y = np.zeros(6, np_int_type)
    >>> y[[-1, -2]] = 1
    >>> dataset = TabularDataset.from_xy(x, y, TaskTypes.CLASSIFICATION)
    >>> k_fold = KFold(3, dataset)
    >>> for train_fold, test_fold in k_fold:
    >>>     print(np.vstack([train_fold.dataset.x, test_fold.dataset.x]))
    >>>     print(np.vstack([train_fold.dataset.y, test_fold.dataset.y]))

    """

    def __init__(self,
                 k: int,
                 dataset: TabularDataset,
                 **kwargs):
        if k <= 1:
            raise ValueError("k should be larger than 1 in KFold")
        ratio = 1. / k
        self.n_list = (k - 1) * [ratio]
        self.splitter = DataSplitter(**kwargs).fit(dataset)
        self.split_results = self._order = self._cursor = None

    def __iter__(self):
        self.split_results = self.splitter.split_multiple(self.n_list, return_remained=True)
        self._order = np.random.permutation(len(self.split_results)).tolist()
        self._cursor = 0
        return self

    def __next__(self) -> Tuple[SplitResult, SplitResult]:
        if self._cursor >= len(self._order):
            raise StopIteration
        train_results = self.split_results.copy()
        test_result = train_results.pop(self._order[self._cursor])
        train_result = SplitResult.concat(train_results)
        self._cursor += 1
        return train_result, test_result


class KRandom:
    """
    Util class which can perform k-random data splitting:

    1. X = {x1, x2, ..., xn} -> [X1, X2, ..., Xk]
    2. idx{X1} ≠ idx{X2} ≠ ... ≠ idx{Xk}, where idx{X} = {1, 2, ..., n}
    3. X1 = X2 = ... = Xk = X

    Parameters
    ----------
    k : int, number of folds
    num_test : {int, float}
    * if float and  < 1 : ratio of the test dataset
    * if int   and  > 1 : exact number of test samples
    dataset : TabularDataset, dataset which we want to split
    **kwargs : used to initialize `DataSplitter` instance

    Examples
    ----------
    >>> import numpy as np
    >>>
    >>> from cfdata.types import np_int_type
    >>> from cfdata.tabular.misc import TaskTypes
    >>> from cfdata.tabular.toolkit import KRandom
    >>> from cfdata.tabular.wrapper import TabularDataset
    >>>
    >>> x = np.arange(12).reshape([6, 2])
    >>> # create an imbalance dataset
    >>> y = np.zeros(6, np_int_type)
    >>> y[[-1, -2]] = 1
    >>> dataset = TabularDataset.from_xy(x, y, TaskTypes.CLASSIFICATION)
    >>> k_random = KRandom(3, 2, dataset)
    >>> for train_fold, test_fold in k_random:
    >>>     print(np.vstack([train_fold.dataset.x, test_fold.dataset.x]))
    >>>     print(np.vstack([train_fold.dataset.y, test_fold.dataset.y]))

    """

    def __init__(self,
                 k: int,
                 num_test: Union[int, float],
                 dataset: TabularDataset,
                 **kwargs):
        self._cursor = None
        self.k, self.num_test = k, num_test
        self.splitter = DataSplitter(**kwargs).fit(dataset)

    def __iter__(self):
        self._cursor = 0
        return self

    def __next__(self) -> Tuple[SplitResult, SplitResult]:
        if self._cursor >= self.k:
            raise StopIteration
        self._cursor += 1
        self.splitter.reset()
        test_result, train_result = self.splitter.split_multiple([self.num_test], return_remained=True)
        return train_result, test_result


class KBootstrap:
    """
    Util class which can perform k-random data splitting with bootstrap:

    1. X = {x1, x2, ..., xn} -> [X1, X2, ..., Xk] (Use bootstrap aggregation to collect datasets)
    3. idx{X1} ≠ idx{X2} ≠ ... ≠ idx{Xk}, where idx{X} = {1, 2, ..., n}
    4. X1 = X2 = ... = Xk = X

    * Notice that only some of the special algorithms (e.g. bagging) need `KBootstrap`.

    Parameters
    ----------
    k : int, number of folds
    num_test : {int, float}
    * if float and  < 1 : ratio of the test dataset
    * if int   and  > 1 : exact number of test samples
    dataset : TabularDataset, dataset which we want to split
    **kwargs : used to initialize `DataSplitter` instance

    Examples
    ----------
    >>> import numpy as np
    >>>
    >>> from cfdata.types import np_int_type
    >>> from cfdata.tabular.misc import TaskTypes
    >>> from cfdata.tabular.toolkit import KBootstrap
    >>> from cfdata.tabular.wrapper import TabularDataset
    >>>
    >>> x = np.arange(12).reshape([6, 2])
    >>> # create an imbalance dataset
    >>> y = np.zeros(6, np_int_type)
    >>> y[[-1, -2]] = 1
    >>> dataset = TabularDataset.from_xy(x, y, TaskTypes.CLASSIFICATION)
    >>> k_bootstrap = KBootstrap(3, 2, dataset)
    >>> for train_fold, test_fold in k_bootstrap:
    >>>     print(np.vstack([train_fold.dataset.x, test_fold.dataset.x]))
    >>>     print(np.vstack([train_fold.dataset.y, test_fold.dataset.y]))

    """

    def __init__(self,
                 k: int,
                 num_test: Union[int, float],
                 dataset: TabularDataset,
                 **kwargs):
        self._cursor = None
        self.dataset = dataset
        self.num_samples = len(dataset)
        if isinstance(num_test, float):
            num_test = int(round(num_test * self.num_samples))
        self.k, self.num_test = k, num_test
        self.splitter = DataSplitter(**kwargs).fit(dataset)

    def __iter__(self):
        self._cursor = 0
        return self

    def __next__(self) -> Tuple[SplitResult, SplitResult]:
        if self._cursor >= self.k:
            raise StopIteration
        self._cursor += 1
        self.splitter.reset()
        test_result, train_result = self.splitter.split_multiple([self.num_test], return_remained=True)
        tr_indices = train_result.corresponding_indices
        tr_indices = np.random.choice(tr_indices, len(tr_indices))
        tr_set = self.dataset.split_with(tr_indices)
        tr_split = SplitResult(tr_set, tr_indices, None)
        return tr_split, test_result


class ImbalancedSampler(LoggingMixin):
    """
    Util class which can sample imbalance dataset in a balanced way

    Parameters
    ----------
    data : TabularData, data which we want to sample from
    imbalance_threshold : float
    * for binary class cases, if n_pos / n_neg < threshold, we'll treat data as imbalance data
    * for multi  class cases, if n_min_class / n_max_class < threshold, we'll treat data as imbalance data
    shuffle : bool, whether shuffle the returned indices
    sample_method : str, sampling method used in `cftool.misc.Sampler`
    * currently only 'multinomial' is supported
    verbose_level : int, verbose level used in `LoggingMixin`

    Examples
    ----------
    >>> import numpy as np
    >>>
    >>> from cfdata.types import np_int_type
    >>> from cfdata.tabular import TabularData
    >>> from cfdata.tabular.toolkit import ImbalancedSampler
    >>> from cftool.misc import get_counter_from_arr
    >>>
    >>> n = 20
    >>> x = np.arange(2 * n).reshape([n, 2])
    >>> # create an imbalance dataset
    >>> y = np.zeros([n, 1], np_int_type)
    >>> y[-1] = [1]
    >>> data = TabularData().read(x, y)
    >>> sampler = ImbalancedSampler(data)
    >>> # Counter({1: 12, 0: 8})
    >>> # This may vary, but will be rather balanced
    >>> # You might notice that positive samples are even more than negative samples!
    >>> print(get_counter_from_arr(y[sampler.get_indices()]))

    """

    def __init__(self,
                 data: TabularData,
                 imbalance_threshold: float = 0.1,
                 *,
                 shuffle: bool = True,
                 aggregation: str = "continuous",
                 aggregation_config: Dict[str, Any] = None,
                 sample_method: str = "multinomial",
                 verbose_imbalance: bool = True,
                 verbose_level: int = 2):
        self.data = data
        self.shuffle = shuffle
        self.imbalance_threshold = imbalance_threshold
        self._sample_imbalance_flag = True
        self._aggregation_name = aggregation
        self._aggregation_config = aggregation_config
        if not data.is_ts:
            self.aggregation = None
            self._num_samples = len(data)
        else:
            if aggregation_config is None:
                aggregation_config = {}
            self.aggregation = aggregation_dict[aggregation](data, aggregation_config, data._verbose_level)
            self._num_samples = len(self.aggregation.indices2id)
        label_recognizer = data.recognizers[-1]
        if not self.shuffle or data.is_reg:
            label_counts = self._label_ratios = self._sampler = None
        else:
            label_counter = label_recognizer.counter
            transform_dict = label_recognizer.transform_dict
            label_counter = {transform_dict[k]: v for k, v in label_counter.items()}
            label_counts = np.array([label_counter[k] for k in sorted(label_counter)], np_float_type)
            self._label_ratios, max_label_count = label_counts / self._num_samples, label_counts.max()
            if label_counts.min() / max_label_count >= imbalance_threshold:
                self._sampler = None
            else:
                labels = data.processed.y.ravel()
                sample_weights = np.zeros(self._num_samples, np_float_type)
                for i, count in enumerate(label_counts):
                    sample_weights[labels == i] = max_label_count / count
                sample_weights /= sample_weights.sum()
                self._sampler = Sampler(sample_method, sample_weights)

        self._sample_method, self._verbose_level = sample_method, verbose_level
        if verbose_imbalance and self._sampler is not None:
            self.log_msg(
                f"using imbalanced sampler with label counts = {label_counts.tolist()}",
                self.info_prefix, 2
            )

    def __len__(self):
        return self._num_samples

    @property
    def is_imbalance(self) -> bool:
        return self._sampler is not None

    @property
    def sample_imbalance(self) -> bool:
        return self._sample_imbalance_flag

    @property
    def label_ratios(self) -> Union[None, np.ndarray]:
        return self._label_ratios

    def switch_imbalance_status(self, flag: bool) -> None:
        self._sample_imbalance_flag = flag

    def get_indices(self) -> np.ndarray:
        if not self.shuffle or not self._sample_imbalance_flag or not self.is_imbalance:
            indices = np.arange(self._num_samples).astype(np_int_type)
        else:
            indices = self._sampler.sample(self._num_samples)
        if self.shuffle:
            np.random.shuffle(indices)
        if self.aggregation is not None:
            indices = self.aggregation.aggregate(indices)
        return indices

    def copy(self) -> "ImbalancedSampler":
        aggregation_config = None
        if self._aggregation_config is not None:
            aggregation_config = shallow_copy_dict(self._aggregation_config)
        return ImbalancedSampler(
            self.data,
            self.imbalance_threshold,
            shuffle=self.shuffle,
            aggregation=self._aggregation_name,
            aggregation_config=aggregation_config,
            sample_method=self._sample_method,
            verbose_level=self._verbose_level,
            verbose_imbalance=False,
        )


class LabelCollators:
    @staticmethod
    def reg_default(y_batch):
        assert len(y_batch) == 2
        return y_batch[1] - y_batch[0]

    @staticmethod
    def clf_default(y_batch):
        assert len(y_batch) == 2
        return y_batch[1] == y_batch[0]


class DataLoader:
    """
    Util class which can generated batches from `ImbalancedSampler`

    Examples
    ----------
    >>> import numpy as np
    >>>
    >>> from cfdata.types import np_int_type
    >>> from cfdata.tabular import TabularData
    >>> from cfdata.tabular.toolkit import DataLoader, ImbalancedSampler
    >>> from cftool.misc import get_counter_from_arr
    >>>
    >>> n = 20
    >>> x = np.arange(2 * n).reshape([n, 2])
    >>> y = np.zeros([n, 1], np_int_type)
    >>> y[-1] = [1]
    >>> data = TabularData().read(x, y)
    >>> sampler = ImbalancedSampler(data)
    >>> loader = DataLoader(16, sampler)
    >>> y_batches = []
    >>> for x_batch, y_batch in loader:
    >>>     y_batches.append(y_batch)
    >>>     # (16, 1) (16, 1)
    >>>     # (4, 1) (4, 1)
    >>>     print(x_batch.shape, y_batch.shape)
    >>> # Counter({1: 11, 0: 9})
    >>> print(get_counter_from_arr(np.vstack(y_batches).ravel()))

    """

    def __init__(self,
                 batch_size: int,
                 sampler: ImbalancedSampler,
                 *,
                 num_siamese: int = 1,
                 return_indices: bool = False,
                 label_collator: callable = None,
                 verbose_level: int = 2):
        self._indices_in_use = None
        self._verbose_level = verbose_level
        self.data = sampler.data
        self.return_indices = return_indices
        if return_indices and num_siamese > 1:
            print(f"{LoggingMixin.warning_prefix}`return_indices` is set to False because siamese loader is used")
            self.return_indices = False
        self._num_siamese, self._label_collator = num_siamese, label_collator
        self._num_samples, self.sampler = len(sampler), sampler
        self.batch_size = min(self._num_samples, batch_size)
        self._verbose_level = verbose_level

    def __len__(self):
        n_iter = int(self._num_samples / self.batch_size)
        return n_iter + int(n_iter * self.batch_size < self._num_samples)

    def __iter__(self):
        self._reset()
        return self

    def __next__(self):
        data_next = self._get_next_batch()
        if self._num_siamese == 1:
            return data_next
        all_data = [data_next] if self._check_full_batch(data_next) else []
        while len(all_data) < self._num_siamese:
            data_next = self._get_next_batch()
            if self._check_full_batch(data_next):
                all_data.append(data_next)
        x_batch, y_batch = zip(*all_data)
        if self._label_collator is not None:
            y_batch = self._label_collator(y_batch)
        return x_batch, y_batch

    @property
    def enabled_sampling(self) -> bool:
        return self.sampler.sample_imbalance

    @enabled_sampling.setter
    def enabled_sampling(self, value: bool):
        self.sampler.switch_imbalance_status(value)

    def _reset(self):
        reset_caches = {
            "_indices_in_use": self.sampler.get_indices(),
            "_siamese_cursor": 0, "_cursor": -1
        }
        for attr, init_value in reset_caches.items():
            setattr(self, attr, init_value)

    def _get_next_batch(self):
        n_iter, self._cursor = len(self), self._cursor + 1
        if self._cursor == n_iter * self._num_siamese:
            raise StopIteration
        if self._num_siamese > 1:
            new_siamese_cursor = int(self._cursor / n_iter)
            if new_siamese_cursor > self._siamese_cursor:
                self._siamese_cursor = new_siamese_cursor
                self._indices_in_use = self.sampler.get_indices()
        start = (self._cursor - n_iter * self._siamese_cursor) * self.batch_size
        end = start + self.batch_size
        indices = self._indices_in_use[start:end]
        batch = self.data[indices]
        if not self.return_indices:
            return batch
        return batch, indices

    def _check_full_batch(self, batch):
        if len(batch[0]) == self.batch_size:
            return True
        return False

    def copy(self) -> "DataLoader":
        return DataLoader(
            self.batch_size,
            self.sampler.copy(),
            num_siamese=self._num_siamese,
            return_indices=self.return_indices,
            label_collator=self._label_collator,
            verbose_level=self._verbose_level,
        )


# time series

class TimeSeriesModifier:
    id_name = "id"
    time_name = "timestamp"
    label_name = "label"

    def __init__(self,
                 file_path: str,
                 task_type: TaskTypes,
                 *,
                 delim: str = None,
                 ts_config: TimeSeriesConfig = None,
                 contains_labels: bool = False):
        if not task_type.is_ts:
            raise ValueError("task_type should be either TIME_SERIES_CLF or TIME_SERIES_REG")
        self._file_path = file_path
        self._task_type = task_type
        self._ts_config = ts_config
        self._contains_labels = contains_labels
        self.data = TabularData.simple(task_type, time_series_config=ts_config)
        self.data.read(file_path, contains_labels=contains_labels)
        if delim is None:
            delim = self.data._delim
        self.delim = delim
        column_names = [self.data._column_names[i] for i in sorted(self.data._column_names)]
        self.header = None if column_names is None else self.delim.join(column_names)
        self._num_samples = len(self.data.raw.x)
        self.xt = self.data.raw.xT
        self._modified = False

    def pad_id(self) -> "TimeSeriesModifier":
        if self.header is not None:
            self.header = f"{self.id_name}{self.delim}{self.header}"
        self.xt.insert(0, ["0"] * self._num_samples)
        self._modified = True
        return self

    def pad_date(self) -> "TimeSeriesModifier":
        if self.header is not None:
            self.header = f"{self.time_name}{self.delim}{self.header}"
        self.xt.insert(0, list(map(str, range(self._num_samples))))
        self._modified = True
        return self

    def pad_id_and_date(self) -> "TimeSeriesModifier":
        self.pad_date().pad_id()
        return self

    def pad_labels(self,
                   fn: Callable[[np.ndarray], np.ndarray],
                   *,
                   offset: int,
                   batch_size: int = 32,
                   ts_config: TimeSeriesConfig = None,
                   aggregation_config: Dict[str, Any] = None,
                   aggregation: str = "continuous") -> "TimeSeriesModifier":
        if self._contains_labels:
            raise ValueError("labels already exist")
        if not self._modified:
            data = self.data
            if not data.is_ts:
                raise ValueError("time_series_config is not provided for the original data")
        else:
            column_names = None
            if self.header is not None:
                column_names = self.header.split(self.delim)
            if ts_config is None:
                raise ValueError("columns are modified but new time_series_config is not provided")
            data = TabularData.simple(
                self._task_type,
                time_series_config=ts_config,
                column_names={i: name for i, name in enumerate(column_names)},
            )
            data.read(transpose(self.xt), contains_labels=self._contains_labels)
        if aggregation_config is None:
            aggregation_config = {}
        aggregation_config["num_history"] = offset + 1
        sampler = ImbalancedSampler(
            data,
            shuffle=False,
            aggregation=aggregation,
            aggregation_config=aggregation_config,
        )
        labels = []
        for x_batch, _ in DataLoader(batch_size, sampler):
            labels.append(fn(x_batch))
        labels = np.vstack(labels).ravel()
        sorted_labels = np.zeros(len(data), np_float_type)
        sorted_labels[sampler.get_indices()[..., 0]] = labels
        self.header = f"{self.header}{self.delim}{self.label_name}"
        self.xt.append(sorted_labels.astype(np.str))
        return self

    def export_to(self,
                  export_path: str) -> "TimeSeriesModifier":
        with open(export_path, "w") as f:
            if self.header is not None:
                f.write(f"{self.header}\n")
            f.write("\n".join(self.delim.join(line) for line in transpose(self.xt)))
        return self


aggregation_dict: Dict[str, Type["AggregationBase"]] = {}


class AggregationBase(LoggingMixin, metaclass=ABCMeta):
    def __init__(self,
                 data: TabularData,
                 config: Dict[str, Any],
                 verbose_level: int):
        if not data.is_ts:
            raise ValueError("time series data is required")
        self.data = data
        self.config, self._verbose_level = config, verbose_level
        self._num_history = config.setdefault("num_history", 1)
        id_column = data.raw.xT[data.ts_config.id_column_idx]
        sorted_id_column = [id_column[i] for i in data.ts_sorting_indices]
        unique_indices = get_unique_indices(sorted_id_column)
        self._unique_id_arr, self._id2indices = unique_indices.unique, unique_indices.split_indices
        self._initialize()

    @property
    @abstractmethod
    def num_aggregation(self):
        pass

    @abstractmethod
    def _aggregate_core(self, indices: np.ndarray) -> np.ndarray:
        """ indices should be a column vector """

    def _initialize(self):
        self._num_samples_per_id = np.array(list(map(len, self._id2indices)), np_int_type)
        self.log_msg("generating valid aggregation info", self.info_prefix, 5)
        valid_mask = self._num_samples_per_id >= self._num_history
        if not valid_mask.any():
            raise ValueError(
                "current settings lead to empty valid dataset, increasing raw dataset size or "
                f"decreasing n_history (current: {self._num_history}) might help"
            )
        if not valid_mask.all():
            invalid_mask = ~valid_mask
            n_invalid_id = invalid_mask.sum()
            n_invalid_samples = self._num_samples_per_id[invalid_mask].sum()
            self.log_msg(
                f"{n_invalid_id} id (with {n_invalid_samples} samples) will be dropped "
                f"(n_history={self._num_history})", self.info_prefix, verbose_level=2
            )
            self.log_msg(
                f"dropped id : {', '.join(map(str, self._unique_id_arr[invalid_mask].tolist()))}",
                self.info_prefix, verbose_level=4
            )
        self._num_samples_per_id_cumsum = np.hstack([[0], np.cumsum(self._num_samples_per_id[:-1])])
        # self._id2indices need to contain 'redundant' indices here because
        # aggregation need to aggregate those 'invalid' samples
        self._id2indices_stack = np.hstack(self._id2indices)
        self.log_msg("generating aggregation attributes", self.info_prefix, verbose_level=5)
        self._get_id2valid_indices()
        self._get_valid_samples_info()

    def _get_valid_samples_info(self):
        # 'indices' in self.indices2id here doesn't refer to indices of original dataset
        # (e.g. 'indices' in self._id2indices), but refers to indices generated by sampler,
        # so we should only care 'valid' indices here
        self._num_valid_samples_per_id = [len(indices) for indices in self._id2valid_indices]
        self._num_valid_samples_per_id_cumsum = np.hstack([[0], np.cumsum(self._num_valid_samples_per_id[:-1])])
        self._num_valid_samples_per_id_cumsum = self._num_valid_samples_per_id_cumsum.astype(np_int_type)
        self.indices2id = np.repeat(np.arange(len(self._unique_id_arr)), self._num_valid_samples_per_id)
        self._id2valid_indices_stack = np.hstack(self._id2valid_indices)

    def _get_id2valid_indices(self):
        # TODO : support nan_fill here
        nan_fill, nan_ratio = map(self.config.setdefault, ["nan_fill", "nan_ratio"], ["past", 0.])
        self._id2valid_indices = [
            np.array([], np_int_type) if len(indices) < self._num_history else
            np.arange(cumsum, cumsum + len(indices) - self._num_history + 1).astype(np_int_type)
            for cumsum, indices in zip(self._num_samples_per_id_cumsum, self._id2indices)
        ]
        self._get_valid_samples_info()
        x, y = self.data.processed.xy
        feature_dim = self.data.processed_dim
        for i, valid_indices in enumerate(self._id2valid_indices):
            cumsum = self._num_valid_samples_per_id_cumsum[i]
            aggregated_flat_indices = self.aggregate(np.arange(cumsum, cumsum + len(valid_indices))).ravel()
            aggregated_x = x[aggregated_flat_indices].reshape([-1, self.num_aggregation, feature_dim])
            aggregated_x_nan_mask = np.isnan(aggregated_x)
            if y is None:
                aggregated_y_valid_mask = None
            else:
                aggregated_y = y[self.get_last_indices(aggregated_flat_indices)]
                aggregated_y_valid_mask = ~np.isnan(aggregated_y)
            aggregated_nan_ratio = aggregated_x_nan_mask.mean((1, 2))
            valid_mask = aggregated_nan_ratio <= nan_ratio
            if aggregated_y_valid_mask is not None:
                valid_mask &= aggregated_y_valid_mask.ravel()
            new_valid_indices = valid_indices[valid_mask]
            self._id2valid_indices[i] = new_valid_indices

    def aggregate(self, indices: np.ndarray) -> np.ndarray:
        """
        We've maintained two groups of indices in `_initialize` method:
        * the 'original' indices, which points to indices of original dataset
        * the 'valid' indices, which is 'virtual' should points to indices of the 'original' indices

        So we need to translate sampler indices to 'valid' indices, add offsets to the 'valid' indices,
        and then fetch the 'original' indices to fetch the corresponding data
        * _aggregate_core method will add offsets for us

        Parameters
        ----------
        indices : np.ndarray, indices come from sampler

        Returns
        -------
        indices : np.ndarray, aggregated 'original' indices

        """
        valid_indices = self._id2valid_indices_stack[indices]
        aggregated_valid_indices_mat = self._aggregate_core(valid_indices[..., None])
        aggregated = self._id2indices_stack[aggregated_valid_indices_mat.ravel()]
        reversed_aggregated = self.data.ts_sorting_indices[aggregated]
        return reversed_aggregated.reshape([-1, self.num_aggregation])

    def get_last_indices(self, aggregated_flat_indices: np.ndarray):
        aggregated_indices_mat = aggregated_flat_indices.reshape([-1, self.num_aggregation])
        return aggregated_indices_mat[..., -1]

    @classmethod
    def register(cls, name: str):
        global aggregation_dict
        return register_core(name, aggregation_dict)


@AggregationBase.register("continuous")
class ContinuousAggregation(AggregationBase):
    def _initialize(self):
        self._history_arange = np.arange(self._num_history)
        super()._initialize()

    @property
    def num_aggregation(self):
        return self._num_history

    def _aggregate_core(self, indices: np.ndarray) -> np.ndarray:
        return indices + self._history_arange


__all__ = [
    "KFold", "KRandom", "KBootstrap",
    "ImbalancedSampler", "LabelCollators", "DataLoader",
    "TimeSeriesModifier", "aggregation_dict", "AggregationBase",
]
