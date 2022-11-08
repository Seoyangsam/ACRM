import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# load in csv file
facilities = pd.read_csv("../../Data/Unprocessed/facilities.csv")

# show
facilities.head(5)
# create list of facility columns
facil_col = ['ticket_vending_machine', 'luggage_lockers', 'free_parking', 'taxi', 'bicycle_spots', 'blue-bike',
             'bus', 'tram', 'metro', 'wheelchair_available', 'ramp', 'disabled_parking_spots', 'elevated_platform',
             'escalator_up', 'escalator_down', 'elevator_platform', 'audio_induction_loop']

# check frequency of each variable
facilities["disabled_parking_spots"].value_counts()

# for the sake of this exercise, we will simply impute all missing values of the facilities with zero
for col in facil_col:
    facilities[col].fillna((0), inplace=True)

# check if it worked
for col in facilities.columns:
    missings = len(facilities[col][facilities[col].isnull()]) / float(len(facilities))
    print(col, missings)

# PROBLEM: disabled_parking_spots is the number of spots instead of a dummy indicator
# so let's create a dummy variable
facilities['disabled_parking_spots_indicator'] = np.where(facilities['disabled_parking_spots']==0,0,1)

# drop old variable and add new name to our list
facil_col.remove('disabled_parking_spots')
facil_col = facil_col + ['disabled_parking_spots_indicator']

# show
facil_col


# compute total number of facilities per station
facilities['number_facilities'] = facilities[facil_col].sum(axis = 1)

# show
facilities['number_facilities']
# prepare data for number of facilities in different stations
input_plot = pd.DataFrame(facilities['number_facilities'].value_counts())
# show
input_plot
# prepare dataset as input for pyplot because we want two columns to make a plot
input_plot['NumberFacilities'] = input_plot.index
input_plot = input_plot.rename(index=str, columns={'number_facilities': 'Occurence'})

# show
input_plot
# time to get plotting
fig, ax = plt.subplots()
plt.bar(input_plot['NumberFacilities'], input_plot['Occurence'])
plt.locator_params(axis='x', nbins=len(input_plot))
plt.xlabel('Number of facilities offered at the station')
plt.ylabel('Number stations offering this amount of facilities')
plt.show()

# import packages
import geopandas as gpd
# read in file in geopandas data structure
map_df = gpd.read_file('../Data/BELGIUM_-_Provinces/BELGIUM_-_Provinces.shp')

#show
map_df.head()
# show
map_df.plot()
# check unique province names in map_df
map_df["NE_Name"].unique()
# load self created excel file regarding inhabitant data (source: statbel)
inh_df = pd.read_excel('../data/inhabitants_prov.xlsx')
# show
inh_df.head()
# change column to the same name and then merge both tables
inh_df = inh_df.rename(index=str, columns={'Province': 'NE_Name'})

# merge
map_df = map_df.merge(inh_df, on='NE_Name')

# show
map_df.head()
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))

# use cmap = 'BuGn' to get nice color-shaded plot
map_df.plot(column='Inhabitants', cmap='BuGn', linewidth=0.8, ax=ax)
# dictionary with location of Belgian universities
data = {'Name':  ['Ugent', 'KULeuven', 'VUB'],
        'lat': [51.046672, 50.877833, 50.822476],
        'lon': [3.727708, 4.700250, 4.394807]}

# create data frame
data_df = pd.DataFrame(data, columns = ['Name', 'lat', 'lon'])

# plot
data_df.plot('lon', 'lat', 'scatter',  color='red')
# overlap with our map
ax = data_df.plot('lon', 'lat', 'scatter',  color='red', zorder=2)
map_df.plot(column='Inhabitants', cmap='BuGn', linewidth=0.8, ax = ax, zorder = 1)

