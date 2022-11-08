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
# for trip_time in data.full_trips[trips_times]:
#     if not is_datetime(data.full_trips[trip_time]):
#         data.facilities[trip_time] = pd.to_datetime(data.facilities[trip_time].astype(str), format='%H:%M:%S')-pd.to_datetime('00:00', format='%H:%M:%S')
