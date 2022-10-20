import data
import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime

# Change all dates and times to datetime STILL NEEDS TO BE CHECKED
# trips_dates= ["Date of departure", 'Date of planned arrival',
#        'Date of planned departure', 'Date of real arrival',
#        'Date of real departure']
# trips_times = ['Time of real arrival',
#        'Time of real departure', 'Time of planned arrival',
#        'Time of planned departure']
#

data.full_trips['Time of real arrival'] = pd.to_datetime(data.full_trips['Time of real arrival'])
data.full_trips['Time of planned arrival'] = pd.to_datetime(data.full_trips['Time of planned arrival'])
data.full_trips['Time of real departure'] = pd.to_datetime(data.full_trips['Time of real departure'])
data.full_trips['Time of planned departure'] = pd.to_datetime(data.full_trips['Time of planned departure'])

# define function to get delay
def get_delay(expected, real):
    if real > expected:
        delay = (real-expected).seconds
    else:
        delay = None
    return delay

data.full_trips['Delay time'] = data.full_trips.apply(lambda obs: get_delay(obs['Time of planned arrival'], obs['Time of real arrival']), axis = 1)
print(data.full_trips['Delay time'].head(5))