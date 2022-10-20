import data
import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

# URI imputation to only get the digits
data.stations['URI'] = data.stations['URI'].str[-9:]

# Drop row if country code not "be"
data.stations = data.stations[data.stations["country-code"] == "be"]

# drop the 4 alternative name columns
data.stations = data.stations.drop(["alternative-fr", "alternative-nl", "alternative-de", "alternative-en"], axis=1)

# drop rows that have 0 for official transfer time: they aren't stations anymore
data.stations = data.stations.dropna(subset=["official_transfer_time"])

