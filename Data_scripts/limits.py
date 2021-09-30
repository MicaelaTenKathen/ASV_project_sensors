import numpy as np


def min_max(data, sensors, k, min_array, max_array, shape_array):
    min = np.min(np.array(data[sensors[k]]))
    max = np.max(np.array(data[sensors[k]]))
    shape = np.shape(np.array(data[sensors[k]]))
    min_array.append(min)
    max_array.append(max)
    shape_array.append(shape)

    return min_array, max_array, shape_array


def limits_plots(min_array, max_array, shape_array, min_sensors, max_sensors, shape_sensors):
    min = np.min(np.array(min_array))
    max = np.max(np.array(max_array))
    shape = np.max(np.array(shape_array))
    min_sensors.append(min)
    max_sensors.append(max)
    shape_sensors.append(shape)

    return min_sensors, max_sensors, shape_sensors
