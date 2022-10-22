#from Analysis.data import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.pylabtools import figsize


import pandas as pd
import matplotlib.pyplot as plt

#vraag3: Plot the number of stations per city for cities with multiple stations.

geg = pd.read_csv(r'C:\users\Annelien\Documents\SCHOOL\ACRM\Project NMBS\group7-group-assignment-\Data\facilities.csv', sep=',')
df = pd.DataFrame(geg)
df2 = df.groupby('city').size().reset_index(name='count') # head(5)dan toon je maar 5lijnen, eruit halen op termijn
#groepeer per city en geef de lengte hier mee
#resetindex = maak nieuwe kolom aan en noem die count
# df2 = count > 1
print(df2)
df2 = df2[df2["count"] > 1 ]

plt.bar(df2['city'], df2['count'], color='r')
plt.xlabel("city")
plt.ylabel("number of stations")
plt.legend(loc="upper left")
plt.xticks(rotation= "vertical")
plt.show()









