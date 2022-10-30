import pandas as pd
from pathlib import Path
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import src.utils as utils
import numpy as np
import geopandas as gpd

#########################################################   LOAD IN DATA  ##########################################################

path = Path(__file__).parent / "../../Data/Unprocessed"

# This file describes facilities available in NMBS/SNCB stations.
facilities = pd.read_csv(path / "facilities.csv")

# This file describes all the type of incidents that happened with the resulting delays and cancellations.
incidents = pd.read_csv(path / "incidents.csv", sep=';')

# This file describes the average satisfaction score for each station.
satisfaction = pd.read_csv(path / "satisfaction.csv")

# This file describes all NMBS/SNCB stations in Belgium.
# A station can have multiple platforms (stops), which are described in stops.csv.
stations = pd.read_csv(path / "stations.csv")

# This file describes all NMBS/SNCB stops in Belgium.
# Each platform is a separate stop location.
stops = pd.read_csv(path / "stops.csv")

# This file describes the average number of travelers per station. URI: The URI identifying this station.
stations = pd.read_csv(path / "stations.csv")

travelers = pd.read_csv(path / "travelers_correct.csv", delimiter=';')

# rename the columns
travelers = travelers.rename({"Avg number of travelers in the week": "week",
                              "Avg number of travelers on Saturday": "saturday",
                              "Avg number of travelers on Sunday": "sunday"}, axis=1)

# This file describes all the trips that happened in the NMBS/SNCB network.
full_trips = pd.concat([pd.read_csv(path, sep=",") for path in (path / "Trips/").glob('*.csv')], axis=0)

# map of the provinces of belgium .shp
provinces = gpd.read_file(path / "BELGIUM_-_Provinces/" "BELGIUM_-_Provinces.shp")

sporen= gpd.read_file(path / "geosporen"/ "geosporen.shp")

inhabitants_per_province = pd.read_excel(path / "inhabitants_per_province.xlsx")

# for each value i of dataframe["Route"], get routes[i]["hey"] and store it in a dataframe["temps"]
def get_route_time(df, routes, key):
    df[key] = df["Route"].apply(lambda i: routes[i][key])
    return df

# for each value of a column from a dataframe, divide the column by 7 and store it in a new column, using lambda function
def divide_by_7(df, column):
    df[column + "_per_day"] = df[column].apply(lambda x: x / 7)
    return df

# get the average value of the column ["Delay_frequency"] per distinct value of another column ["Re"] and store it in a new column ["Re_new"]. Put all this in a new dataframe
# with columns ["Re_new", "Delay_frequency" , "Re"]
def get_average_per(df, column, per):
    df = df.groupby([per])[column].mean().reset_index(name=column + "_per_" + per)
    return df

# create a new dataframe that takes the columns ["stations, "date"] from the dataframe trips
new_df= full_trips[["Station", "Date"]]

#dtop the column "Route" from the dataframe trips
full_trips = full_trips.drop(columns=["Route"])

