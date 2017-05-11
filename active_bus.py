import pandas as pd
from ast import literal_eval as make_tuple
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError
import matplotlib.pyplot as plt

dist = 0.5 #radius that defines closeness of housing to whatever amenity

housing_df = pd.read_csv('new_housing_processed.csv')

def convert_money(value):
    return float(value[1:])

housing_df['value'] = housing_df['Valuation'].apply(convert_money)

housing_df = housing_df[housing_df['value'] < 2000000] #restrict to houses<2mil
    
biz_df = pd.read_csv('/Users/bihuili/Downloads/Listing_of_Active_Businesses.csv')

biz_df = biz_df.dropna(subset = ['LOCATION'])
print len(biz_df)
#filter for type of business
#biz_df = biz_df[biz_df['PRIMARY NAICS DESCRIPTION'] =='Educational services (including schools, colleges, & universities)']
biz_df = biz_df[biz_df['PRIMARY NAICS DESCRIPTION'] =='Grocery stores (including supermarkets & convenience stores without gas)']
#biz_df = biz_df[biz_df['PRIMARY NAICS DESCRIPTION'] =='Independent artists, writers, & performers']
print len(biz_df)


def compare(tple_str, tple, dist): #tple_str is in string form
    tple2 = make_tuple(tple_str)
    if great_circle(tple2, tple).miles<dist:
        return 1
    else:
        return 0
#for each tple representing lat/long of new house, return # of cultural institutions within dist radius      
def num_cult(tple, dist):
    ## for i in range(len(biz_df)):
    ##     if great_circle(make_tuple(biz_df.iloc[i]['LOCATION']),tple).miles < dist:
    ##         count +=1
    biz_df['close_or_not'] = biz_df['LOCATION'].apply(lambda x: compare(x, tple, dist))
    count = biz_df['close_or_not'].sum(axis=0)
    print count
    return count

housing_df['biz_count'] = housing_df['lat_long'].apply(lambda x: num_cult(x, dist))

housing_df.to_csv('groc_05_new_housing_processed.csv', index=False)

#housing_df = housing_df.astype(float)
plt.scatter(housing_df['biz_count'], housing_df['value'])
plt.show()


