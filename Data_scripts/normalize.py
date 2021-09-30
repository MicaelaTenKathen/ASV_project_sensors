import numpy as np

def norm(data):
    nor = np.linalg.norm(data)
    normal = data / nor
    return normal

def norm_std(data):
    mean = np.mean(data)
    std = np.std(data)
    normal = (data - mean) / std
    return normal