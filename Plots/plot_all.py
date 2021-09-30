import matplotlib.pyplot as plt
import numpy as np

plt.style.use("seaborn")


def plots_all(data, time):

    plt.figure(figsize=(8, 14))

    plt.subplot(511)
    plt.plot(time, data["TEMP"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("Temp [ºC]")

    plt.subplot(512)
    plt.plot(time, data["PH"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("pH [mV]")

    plt.subplot(513)
    plt.plot(time, data["DO"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("DO [%]")

    plt.subplot(514)
    plt.plot(time, data["COND"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("Cond [us/cm]")

    plt.subplot(515)
    plt.plot(time, data["ORP"])
    plt.xlabel("tiempo [s]")
    plt.ylabel("ORP [mV]")

    # plt.tight_layout()

    #%% no consideramos las primeras diez muestras
    # ya que se están estabilizando las medidas


def histo_all(data, num):
    stable_data = data
    if num == 1:
        sa = 4
    else:
        sa = 4

    plt.figure(figsize=(8, 14))

    plt.subplot(511)
    plt.hist(stable_data["TEMP"][sa:], bins=10)
    plt.xlabel("Temp [ºC]")

    plt.subplot(512)
    plt.hist(stable_data["PH"][sa:], bins=10)
    plt.xlabel("pH [mV]")

    plt.subplot(513)
    plt.hist(stable_data["DO"][sa:], bins=10)
    plt.xlabel("DO [%]")

    plt.subplot(514)
    plt.hist(stable_data["COND"][sa:], bins=10)
    plt.xlabel("Cond [us/cm]")

    plt.subplot(515)
    plt.hist(stable_data["ORP"][sa:], bins=10)
    plt.xlabel("ORP [mV]")

    plt.tight_layout()
