import pandas as pd
# from Data_scripts.data_collected_time import data_collec
# from Data_scripts.data_collected import data_collec_cond
from Data_scripts.limits import *
from Data_scripts.mean_std import mean
from Data_scripts.normalize import *
from Plots.sensors import comparison
from Plots.plot import *

total_data1 = pd.read_csv("Data/datapoint(170222point1).csv", delimiter=",")
# total_data2 = pd.read_csv("Data/datapoint2(0110).csv", delimiter=",")
# total_data3 = pd.read_csv("Data/datapoint3(0110).csv", delimiter=",")
# total_data4 = pd.read_csv("Data/datapoint4(0110).csv", delimiter=",")
# total_data5 = pd.read_csv("Data/datapoint5(0110).csv", delimiter=",")

total_data1["Fecha"] = pd.to_datetime(total_data1["Fecha"])
total_sample = np.copy(total_data1["SAMPLE_NUM"])

last_data = 0
init = 0
num_points = 1

time = False
cond = False
only = True

data1 = np.copy(total_data1["Fecha"])
n_data = [total_data1]#, total_data2, total_data3, total_data4, total_data5]
h = np.array(n_data).shape[0] - 1
sensors = ["Temperatura", "Ph", "Oxigeno Disuelto", "Conductividad", "OxRed", "Nitrato Disuelto",
           "Amonio disuelto"]  # , "BAT"]
name_sensors = ['temp%s', 'ph%s', 'do%s', 'cond%s', 'orp%s', 'no3%s', 'nh4%s']  # , 'bat%s']
mean_sensors = ['mean_temp%s', 'mean_ph%s', 'mean_do%s', 'mean_cond%s', 'mean_orp%s', 'mean_no3%s',
                'mean_nh4%a']  # , 'mean_bat%s']
std_sensors = ['std_temp%s', 'std_ph%s', 'std_do%s', 'std_cond%s', 'std_orp%s', 'std_no3%s',
               'std_nh4%s']  # , 'std_bat%s']

for k in range(len(sensors)):
    p = 0
    while p <= h:
        ar = n_data[p]
        globals()[name_sensors[k] % p] = pd.DataFrame.to_numpy(ar[sensors[k]])
        p += 1

for k in range(len(sensors)):
    p = 0
    data_l = list()
    while p <= h:
        data_l.extend(globals()[name_sensors[k] % p])
        p += 1
    globals()['total%s' % sensors[k]] = np.copy(data_l)

p = 0
while p <= h:
    globals()['sample_points%s' % p] = {"Temperatura": globals()[name_sensors[0] % p],  # % n_data[r]],
                                  "Ph": globals()[name_sensors[1] % p],  # % n_data[r]],
                                  "Oxigeno Disuelto": globals()[name_sensors[2] % p],  # % n_data[r]],
                                  "Conductividad": globals()[name_sensors[3] % p],  # % n_data[r]],
                                  "OxRed": globals()[name_sensors[4] % p],  # % n_data[r]],
                                  "Nitrato Disuelto": globals()[name_sensors[5] % p],  # % n_data[r]],
                                  "Amonio disuelto": globals()[name_sensors[6] % p]}  # % n_data[r]]}
# "BAT": globals()[name_sensors[5] % n_data[j]]

    globals()['time%s' % p] = np.arange(0, np.array(globals()[name_sensors[0] % p]).shape[0], 1) * 15
    p += 1

min_sensors = []
max_sensors = []
shape_sensors = []

for k in range(len(sensors)):
    min_array = []
    max_array = []
    shape_array = []
    r = 0
    while r <= h:
        min_array, max_array, shape_array = min_max(globals()['sample_points%s' % r], sensors, k, min_array,
                                                    max_array, shape_array)
        r += 1
    min_sensors, max_sensors, shape_sensors = limits_plots(min_array, max_array, shape_array, min_sensors, max_sensors,
                                                           shape_sensors)

r = 0
while r <= h:
    plots(globals()['sample_points%s' % r], globals()['time%s' % r], r, min_sensors,
          max_sensors)
    histo(globals()['sample_points%s' % r], r, min_sensors, max_sensors, shape_sensors)
    r += 1

total_sample = {"Temperatura": globals()['total%s' % sensors[0]],
                "Ph": globals()['total%s' % sensors[1]],
                "Oxigeno Disuelto": globals()['total%s' % sensors[2]],
                "Conductividad": globals()['total%s' % sensors[3]],
                "OxRed": globals()['total%s' % sensors[4]],
                "Nitrato Disuelto": globals()['total%s' % sensors[5]],
                "Amonio disuelto": globals()['total%s' % sensors[6]]}

histo(total_sample, 0, min_sensors, max_sensors, shape_sensors)

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

    while r <= h:
        a = np.copy(globals()['sample_points%s' % r][sensors[t]])
        b = norm_std(np.array(a))
        me, s, sha = mean(np.array(a), r)
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
    n = ((sum_shape * cua_zones * 1.96 * 1.96) / (
            (med * 0.05) * (med * 0.05) * (sum_shape - 1) + cua_zones * 1.96 * 1.96))
    array_n.append(n)
    globals()['sensor%s' % sensors[t]] = {"MEAN": mea,
                                          "STD": st}
    comparison(globals()['sensor%s' % sensors[t]], t, r + 1)

n_max = np.max(np.array(array_n))
print(array_n)
max_n = np.max(np.array(max_zone))
print(max_n)
