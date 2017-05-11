import pandas as pd
from ast import literal_eval as make_tuple
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError
import matplotlib.pyplot as plt

dist = 2 #radius that defines closeness of housing to whatever amenity

housing_df = pd.read_csv('/Users/bihuili/Downloads/New_Housing_Units_Permitted.csv')
print len(housing_df)
housing_df = housing_df[housing_df['Permit Sub-Type'] == '1 or 2 Family Dwelling']
print len(housing_df)



#housing_df['val_float'] = housing_df['Valuation'].apply(convert_money)
    
housing_df = housing_df.dropna(subset = ['Latitude/Longitude', 'Valuation'])

cult_df = pd.read_csv('/Users/bihuili/Downloads/Historic___Cultural_Resources_2015.csv')

cult_df = cult_df.dropna(subset = ['Location 1'])

#write function for cult_df to read in 'Location 1' column such that:
#if lat/long exist, use them
#if not, take entire address and run in geopy to obtain lat/long
def conv_loc1(entry):
    if entry[-1] == ")":
        coords = entry[entry.find("("):entry.find(")")+1]
        tple = make_tuple(coords)
        return tple
    else:
        geolocator = Nominatim()
        try:
            location = geolocator.geocode(entry)
            return (location.latitude, location.longitude)
        except AttributeError:
            return (0,0)
        except GeocoderTimedOut as e:
            print e
            return (0,0)
        except GeocoderServiceError as e:
            print e
            return (0,0)
        
housing_df['lat_long'] = housing_df['Latitude/Longitude'].apply(conv_loc1)
housing_df = housing_df.dropna(subset = ['lat_long'])

cult_df['lat_long'] = cult_df['Location 1'].apply(conv_loc1)
print len(cult_df)
cult_df = cult_df[cult_df['Location 1'] != (0,0)]
print len(cult_df)

#for each tple representing lat/long of new house, return # of cultural institutions within dist radius            
def num_cult(tple, dist):
    count = 0
    for i in range(len(cult_df)):
        if great_circle(cult_df.iloc[i]['lat_long'],tple).miles < dist:
            count +=1
    print count
    return count

housing_df['cult_count'] = housing_df['lat_long'].apply(lambda x: num_cult(x, dist))

housing_df.to_csv('new_housing_processed.csv', index=False)

#housing_df = housing_df.astype(float)
plt.scatter(housing_df['cult_count'], housing_df['Valuation'])
plt.show()


