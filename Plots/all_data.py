import pandas as pd
from Plots.plot_all import *
from Data_scripts.mean_std import *

total_data = pd.read_csv("../Data/data_11_06_2021_v2.csv", delimiter=",")
total_data["ORP"] = np.multiply(total_data["ORP"], 1000)
plots_all(total_data, np.arange(0, np.copy(total_data["TEMP"]).shape[0], 1) * 13)
histo_all(total_data, 1)
