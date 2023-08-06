import torch
import numpy as np
import tensorflow as tf
import scipy.sparse as sp

from graphgallery import floatx, intx, backend
from graphgallery import (is_list_like,
                          is_interger_scalar,
                          is_tensor_or_variable)


def asintarr(x, dtype: str = None):
    """Convert `x` to interger Numpy array.

    Parameters:
    ----------
    x: tf.Tensor, tf.Variable, Scipy sparse matrix,
        Numpy array-like, etc.

    Returns:
    ----------
        Integer Numpy array with dtype or `graphgallery.intx()`

    """
    if dtype is None:
        dtype = intx()

    if is_tensor_or_variable(x):
        if x.dtype != dtype:
            kind = backend().kind
            if kind == "T":
                x = tf.cast(x, dtype=dtype)
            else:
                x = x.to(getattr(torch, dtype))
        return x

    if is_interger_scalar(x):
        x = np.asarray([x], dtype=dtype)
    elif is_list_like(x) or isinstance(x, (np.ndarray, np.matrix)):
        x = np.asarray(x, dtype=dtype)
    else:
        raise ValueError(
            f"Invalid input which should be either array-like or integer scalar, but got {type(x)}.")
    return x


def indices2mask(indices, shape):
    mask = np.zeros(shape, np.bool)
    mask[indices] = True
    return mask
