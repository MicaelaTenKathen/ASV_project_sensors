# ASV_project_sensors

Code to discriminate sensor data from [csv file](Data/data_01_06_2021.csv).

## Installation

Please install the ```requirements.txt``` file before use.

```
pip install -r requirements.txt
```

## Use

First, the quotes must be removed from the csv file data. One option is to use Powershell. Copy the following command line and paste into Powershell:

```
(Get-Content C:\fso\UsersConsolidated.csv) | % {$_ -replace '"', ''} | out-file -FilePath C:\fso\UsersConsolidated.csv -Force -Encoding ascii
```

where ```C:\fso\UsersConsolidated.csv``` corresponds to the path of the csv file.

For more information, go to [this link](https://devblogs.microsoft.com/scripting/remove-unwanted-quotation-marks-from-csv-files-by-using-powershell/)

The [main](SWprocessing.py) file contains the main part of the code. Running this script will generate the graphs.


On line 7, the file must be selected. Preferably, save the document in the [Data](Data) folder and extract from there.

```
total_data = pd.read_csv("Data/data_01_06_2021.csv", delimiter=",")
```


On line 14, the number of sample points is determined:

```
num_points = 7
```


On line 18, 19, 20 and 21, the names and variables for the sensors:

```
sensors = ["TEMP", "PH", "DO", "COND", "ORP"] #, "BAT"]
name_sensors = ['temp%s', 'ph%s', 'do%s', 'cond%s', 'orp%s']  #, 'bat%s']
mean_sensors = ['mean_temp%s', 'mean_ph%s', 'mean_do%s', 'mean_cond%s', 'mean_orp%s'] #, 'mean_bat%s']
std_sensors = ['std_temp%s', 'std_ph%s', 'std_do%s', 'std_cond%s', 'std_orp%s'] #, 'std_bat%s']
```



To plot all the data of the csv file, [All data](Data_scripts/all_data.py) can be used.

