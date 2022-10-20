import data
import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

# Impute name and URI, we dont need to keep the # of URI because we store the same number in platform
data.stops['URI'] = data.stops['URI'].str[-9:]
data.stops['parent_stop'] = data.stops['parent_stop'].str[-9:]

# Drop the name columns
data.stops = data.stops.drop(["alternative-fr", "alternative-nl", "alternative-de", "alternative-en"], axis =1)
