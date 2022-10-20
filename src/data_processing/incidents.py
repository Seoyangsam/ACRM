import data
import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

# Change date of the incident to datetime
if not is_datetime(data.incidents["Date of the incident"]):
    data.incidents["Date of the incident"] = pd.to_datetime(data.incidents["Date of the incident"].astype(str),
                                                            format='%d/%m/%y')
# Remove month, since Date of the incidents already captures the month + extra info(day)
data.incidents = data.incidents.drop("Month", axis =1);

# General number of delay and cancellation incidents
frequency_trips = data.full_trips["Name of the stop"].value_counts()
data.travelers["sum"] = data.travelers["week"] + data.travelers["saturday"] + data.travelers["sunday"]
frequency_travelers = data.travelers[["Station", "sum"]].sort_values(by = ["sum"], ascending = False)
