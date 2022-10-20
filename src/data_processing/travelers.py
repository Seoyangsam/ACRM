import data
import src.utils as utils
import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

# Impute missing values with 0: because null value indicates no train rides on that day /week
data.travelers['week'].fillna(0, inplace=True)
data.travelers['saturday'].fillna(0, inplace=True)
data.travelers['sunday'].fillna(0, inplace=True)


# Standardize name for travelers
data.travelers['Station'] = data.travelers['Station'].str.lower()
data.travelers = data.travelers.replace({"Station": utils.Dict})