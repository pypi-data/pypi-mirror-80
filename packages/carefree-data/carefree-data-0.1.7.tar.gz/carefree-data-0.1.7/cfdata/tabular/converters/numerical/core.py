import numpy as np

from typing import *

from ...misc import *
from ....types import *
from ..base import Converter


@Converter.register("numerical")
class NumericalConverter(Converter):
    @property
    def nan_fill(self) -> Union[float, None]:
        return None if self._nan_fill is None else self._feature_statistics[self._nan_fill]

    @property
    def statistics(self) -> Dict[str, float]:
        return self._feature_statistics

    def _initialize(self, **kwargs) -> None:
        self._nan_fill = kwargs.get("nan_fill", "median")
        self._feature_statistics = {}

    def _fit(self) -> "Converter":
        assert self.info.is_valid and self.info.is_numerical
        nan_mask = self.info.nan_mask
        np_flat_features = self.info.flat_arr.copy()
        base_attrs = ["median", "mean", "std", "min", "max"]
        for attr in base_attrs:
            if nan_mask is None:
                np_flat_valid = np_flat_features
            else:
                np_flat_valid = np_flat_features[~nan_mask]
            self._feature_statistics[attr] = getattr(np, attr)(np_flat_valid).item()
        if self._nan_fill is None or not self.info.contains_nan:
            self._converted_features = np_flat_features
        else:
            np_flat_features[nan_mask] = self.nan_fill
            self._converted_features = np_flat_features
        return self

    def _convert(self,
                 flat_arr: flat_arr_type) -> np.ndarray:
        np_flat = np.asarray(flat_arr, np_float_type)
        if self._nan_fill is None:
            return np_flat
        np_flat[np.isnan(np_flat)] = self.nan_fill
        return np_flat

    def _recover(self,
                 flat_arr: flat_arr_type) -> np.ndarray:
        return np.asarray(flat_arr, np_float_type)


__all__ = ["NumericalConverter"]
