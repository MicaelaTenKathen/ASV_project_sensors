import numpy as np
import matplotlib.pyplot as plt


def comparison(data, i, num_points):
    width = 0.2
    x = np.arange(1, num_points, 1)

    if i == 0:
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        fig.suptitle("Temperatura")
        ax.bar(x, data["MEAN"], width, color='b', yerr=data["STD"], label='Temperatura', alpha=0.6)
        ax.set_xlabel("Punto de muestreo")
        ax.set_ylabel("ºC")

    elif i == 1:
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        fig.suptitle("pH")
        ax.bar(x, data["MEAN"], width, color='c', yerr=data["STD"], label='pH', alpha=0.9)
        ax.set_xlabel("Punto de muestreo")
        ax.set_ylabel("mV")

    elif i == 2:
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        fig.suptitle("DO")
        ax.bar(x, data["MEAN"], width, color='y', yerr=data["STD"], label='DO', alpha=0.7)
        ax.set_xlabel("Punto de muestreo")
        ax.set_ylabel("%")

    elif i == 3:
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        fig.suptitle("Conductividad")
        ax.bar(x, data["MEAN"], width, color='r', yerr=data["STD"], label='Conductividad', alpha=0.6)
        ax.set_xlabel("Punto de muestreo")
        ax.set_ylabel("us/cm")

    elif i == 4:
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        fig.suptitle("ORP")
        ax.bar(x, data["MEAN"], width, color='g', yerr=data["STD"], label='ORP', alpha=0.7)
        ax.set_xlabel("Punto de muestreo")
        ax.set_ylabel("mV")