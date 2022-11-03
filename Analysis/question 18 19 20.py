#question 18
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
from sklearn.linear_model import LinearRegression
import os


####################   LOAD IN DATA  ####################

# This file describes facilities available in NMBS/SNCB stations.
facilities = pd.read_csv("../../Data/Unprocessed/facilities.csv")

# This file describes all the type of incidents that happened with the resulting delays and cancellations.
incidents = pd.read_csv("../../Data/Unprocessed/incidents.csv", sep=';')

# This file describes the average satisfaction score for each station.
satisfaction = pd.read_csv("../../Data/Unprocessed/satisfaction.csv")

# This file describes all NMBS/SNCB stations in Belgium.
# A station can have multiple platforms (stops), which are described in stops.csv.
stations = pd.read_csv("../../Data/Unprocessed/stations.csv")

# This file describes all NMBS/SNCB stops in Belgium.
# Each platform is a separate stop location.
stops = pd.read_csv("../../Data/Unprocessed/stops.csv")

# This file describes the average number of travelers per station. URI: The URI identifying this station.
travelers = pd.read_excel("../../Data/Unprocessed/travelers.xlsx", skiprows=1)
travelers = travelers.rename({"Avg number of travelers in the week": "week",
                              "Avg number of travelers on Saturday": "saturday",
                              "Avg number of travelers on Sunday": "sunday"}, axis=1)

# This directory contains files that each describe the information on train trips on a certain day
trips_dir = "../Data/Trips/"
all_trips = [obs for obs in os.listdir(trips_dir) if ".DS" not in obs]

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width',200)


#question 18

print(incidents["Place"].describe())
print(incidents["Description of the incident"].describe())
print(incidents)
print(incidents.isnull())
print(incidents.groupby('Place').size())
incidents_location = pd.Series(incidents.groupby('Place').size())
#incidents_location.plot.pie()
print(incidents.groupby('Description of the incident').size())
incidents_type = pd.Series(incidents.groupby('Description of the incident').size())
plt.figure(figsize=(20,20))
print(incidents_type)

incidents_type.plot.pie(ylabel='')
num1 = 1
num2 = 0
num3 = 3
num4 = 0
plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4)
plt.show()



#19
"""
stations['name'] = stations['name'].str.replace("é","e")
stations['name'] = stations['name'].str.replace("à","a")
stations['name'] = stations['name'].str.replace("É","E")
stations['name'] = stations['name'].str.replace("â","a")
stations['name'] = stations['name'].str.replace("è","e")
stations['name'] = stations['name'].str.replace("ê","e")
stations['name'] = stations['name'].str.replace("ô","o")
stations['name'] = stations['name'].str.replace("œ","oe")
stations['name'] = stations['name'].str.replace("û","u")
stations['name'] = stations['name'].str.upper()
#print(stations)
new_data1 = pd.merge(satisfaction,stations,how ='inner',left_on = "station",right_on = "name")
#new_data1 = new_data1.dropna(subset=["avg_stop_times"])
new_data1 = new_data1.dropna(subset=["Avg Satisfaction"])
print(new_data1)

plt.figure(figsize=(5,3))
plt.scatter(new_data1["avg_stop_times"],new_data1["Avg Satisfaction"],s=4)
lr_mode = LinearRegression()
lr_mode.fit(X=new_data1[["avg_stop_times"]],y=new_data1["Avg Satisfaction"])
avg_est = lr_mode.predict(new_data1[["avg_stop_times"]])
plt.plot(new_data1["avg_stop_times"],avg_est,"-",color='red')
plt.legend()
plt.show()
"""