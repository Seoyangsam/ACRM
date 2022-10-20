import numpy as np
import pandas as pd
import src.utils as utils
import data



# FACILITIES

# impute the URI
data.facilities['URI'] = data.facilities['URI'].str[-9:]

# Change disabled parking spots to dummy indicator
data.facilities['disabled_parking_spots'] = np.where(data.facilities['disabled_parking_spots'] == 0, 0, 1)

# impute null values with 0
facil_col = ['ticket_vending_machine', 'luggage_lockers', 'free_parking', 'taxi', 'bicycle_spots', 'blue-bike',
             'bus', 'tram', 'metro', 'wheelchair_available', 'ramp', 'disabled_parking_spots', 'elevated_platform',
             'escalator_up', 'escalator_down', 'elevator_platform', 'audio_induction_loop']

for col in facil_col:
    data.facilities[col].fillna((0), inplace=True)

facil_col2 = ["street", "zip", "city"]
data.facilities = data.facilities.dropna(axis=0, subset=["street", "zip", "city"])

# INCIDENTS

# print(data.incidents.dtypes)
# data.incidents["Date of the incident"] = pd.to_datetime(data.incidents["Date of the incident"], format="%d/%m/%Y")
# print(data.incidents.dtypes)


# Satisfaction

# Drop rows that contain null value for avg satisfaction
# before (622, 3)
# after (580, 3)
# dropped 42 rows
data.satisfaction = data.satisfaction.dropna()

# Stations

# URI imputation
data.stations['URI'] = data.stations['URI'].str[-9:]

# Drop row if country code not "be"
# Before: (675, 11)
# After: (574, 11)
data.stations = data.stations[data.stations["country-code"] == "be"]

# drop the 4 alternative name columns
data.stations = data.stations.drop(["alternative-fr", "alternative-nl", "alternative-de", "alternative-en"], axis=1)

# drop rows that have 0 for official transfer time
# before (574, 11) after (569, 7)
data.stations = data.stations.dropna(subset=["official_transfer_time"])


# print(data.stations.shape)


# STOPS
def get_station_id(url):
    return url.split("/")[-1].split("#")[0]

data.stops['URI'] = data.stops['URI'].apply(get_station_id)
# 2996
# 556
# print(len(data.stops["URI"]))
# print(len(data.stops["URI"].unique()))
data.stops['parent_stop'] = data.stops['parent_stop'].apply(get_station_id)
print(data.stops['parent_stop'])

data.stops = data.stops.drop(["alternative-fr", "alternative-nl", "alternative-de", "alternative-en"], axis =1)
print(data.stops.columns)

# TRAVELERS
# rename
data.travelers = data.travelers.rename({"Avg number of travelers in the week": "week",
                                        "Avg number of travelers on Saturday": "saturday",
                                        "Avg number of travelers on Sunday": "sunday"}, axis=1)

# Therefore we impute every missing value with zero
data.travelers['week'].fillna(0, inplace=True)
data.travelers['saturday'].fillna(0, inplace=True)
data.travelers['sunday'].fillna(0, inplace=True)


#Trips
for timing in data.full_trips[
    ['Time of planned arrival', 'Time of planned departure', 'Time of real arrival', 'Time of real departure']]:
    timing = pd.to_timedelta(arg=timing, errors="coerce")


# print(data.full_trips.dtypes)
# replace names of travelers using the dictionary
travelers = data.travelers.replace({"Station": utils.Dict})
# print(travelers.shape)
# print(data.facilities.shape)
# len(list(set(data.facilities['name']).intersection(set(travelers['Station']))))
# len(list(set(data.facilities['name']).intersection(set(travelers['Station']))))
# print(travelers.shape)
# print(data.facilities.shape)

"function to get first word of a sentence"
def get_first_word(sentence):
    return sentence.split(" ")[0]

#print 2 columns and sort by number 2nd column descending
def print_2col_sort_2ndcol_desc(df, col1, col2):
    print(df[[col1, col2]].sort_values(by=[col2], ascending=False))
def print_2col_sort_2ndcol(df, col1, col2):
    print(df[[col1, col2]].sort_values(by=[col2]))