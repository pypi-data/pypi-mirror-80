__author__ = 'Milo Utsch'
__version__ = '0.1.1'

import typing as tp

import numpy as np
import pandas as pd

NUMBER = tp.Union[float, int]
ARRAY = tp.Union[pd.Series, np.ndarray]


def weighted_mean(x: ARRAY, w: ARRAY) -> float:
    """Takes weighted mean.

    :param x: Values to be averaged.
    :type x: ``pd.Series`` or ``np.ndarray``
    :param w: Weights to be applied.
    :type w: ``pd.Series`` or ``np.ndarray``
    :return: Weighted mean.
    :rtype: ``float``
    """
    return np.vdot(x, w) / np.sum(w)


def scale(x: NUMBER, min_: NUMBER, max_: NUMBER) -> NUMBER:
    """Transform a value x to a scale between min_ and max_.

    :param x: Value to be converted.
    :type x: ``float`` or ``int``
    :param min_: Minimum value on scale.
    :type min_: ``float`` or ``int``
    :param max_: Maximum value on scale.
    :type max_: ``float`` or ``int``
    :return: Scaled value.
    :rtype: ``float`` or ``int``
    """
    return (x - min_) / (max_ - min_)
