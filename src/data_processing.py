import pandas as pd
import utils
import data

# Interesting: never completely missing
# Inspection Wikipedia and NMBS website revealed no train rides on these dates for these stations (e.g., Baasrode-Zuid & Buda only train rides during the week)
# Therefore we impute every missing value with zero
data.travelers['week'].fillna(0, inplace=True)
data.travelers['saturday'].fillna(0, inplace=True)
data.travelers['sunday'].fillna(0, inplace=True)


for timing in data.full_trips [['Time of planned arrival', 'Time of planned departure', 'Time of real arrival', 'Time of real departure']]:
    timing = pd.to_timedelta(arg = timing, errors= "coerce")

#clean up facilities df
data.facilities['URI_ID'] = data.facilities['URI'].str[-9:]
print(data.facilities.columns)

# replace names of travelets using the dictionary
travelers = data.travelers.replace({"Station": utils.Dict})