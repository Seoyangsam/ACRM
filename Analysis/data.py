import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns
import os

####################   LOAD IN DATA  ####################

# This file describes facilities available in NMBS/SNCB stations.
facilities = pd.read_csv("../group7-group-assignment-/Data/facilities.csv")
# check number of missing values per variable
for col in facilities.columns:
    missings = len(facilities[col][facilities[col].isnull()]) / float(len(facilities))
    print(col, missings)

facilities['sales_open_monday2'] = pd.to_datetime(facilities['sales_open_monday'].astype(str), format='%H:%M')-pd.to_datetime('00:00', format='%H:%M')
# for instance only use subset of 'late openers'
late_openers = facilities[facilities['sales_open_monday2'] < pd.Timedelta(8,'h')]

# or use it to impute missing values
facilities['sales_open_monday2'].fillna((facilities['sales_open_monday2'].mean()), inplace=True)

# check number of missing values per variable
for col in facilities.columns:
    missings = len(facilities[col][facilities[col].isnull()]) / float(len(facilities))
    print(col, missings)


# This file describes all the type of incidents that happened with the resulting delays and cancellations.
incidents = pd.read_csv("../group7-group-assignment-/Data/incidents.csv")

# This file describes the average satisfaction score for each station.
satisfaction = pd.read_csv("../group7-group-assignment-/Data/satisfaction.csv")

# This file describes all NMBS/SNCB stations in Belgium.
# A station can have multiple platforms (stops), which are described in stops.csv.
stations = pd.read_csv("../group7-group-assignment-/Data/stations.csv")

# This file describes all NMBS/SNCB stops in Belgium.
# Each platform is a separate stop location.
stops = pd.read_csv("../group7-group-assignment-/Data/stops.csv")

# This file describes the average number of travelers per station. URI: The URI identifying this station.
travelers = pd.read_excel("../group7-group-assignment-/Data/travelers.xlsx", skiprows=1)
travelers.head(5)
# rename
travelers = travelers.rename({"Avg number of travelers in the week": "week",
                              "Avg number of travelers on Saturday": "saturday",
                              "Avg number of travelers on Sunday": "sunday"}, axis=1)

# check number of missing values per variable
for col in travelers.columns:
    missings = len(travelers[col][travelers[col].isnull()]) / float(len(travelers))
    print(col, missings)

# check missings
# change settings to visualize ALL rows
pd.set_option('display.max_rows', None)
print(travelers[travelers.isnull().any(axis=1)])

# change settings back
pd.reset_option('display.max_rows')

# Interesting: never completely missing
# Inspection Wikipedia and NMBS website revealed no train rides on these dates for these stations (e.g., Baasrode-Zuid & Buda only train rides during the week)
# Therefore we impute every missing value with zero

travelers['week'].fillna(0, inplace=True)
travelers['saturday'].fillna(0, inplace=True)
travelers['sunday'].fillna(0, inplace=True)

# create total
travelers["week_total"] = 5 * travelers["week"] + travelers["saturday"] + travelers["sunday"]

# get weekend avg
travelers["weekend"] = (travelers["sunday"] + travelers["saturday"]) / float(2)

# get avg travelers per day
travelers["avg_day"] = travelers["week_total"] / float(7)

# check top 5 stations with highest number of travelers during the weekend
travelers.sort_values(by="week", ascending=False)[["Station", "week"]].head(5)

# check top 5 stations with highest number of travelers during the week
travelers.sort_values(by="weekend", ascending=False)[["Station", "weekend"]].head(5)

# Most remarkable differences are between Brussels Midi and Brussels North. North is in the middle of business centre ==> attracts many commuters during the week while Brussels Midi is the most important international railway station of Belgium and thus attracts many tourists. Also notice how Antwerpen and Leuven almost have equal travellers during the week and are off by almost a factor two during the weekend. This could signify a more or less equal commute potential but a far greater touristic potential for Antwerp. However, both are edjucated guesses based on my personal knowledge about the country. Implementing this mathematical and on a larger scale requires external data!

# Other explanations for the commute numbers may possible lay in the number of facilities. As a proof of concept, let's try to mathematically proof whether weekly commute numbers are linked to availabilty of free parking and/or tram stations nearby. To do so, we will link the facilities and travelers datasets. We will impute missing values of free parking and tram with these facilities not being available. However, do note that this is not necessarily the best assumption!

# impute columns with zero values
facilities['free_parking'].fillna(0, inplace=True)
facilities['tram'].fillna(0, inplace=True)

# In[55]:


facilities.shape

# In[56]:


travelers.shape

# In[57]:


# PROBLEM: no exact match in traveler/facilities information
# ASSUMPTION: travelers is subset of facilities

# convert to lower case
facilities['name'] = facilities['name'].str.lower()
travelers['Station'] = travelers['Station'].str.lower()

# check overlap
len(list(set(facilities['name']).intersection(set(travelers['Station']))))

# around 80 which will need manual imputation
intersection = list(set(facilities['name']).intersection(set(travelers['Station'])))

still_needed = set(travelers['Station']).difference(intersection)

len(still_needed)

still_needed

facility_names = set(facilities['name']).difference(intersection)

facility_names

# The facilities dateset also includes international stations, more small stations and different names for the stations with bilingual names or more complicated names. We will have to impute these manually. I will do some, but you will have to create a dictionary of all linked names in order to impute those names.

# dictionary with correct names
Dict = dict({'antwerpen-caal': 'antwerpen-centraal',
             'arcades': 'arcaden/arcades',
             'beignee': 'beignée',
             'berchem-st-ag.-berchem': 'sint-agatha-berchem/berchem-sainte-agathe'})

# replace names
travelers = travelers.replace({"Station": Dict})

# check if overlap +4 (previously overlap = 473)
len(list(set(facilities['name']).intersection(set(travelers['Station']))))

# Overlap has increased by four. These four are the four stations I have mapped out.

# Let's assume we have imputed all station names. Now we can merge the two datasets and run an analysis to see whether tram and free parking availability correlate to the number of travelers on a weekday. Do note that the relationship can be bi-directional. People can be inclined to use stations with connection to trams, but public transport companies can also be more likely to link their network with popular train stations.


# first merge
merge = pd.merge(facilities, travelers, left_on='name', right_on='Station')

# check if all were matched
merge.shape

# To perform a multivariate regression, we will use the statsmodels package. Note that sklearn (which you will use later on in the course) also has an implementation of the model. However, sklearn focuses more on predictive performance (how good you can predict something) instead of statistical inference. Since we are interested whether relationships are significant, we will use statsmodels in this case

import statsmodels.api as sm

# run multivariate regression
X = merge[['tram', 'free_parking']]
Y = merge['week']
X = sm.add_constant(
    X)  # adding a constant: Y = beta0 + beta1*X1 + beta2*X2 + espilon instead of Y = beta1*X1 + beta2*X2 + epsilon

model = sm.OLS(Y, X).fit()
print_model = model.summary()

# show results of regression
print_model


# This directory contains files that each describe the information on train trips on a certain day
data_dir = "../group7-group-assignment-/Data/Trips"
os.listdir(data_dir)
all_trips = [obs for obs in os.listdir(data_dir) if ".DS" not in obs]
full_trips = pd.DataFrame()
print(full_trips.shape)

for trip in all_trips:
    # import
    df = pd.read_csv(os.path.join(data_dir, trip), sep=",")
    full_trips = full_trips.append(df)
    print(full_trips.shape)

