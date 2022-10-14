import numpy as np
import pandas as pd
import matplotlib as plt
import seaborn as sns
import os

####################   LOAD IN DATA  ####################

# This file describes facilities available in NMBS/SNCB stations.
facilities = pd.read_csv("../Data/facilities.csv")



# This file describes all the type of incidents that happened with the resulting delays and cancellations.
incidents = pd.read_csv("../Data/incidents.csv")

# This file describes the average satisfaction score for each station.
satisfaction = pd.read_csv("../Data/satisfaction.csv")

# This file describes all NMBS/SNCB stations in Belgium.
# A station can have multiple platforms (stops), which are described in stops.csv.
stations = pd.read_csv("../Data/stations.csv")

# This file describes all NMBS/SNCB stops in Belgium.
# Each platform is a separate stop location.
stops = pd.read_csv("../Data/stops.csv")

# This file describes the average number of travelers per station. URI: The URI identifying this station.
travelers_xlsx = pd.read_excel("../Data/travelers.xlsx", skiprows=1)

# This directory contains files that each describe the information on train trips on a certain day
trips_dir = "../Data/Trips/"
all_trips = [obs for obs in os.listdir(trips_dir) if ".DS" not in obs]
