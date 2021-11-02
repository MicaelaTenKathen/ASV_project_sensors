import matplotlib.pyplot as plt
import numpy as np

plt.style.use("seaborn")


def plots(data, time, nu, min_sensors, max_sensors):

    num = nu

    plt.figure(figsize=(8, 10))
    plt.suptitle("Punto de muestreo %i" % num)

    plt.subplot(311)
    plt.plot(time, data["Temperatura"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("Temp [ºC]")
    plt.ylim((min_sensors[0] - 0.01 * min_sensors[0], max_sensors[0] + 0.01 * min_sensors[0]))

    # plt.subplot(512)
    # plt.plot(time, data["Ph"])
    # plt.xlabel("tiempo [s]")
    # plt.ylabel("pH [mV]")
    # plt.ylim((min_sensors[1] - 0.1 * min_sensors[1], max_sensors[1] + 0.1 * min_sensors[1]))
    #
    # plt.subplot(513)
    # plt.plot(time, data["Oxigeno Disuelto"])
    # plt.xlabel("tiempo [s]")
    # plt.ylabel("DO [%]")
    # plt.ylim((min_sensors[2] - 0.1 * min_sensors[2], max_sensors[2] + 0.1 * min_sensors[2]))
    #
    # plt.subplot(514)
    # plt.plot(time, data["Conductividad"])
    # plt.xlabel("tiempo [s]")
    # plt.ylabel("Cond [us/cm]")
    # plt.ylim((min_sensors[3] - 0.1 * max_sensors[3], max_sensors[3] + 0.1 * max_sensors[3]))
    #
    # plt.subplot(515)
    # plt.plot(time, data["OxRed"])
    # plt.xlabel("tiempo [s]")
    # plt.ylabel("ORP [mV]")
    # plt.ylim((min_sensors[4] - 0.1 * max_sensors[4], max_sensors[4] + 0.1 * max_sensors[4]))

    plt.subplot(312)
    plt.plot(time, data["Nitrato Disuelto"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("NO3 [ppm]")
    plt.ylim((min_sensors[5] - 0.1 * max_sensors[5], max_sensors[5] + 0.1 * max_sensors[5]))

    plt.subplot(313)
    plt.plot(time, data["Amonio disuelto"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("NH4 [ppm]")
    plt.ylim((min_sensors[6] - 0.1 * max_sensors[6], max_sensors[6] + 0.1 * max_sensors[6]))

    # plt.tight_layout()

    #%% no consideramos las primeras diez muestras
    # ya que se están estabilizando las medidas


def histo(data, nu, min_sensors, max_sensors, shape_sensors):
    stable_data = data
    num = nu
    if num == 1:
        sa = 4
    else:
        sa = 4

    plt.figure(figsize=(8, 10))
    plt.suptitle("Punto de muestreo %i" % num)

    plt.subplot(311)
    plt.hist(stable_data["Temperatura"][sa:], bins=10, range=(min_sensors[0], 31.5))
    plt.xlabel("Temp [ºC]")
    plt.ylim((0, shape_sensors[0]))

    # plt.subplot(512)
    # plt.hist(stable_data["Ph"][sa:], bins=10, range=(min_sensors[1], max_sensors[1]))
    # plt.xlabel("pH [mV]")
    # plt.ylim((0, shape_sensors[0]))
    #
    # plt.subplot(513)
    # plt.hist(stable_data["Oxigeno Disuelto"][sa:], bins=10, range=(min_sensors[2], max_sensors[2]))
    # plt.xlabel("DO [%]")
    # plt.ylim((0, shape_sensors[2]))
    #
    # plt.subplot(514)
    # plt.hist(stable_data["Conductividad"][sa:], bins=10, range=(min_sensors[3], max_sensors[3]))
    # plt.xlabel("Cond [us/cm]")
    # plt.ylim((0, shape_sensors[0]))
    #
    # plt.subplot(515)
    # plt.hist(stable_data["OxRed"][sa:], bins=10, range=(min_sensors[4], max_sensors[4]))
    # plt.xlabel("ORP [mV]")
    # plt.ylim((0, shape_sensors[0]))

    plt.subplot(312)
    plt.hist(stable_data["Nitrato Disuelto"][sa:], bins=10, range=(min_sensors[5], max_sensors[5]))
    plt.xlabel("NO3 [ppm]")
    plt.ylim((0, shape_sensors[0]))

    plt.subplot(313)
    plt.hist(stable_data["Amonio disuelto"][sa:], bins=10, range=(min_sensors[6], max_sensors[6]))
    plt.xlabel("NH4 [ppm]")
    plt.ylim((0, shape_sensors[0]))

    plt.tight_layout()
