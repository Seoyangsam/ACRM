import data
import numpy as np
import pandas as pd
import src.utils as utils
from pandas.api.types import is_datetime64_any_dtype as is_datetime

#impute the URI
data.facilities['URI'] = data.facilities['URI'].str[-9:]

# Change disabled parking spots to dummy indicator
data.facilities['disabled_parking_spots'] = np.where(data.facilities['disabled_parking_spots'] == 0, 0, 1)


#Assumption that null values mean that the facilities are not available.
# So we impute null values with 0
facil_col = ['ticket_vending_machine', 'luggage_lockers', 'free_parking', 'taxi', 'bicycle_spots', 'blue-bike',
             'bus', 'tram', 'metro', 'wheelchair_available', 'ramp', 'disabled_parking_spots', 'elevated_platform',
             'escalator_up', 'escalator_down', 'elevator_platform', 'audio_induction_loop']

for col in facil_col:
    data.facilities[col].fillna((0), inplace=True)

# If street, zip and city are null, then the station is not from Belgium, so we can drop it
data.facilities = data.facilities.dropna(axis=0, subset=["street", "zip", "city"])


# Stations that do not have openinghours (null values), simply don't have a 'building'
# We change those null values to 00:00 , interpreted as opening and closing at 00:00 so no opening time , (NOT opened 24/7)
facility_openinghours=['sales_open_monday', 'sales_close_monday', 'sales_open_tuesday',
       'sales_close_tuesday', 'sales_open_wednesday', 'sales_close_wednesday',
       'sales_open_thursday', 'sales_close_thursday', 'sales_open_friday',
       'sales_close_friday', 'sales_open_saturday', 'sales_close_saturday',
       'sales_open_sunday', 'sales_close_sunday']
for col in facility_openinghours:
    data.facilities[col] = data.facilities[col].fillna("00:00")

# Change all opening and closing times to datetime
for fac_time in data.facilities[facility_openinghours]:
    if not is_datetime(data.facilities[fac_time]):
        data.facilities[fac_time] = pd.to_datetime(data.facilities[fac_time].astype(str), format='%H:%M')-pd.to_datetime('00:00', format='%H:%M')


# Standardize name for facilities, we might have to do this for other ones too.So beware
    data.facilities['name'] = data.facilities['name'].str.lower()

