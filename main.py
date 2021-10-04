import pandas as pd
from Data_scripts.data_collected_time import data_collec
from Data_scripts.data_collected_cond import data_collec_cond
from Data_scripts.limits import *
from Data_scripts.mean_std import mean
from Data_scripts.normalize import *
from Plots.sensors import comparison
from Plots.plot import *

total_data = pd.read_csv("Data/data_11_06_2021_v2.csv", delimiter=",")

total_data["DATE"] = pd.to_datetime(total_data["DATE"])
total_sample = np.copy(total_data["SAMPLE_NUM"])

last_data = 0
init = 0
num_points = 1

time = False
cond = True

data1 = np.copy(total_data["DATE"])
n_data = np.arange(1, num_points + 1, 1)
sensors = ["TEMP", "PH", "DO", "COND", "ORP", "SWINO3", "SWINH4"]  # , "BAT"]
name_sensors = ['temp%s', 'ph%s', 'do%s', 'cond%s', 'orp%s', 'no3%s', 'nh4%s']  # , 'bat%s']
mean_sensors = ['mean_temp%s', 'mean_ph%s', 'mean_do%s', 'mean_cond%s', 'mean_orp%s', 'mean_no3%s', 'mean_nh4%a']  # , 'mean_bat%s']
std_sensors = ['std_temp%s', 'std_ph%s', 'std_do%s', 'std_cond%s', 'std_orp%s', 'std_no3%s', 'std_nh4%s']  # , 'std_bat%s']

if time:
    for k in range(len(sensors)):
        init = 0
        for j in range(len(n_data)):
            globals()[name_sensors[k] % n_data[j]], init = data_collec(total_data, init, sensors, k)
            m = j
elif cond:
    for k in range(len(sensors)):
        init = 0
        conf = False
        p = 0
        m = 0
        for j in range(len(n_data)):
            data_con, init, conf = data_collec_cond(total_data, init, sensors, k, conf)
            if conf:
                if p != 3:
                    if k == 4:
                        data_con = np.multiply(data_con, 1000)
                    globals()[name_sensors[k] % n_data[m]] = np.copy(data_con)
                    p += 1
                    m += 1
                    conf = False
                else:
                    p += 1
                    conf = False

d = 0

for k in range(len(sensors)):
    d = 0
    r = 0
    data_l = list()
    while d < 3:
        globals()[name_sensors[k] % n_data[3]] = np.delete(globals()[name_sensors[k] % n_data[3]], - 1)
        d += 1
    while r < m:
        data_l.extend(globals()[name_sensors[k] % n_data[r]])
        r += 1
    globals()['total%s' % sensors[k]] = np.copy(data_l)

r = 0
while r < m:

    globals()['sample_points%s' % n_data[r]] = {"TEMP": globals()[name_sensors[0] % n_data[r]],
                                                "PH": globals()[name_sensors[1] % n_data[r]],
                                                "DO": globals()[name_sensors[2] % n_data[r]],
                                                "COND": globals()[name_sensors[3] % n_data[r]],
                                                "ORP": globals()[name_sensors[4] % n_data[r]],
                                                "SWINO3": globals()[name_sensors[5] % n_data[r]],
                                                "SWINH4": globals()[name_sensors[6] % n_data[r]]}
    # "BAT": globals()[name_sensors[5] % n_data[j]]

    globals()['time%s' % n_data[r]] = np.arange(0, np.array(globals()[name_sensors[0] % n_data[r]]).shape[0], 1) * 13

    r += 1

min_sensors = []
max_sensors = []
shape_sensors = []

for k in range(len(sensors)):
    min_array = []
    max_array = []
    shape_array = []
    r = 0

    while r < m:
        min_array, max_array, shape_array = min_max(globals()['sample_points%s' % n_data[r]], sensors, k, min_array,
                                                    max_array, shape_array)
        r += 1
    min_sensors, max_sensors, shape_sensors = limits_plots(min_array, max_array, shape_array, min_sensors, max_sensors,
                                                           shape_sensors)

r = 0
while r < m:
    plots(globals()['sample_points%s' % n_data[r]], globals()['time%s' % n_data[r]], n_data[r], min_sensors,
          max_sensors)
    histo(globals()['sample_points%s' % n_data[r]], n_data[r], min_sensors, max_sensors, shape_sensors)
    r += 1

total_sample = {"TEMP": globals()['total%s' % sensors[0]],
                "PH": globals()['total%s' % sensors[1]],
                "DO": globals()['total%s' % sensors[2]],
                "COND": globals()['total%s' % sensors[3]],
                "ORP": globals()['total%s' % sensors[4]],
                }

histo(total_sample, 1, min_sensors, max_sensors, shape_sensors)

array_n = list()
max_zone = list()

for t in range(len(sensors)):
    mea = list()
    st = list()
    h = 0
    r = 0
    sum_shape = 0
    st_cua = list()
    n_zone = list()
    cua_zones = 0
    med = 0

    print(n_data[h])
    while r < m:
        a = np.copy(globals()['sample_points%s' % n_data[r]][sensors[t]])
        b = norm_std(np.array(a))
        me, s, sha = mean(np.array(a), n_data[r])
        mea.append(me)
        st.append(s)
        cua = float(s) * float(s)
        med = med + me
        cua_zones = cua_zones + cua
        sum_shape = sum_shape + sha
        nz = ((sha * cua * 1.96 * 1.96) / ((0.05 * me) * (0.05 * me) * (sha - 1) + cua * 1.96 * 1.96))
        n_zone.append(nz)
        r += 1
    print(n_zone)
    print(sensors[t])
    max_z = np.max(np.array(n_zone))
    max_zone.append(max_z)
    n = ((sum_shape * cua_zones * 1.96 * 1.96) / ((med * 0.05) * (med * 0.05) * (sum_shape - 1) + cua_zones * 1.96 * 1.96))
    array_n.append(n)
    globals()['sensor%s' % sensors[t]] = {"MEAN": mea,
                                          "STD": st}
    comparison(globals()['sensor%s' % sensors[t]], t, r + 1)

n_max = np.max(np.array(array_n))
print(array_n)
max_n = np.max(np.array(max_zone))
print(max_n)