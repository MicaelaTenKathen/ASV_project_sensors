import numpy as np


def mean(array, num):
    if num == 1:
        sa = 10
    else:
        sa = 3
    mean = np.mean(array[sa:])
    std = np.std(array[sa:])
    shape = array.shape[0]
    return mean, std, shape