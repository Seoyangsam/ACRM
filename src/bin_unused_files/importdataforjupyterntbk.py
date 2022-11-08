import pandas as pd
from pathlib import Path


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
travelers = pd.read_excel(path / "travelers.xlsx", skiprows=1)
travelers = travelers.rename({"Avg number of travelers in the week": "week",
                              "Avg number of travelers on Saturday": "saturday",
                              "Avg number of travelers on Sunday": "sunday"}, axis=1)

# This file describes all the trips that happened in the NMBS/SNCB network.
full_trips = pd.concat([pd.read_csv(path, sep=",") for path in (path / "Trips/").glob('*.csv')], axis=0)


# funcion to get union of travelers['station'] and incidents['station'] to lower case
def get_union_of_stations():
    # get union of travelers['station'] and incidents['station'] to lower case
    union_of_stations = set(travelers['station'].str.lower().unique()).union(set(incidents['station'].str.lower().unique()))
    return union_of_stations

# get sum of "Number of minutes of delay" for each "Place" in incidents
def get_sum_of_delay_per_place():
    sum_of_delay_per_place = incidents.groupby('Place')['Number of minutes of delay'].sum()
    return sum_of_delay_per_place
