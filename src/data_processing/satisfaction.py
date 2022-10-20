import data
import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

#drop the rows that have null values
data.satisfaction.dropna(inplace=True)



