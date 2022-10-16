# import packages
import numpy as np
import pandas as pd
import os

# Prepare Trips Data

# define dir
data_dir = "../Data/Trips"

os.listdir(data_dir)

# get all the infrabel trip files
all_trips = [obs for obs in os.listdir(data_dir) if ".DS" not in obs]
all_trips
full_trips = pd.DataFrame()
print(full_trips.shape)

for trip in all_trips:
    # import
    df = pd.read_csv(os.path.join(data_dir, trip), sep=",")
    full_trips = full_trips.append(df)
    print(full_trips.shape)

#Import Data Facilities
# import facilities
facilities = pd.read_csv("../data/facilities.csv")
# check
facilities.head(5)
# check number of missing values per variable
for col in facilities.columns:
    missings = len(facilities[col][facilities[col].isnull()]) / float(len(facilities))
    print(col, missings)
# Check data type of columns
facilities.dtypes
facilities['sales_open_monday2'] = pd.to_datetime(facilities['sales_open_monday'].astype(str),
                                                  format='%H:%M') - pd.to_datetime('00:00', format='%H:%M')
# see new column is of type timedelta64
facilities.dtypes
# for instance only use subset of 'late openers'
late_openers = facilities[facilities['sales_open_monday2'] > pd.Timedelta(8, 'h')]
late_openers['sales_open_monday']
# or use it to impute missing values
facilities['sales_open_monday2'].fillna((facilities['sales_open_monday2'].mean()), inplace=True)
# check number of missing values per variable
for col in facilities.columns:
    missings = len(facilities[col][facilities[col].isnull()]) / float(len(facilities))
    print(col, missings)

#Travelers
# import data
travelers = pd.read_excel("../data/travelers.xlsx", header=1, index_col=0)
# check
travelers.head(5)
# rename
travelers = travelers.rename({"Avg number of travelers in the week": "week",
                              "Avg number of travelers on Saturday": "saturday",
                              "Avg number of travelers on Sunday": "sunday"}, axis=1)
# check number of missing values per variable
for col in travelers.columns:
    missings = len(travelers[col][travelers[col].isnull()]) / float(len(travelers))
    print(col, missings)
# check missings
# change settings to visualize ALL rows
pd.set_option('display.max_rows', None)
print(travelers[travelers.isnull().any(axis=1)])

# change settings back
pd.reset_option('display.max_rows')

# Interesting: never completely missing
# Inspection Wikipedia and NMBS website revealed no train rides on these dates for these stations (e.g., Baasrode-Zuid & Buda only train rides during the week)
# Therefore we impute every missing value with zero

travelers['week'].fillna(0, inplace=True)
travelers['saturday'].fillna(0, inplace=True)
travelers['sunday'].fillna(0, inplace=True)
# create total
travelers["week_total"] = 5 * travelers["week"] + travelers["saturday"] + travelers["sunday"]
# get weekend avg
travelers["weekend"] = (travelers["sunday"] + travelers["saturday"]) / float(2)
# get avg travelers per day
travelers["avg_day"] = travelers["week_total"] / float(7)
# check top 5 stations with highest number of travelers during the weekend
travelers.sort_values(by="week", ascending=False)[["Station", "week"]].head(5)
# check top 5 stations with highest number of travelers during the week
travelers.sort_values(by="weekend", ascending=False)[["Station", "weekend"]].head(5)



# impute columns with zero values
facilities['free_parking'].fillna(0, inplace=True)
facilities['tram'].fillna(0, inplace=True)
facilities.shape
travelers.shape
# PROBLEM: no exact match in traveler/facilities information
# ASSUMPTION: travelers is subset of facilities

# convert to lower case
facilities['name'] = facilities['name'].str.lower()
travelers['Station'] = travelers['Station'].str.lower()
# check overlap
len(list(set(facilities['name']).intersection(set(travelers['Station']))))
# around 80 which will need manual imputation
intersection = list(set(facilities['name']).intersection(set(travelers['Station'])))

still_needed = set(travelers['Station']).difference(intersection)
len(still_needed)
still_needed
facility_names = set(facilities['name']).difference(intersection)
facility_names


