import matplotlib.pyplot as plt
import numpy as np

plt.style.use("seaborn")


def plots(data, time, num, min_sensors, max_sensors):

    plt.figure(figsize=(8, 14))
    plt.suptitle("Punto de muestreo %i" % num)

    plt.subplot(511)
    plt.plot(time, data["TEMP"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("Temp [ºC]")
    plt.ylim((min_sensors[0] - 0.01 * min_sensors[0], max_sensors[0] + 0.01 * min_sensors[0]))

    plt.subplot(512)
    plt.plot(time, data["PH"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("pH [mV]")
    plt.ylim((min_sensors[1] - 0.1 * min_sensors[1], max_sensors[1] + 0.1 * min_sensors[1]))

    plt.subplot(513)
    plt.plot(time, data["DO"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("DO [%]")
    plt.ylim((min_sensors[2] - 0.1 * min_sensors[2], max_sensors[2] + 0.1 * min_sensors[2]))

    plt.subplot(514)
    plt.plot(time, data["COND"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("Cond [us/cm]")
    plt.ylim((min_sensors[3] - 0.1 * max_sensors[3], max_sensors[3] + 0.1 * max_sensors[3]))

    plt.subplot(515)
    plt.plot(time, data["ORP"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("ORP [mV]")
    plt.ylim((min_sensors[4] - 0.1 * max_sensors[4], max_sensors[4] + 0.1 * max_sensors[4]))

    # plt.tight_layout()

    #%% no consideramos las primeras diez muestras
    # ya que se están estabilizando las medidas


def histo(data, num, min_sensors, max_sensors, shape_sensors):
    stable_data = data
    if num == 1:
        sa = 4
    else:
        sa = 4

    plt.figure(figsize=(8, 14))
    plt.suptitle("Punto de muestreo %i" % num)

    plt.subplot(511)
    plt.hist(stable_data["TEMP"][sa:], bins=10, range=(min_sensors[0], 31.5))
    plt.xlabel("Temp [ºC]")
    plt.ylim((0, shape_sensors[0]))

    plt.subplot(512)
    plt.hist(stable_data["PH"][sa:], bins=10, range=(min_sensors[1], max_sensors[1]))
    plt.xlabel("pH [mV]")
    plt.ylim((0, shape_sensors[0]))

    plt.subplot(513)
    plt.hist(stable_data["DO"][sa:], bins=10, range=(min_sensors[2], max_sensors[2]))
    plt.xlabel("DO [%]")
    plt.ylim((0, shape_sensors[2]))

    plt.subplot(514)
    plt.hist(stable_data["COND"][sa:], bins=10, range=(min_sensors[3], max_sensors[3]))
    plt.xlabel("Cond [us/cm]")
    plt.ylim((0, shape_sensors[0]))

    plt.subplot(515)
    plt.hist(stable_data["ORP"][sa:], bins=10, range=(min_sensors[4], max_sensors[4]))
    plt.xlabel("ORP [mV]")
    plt.ylim((0, shape_sensors[0]))

    plt.tight_layout()