#  get outliers from a column with 5% significance level
def get_outliers(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    outliers = df[(df[column] < q1 - 1.5 * iqr) | (df[column] > q3 + 1.5 * iqr)]
    return outliers












#########################################################  FACILITIES  ##########################################################
# impute the URI
facilities['URI'] = facilities['URI'].str[-9:]

# Change disabled parking spots to dummy indicator
facilities['disabled_parking_spots'] = np.where(facilities['disabled_parking_spots'] == 0, 0, 1)

# Assumption that null values mean that the facilities are not available.
# So we impute null values with 0
facil_col = ['ticket_vending_machine', 'luggage_lockers', 'free_parking', 'taxi', 'bicycle_spots', 'blue-bike',
             'bus', 'tram', 'metro', 'wheelchair_available', 'ramp', 'disabled_parking_spots', 'elevated_platform',
             'escalator_up', 'escalator_down', 'elevator_platform', 'audio_induction_loop']

for col in facil_col:
    facilities[col].fillna((0), inplace=True)

# If street, zip and city are null, then the station is not from Belgium, so we can drop it
facilities = facilities.dropna(axis=0, subset=["street", "zip", "city"])

# Stations that do not have openinghours (null values), simply don't have a 'building'
# We change those null values to 00:00 , interpreted as opening and closing at 00:00 so no opening time , (NOT opened 24/7)
facility_openinghours = ['sales_open_monday', 'sales_close_monday', 'sales_open_tuesday',
                         'sales_close_tuesday', 'sales_open_wednesday', 'sales_close_wednesday',
                         'sales_open_thursday', 'sales_close_thursday', 'sales_open_friday',
                         'sales_close_friday', 'sales_open_saturday', 'sales_close_saturday',
                         'sales_open_sunday', 'sales_close_sunday']
for col in facility_openinghours:
    facilities[col] = facilities[col].fillna("00:00")

# Change all opening and closing times to datetime
for fac_time in facilities[facility_openinghours]:
    if not is_datetime(facilities[fac_time]):
        facilities[fac_time] = pd.to_datetime(facilities[fac_time].astype(str), format='%H:%M') - pd.to_datetime(
            '00:00', format='%H:%M')

# Standardize name for facilities, we might have to do this for other ones too.So beware
facilities['name'] = facilities['name'].str.lower()

#########################################################  INCIDENTS  ##########################################################

# Change date of the incident to datetime
if not is_datetime(incidents["Date of the incident"]):
    incidents["Date of the incident"] = pd.to_datetime(incidents["Date of the incident"].astype(str),
                                                       format='%d/%m/%y')
# Remove month, since Date of the incidents already captures the month + extra info(day)
incidents = incidents.drop("Month", axis=1)

# General number of delay and cancellation incidents
frequency_trips = full_trips["Name of the stop"].value_counts()
travelers["sum"] = travelers["week"] + travelers["saturday"] + travelers["sunday"]
frequency_travelers = travelers[["Station", "sum"]].sort_values(by=["sum"], ascending=False)

incidents['Place'] = incidents['Place'].str.lower()

#########################################################  SATISFACTION  ##########################################################
# drop the rows that have null values
satisfaction.dropna(inplace=True)

#########################################################  STATIONS  ##########################################################
# URI imputation to only get the digits
stations['URI'] = stations['URI'].str[-9:]

# Drop row if country code not "be"
stations = stations[stations["country-code"] == "be"]

# drop the 4 alternative name columns
stations = stations.drop(["alternative-fr", "alternative-nl", "alternative-de", "alternative-en"], axis=1)

# drop rows that have 0 for official transfer time: they aren't stations anymore
stations = stations.dropna(subset=["official_transfer_time"])

#########################################################  STOPS  ##########################################################
# Impute name and URI, we dont need to keep the # of URI because we store the same number in platform
stops['URI'] = stops['URI'].str[-9:]
stops['parent_stop'] = stops['parent_stop'].str[-9:]

# Drop the name columns
stops = stops.drop(["alternative-fr", "alternative-nl", "alternative-de", "alternative-en"], axis=1)

#########################################################  TRAVELERS  ##########################################################

# Impute missing values with 0: because null value indicates no train rides on that day /week
travelers['week'].fillna(0, inplace=True)
travelers['saturday'].fillna(0, inplace=True)
travelers['sunday'].fillna(0, inplace=True)

# Standardize name for travelers
travelers['Station'] = travelers['Station'].str.lower()
travelers = travelers.replace({"Station": utils.Dict})

#########################################################  TRIPS  ##########################################################
# Change all dates and times to datetime STILL NEEDS TO BE CHECKED
# trips_dates= ["Date of departure", 'Date of planned arrival',
#        'Date of planned departure', 'Date of real arrival',
#        'Date of real departure']
# trips_times = ['Time of real arrival',
#        'Time of real departure', 'Time of planned arrival',
#        'Time of planned departure']
#
# change 'time of real arrival' to pd.datetime


full_trips['Time of real arrival'] = pd.to_datetime(full_trips['Time of real arrival'])
full_trips['Time of planned arrival'] = pd.to_datetime(full_trips['Time of planned arrival'])
full_trips['Time of real departure'] = pd.to_datetime(full_trips['Time of real departure'])
full_trips['Time of planned departure'] = pd.to_datetime(full_trips['Time of planned departure'])


# define function to get delay
def get_delay(expected, real):
    if real > expected:
        delay = (real - expected).seconds
    else:
        # changed this to 0 or else we won't take into account the number of trips that had no delay.
        delay = 0
    return delay


full_trips['Delay time'] = full_trips.apply(
    lambda obs: get_delay(obs['Time of planned arrival'], obs['Time of real arrival']), axis=1)