# dictionary with correct names
Dict = dict({'antwerpen-caal': 'antwerpen-centraal',
             'arcades': 'arcaden/arcades',
             'beignee': 'beignée',
             'berchem-st-ag.-berchem': 'sint-agatha-berchem/berchem-sainte-agathe',
             'berzee' : 'berzée',
             'boitsfort/bosvoorde' : 'bosvoorde/boitsfort',
             'boondael/boondaal' : 'boondaal/boondael',
             'bru. airport - zaventem' : 'brussels airport - zaventem',
             'bru.-cent.' : 'brussel-centraal/bruxelles-central',
             'bru.-chap./kap.' : 'brussel-kapellekerk/bruxelles-chapelle',
             'bru.-cong.' : 'brussel-congres/bruxelles-congrès',
             'bru.-luxembg' : 'brussel-luxemburg/bruxelles-luxembourg',
             'bru.-midi/zuid' : 'brussel-zuid/bruxelles-midi',
             'bru.-noord/nord' : 'brussel-noord/bruxelles-nord',
             'bru.-schuman' : 'brussel-schuman/bruxelles-schuman',
             'bru.-west/ouest' : 'brussel-west/bruxelles-ouest',
             'chateau-de-seilles' : 'château-de-seilles',
             'chatelet' : 'châtelet',
             'chenee' : 'chênée',
             'comines/komen' : 'comines',
             'courriere' : 'courrière',
             'court-saint-etienne' : 'court-saint-étienne',
             'ecaussinnes' : 'écaussinnes',
             'enghien/edingen' : 'enghien',
             'erbisoeul' : 'erbisœul',
             'fexhe-le-ht-clocher':'fexhe-le-haut-clocher',
             'forest-est/vorst-oost' : 'vorst-oost/forest-est',
             'forest-midi/vorst-zuid' :'vorst-zuid/forest-midi',
             'forrieres' : 'forrières',
             'franiere' : 'franière',
             'germoir/mouterij' : 'mouterij/germoir',
             'haren-zuid/sud' : 'haren-sud/haren-zuid',
             'haute-flone' : 'haute-flône',
             'hennuyeres' : 'hennuyères',
             'jurbise' : 'jurbeke',
             'la louviere-centre' : 'la louvière-centre',
             'la louviere-sud' : 'la louvière-sud',
             'la roche' : 'la roche (brabant)',
             'labuissiere' : 'labuissière',
             'lessines' : 'lessen',
             'liege-carre' : 'liège-carré',
             'liege-guillemins' : 'liège-guillemins',
             'liege-saint-lambert' : 'liège-saint-lambert',
             'lonzee' : 'lonzée',
             'marche-lez-ecaussinnes' : 'marche-lez-écaussinnes',
             'mery' : 'méry',
             'mortsel-oude-god' : 'mortsel-oude god',
             'mouscron/moeskroen' : 'mouscron',
             'nameche' : 'namêche',
             'neufchateau' : 'neufchâteau',
             'ougree' : 'ougrée',
             'papignies' : 'papegem',
             'pecrot' : 'pécrot',
             'pepinster-cite' : 'pepinster-cité',
             'peruwelz' : 'péruwelz',
             'pieton' : 'piéton',
             'pont-a-celles' : 'pont-à-celles',
             'ronse/renaix' : 'ronse',
             'ruisbr.-sauvegarde' : 'ruisbroek-sauvegarde',
             'spa-geronstere' : 'spa-géronstère',
             'st-denijs-boekel' : 'sint-denijs-boekel',
             'st-denis-bovesse' : 'saint-denis-bovesse',
             'st-gen-rode/rhode-st-gen' : 'sint-genesius-rode',
             'st-ghislain' : 'saint-ghislain',
             'st-gillis' : 'sint-gillis-dendermonde',
             'st-job' : 'sint-job',
             'st-joris-weert' : 'sint-joris-weert',
             'st-katelijne-waver' : 'sint-katelijne-waver',
             'st-mariaburg' : 'sint-mariaburg',
             'st-martens-bodegem' : 'sint-martens-bodegem',
             'st-niklaas' : 'sint-niklaas',
             'st-truiden' : 'sint-truiden',
             'tour et taxis/thurn en taxis' : 'thurn en taxis/tour et taxis',
             'uccle/ukkel-calevoet' : 'ukkel-kalevoet/uccle-calevoet',
             'uccle/ukkel-stalle' : 'ukkel-stalle/uccle-stalle',
             'ville-pommeroeul' : 'ville-pommerœul',
             'vise' : 'visé',
             'vivier d\'oie/diesdelle' : 'diesdelle/vivier d\'oie',
             'watermael/watermaal' : 'watermaal/watermael',
             'yves-gomezee' : 'yves-gomezée'
             })

# replace names
travelers = travelers.replace({"Station": Dict})
# check if overlap +4 (previously overlap = 473)
print(len(list(set(facilities['name']).intersection(set(travelers['Station'])))))
intersection = list(set(facilities['name']).intersection(set(travelers['Station'])))

## now we have changed all names correctly, the travelers stations names overlap completely!
still_needed = set(travelers['Station']).difference(intersection)
print(len(still_needed))
print(still_needed)


# Now we can merge the two datasets and run an analysis to see whether tram and free parking availability correlate to the number of travelers on a weekday.
# Do note that the relationship can be bi-directional. People can be inclined to use stations with connection to trams, but public transport companies can also be more likely to link their network with popular train stations.

# first merge
merge = pd.merge(facilities, travelers, left_on='name', right_on='Station')
# check if all were matched
print(merge.shape)


# only run this code once for installation of the package
# !pip3 install statsmodels
import statsmodels.api as sm

# run multivariate regression
X = merge[['tram', 'free_parking']]
Y = merge['week']
X = sm.add_constant(X)  # adding a constant: Y = beta0 + beta1*X1 + beta2*X2 + espilon instead of Y = beta1*X1 + beta2*X2 + epsilon

model = sm.OLS(Y, X).fit()
print_model = model.summary()
# show results of regression
print(print_model)

