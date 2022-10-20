import pandas as pd
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

# Full_trips is all the train trips
all_trips = [obs for obs in os.listdir("../../Data/Unprocessed/Trips/") if ".DS" not in obs]
full_trips = pd.DataFrame()
for trip in all_trips:
    df = pd.read_csv(os.path.join("../../Data/Unprocessed/Trips/", trip), sep=",")
    full_trips = full_trips.append(df)


