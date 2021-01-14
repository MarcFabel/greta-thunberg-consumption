#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 14:14:57 2020

@author: marcfabel

Description: 
    obtain long & lat from strikes obtained from facebook and instagram

Inputs:
    fff_strikes_biggest_cities_social_media.xlsx        [source]
    

Outputs:

"""

# packages
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


# HOME directories
z_strike_input =            '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/source/fff_strikes/'
z_strike_intermediate =     '/Users/marcfabel/Dropbox/greta_cons_Dx/analysis/data/intermediate/fff_strikes/'
z_prefix =                  'greta_cons_'



###############################################################################
#           Read in Data
###############################################################################
strikes = pd.read_excel(z_strike_input + 'fff_strikes_biggest_cities_social_media.xlsx')


# replace nan strings with space
strikes['plz'].fillna('', inplace=True)


### geocode addresses


# drop duplicates
locations = strikes[['state', 'plz', 'municipality', 'location']].drop_duplicates()


# create adress column
locations['address'] = locations['location']+', '+locations['plz']+' '+ locations['municipality']+', '+locations['state']+', '+'Deutschland'


# check for Marienplatz (48.137320, 11.575435)
#locator = Nominatim(user_agent='myGeocoder')
#location = locator.geocode('Marienplatz, 80331 München, Bayern, Deutschland')
#print('Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude))





### Geocoding
locator = Nominatim(user_agent='myGeocoder')

# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
# 2- - create location column
locations['location2'] = locations['address'].apply(geocode)
# 3 - create longitude, laatitude and altitude from location column (returns tuple)
locations['point'] = locations['location2'].apply(lambda loc: tuple(loc.point) if loc else None)
# 4 - split point column into latitude, longitude and altitude columns
locations[['latitude', 'longitude', 'altitude']] = pd.DataFrame(locations['point'].tolist(), index=locations.index)



### Manual replacement where program did not deliver longitude & latitude (nans are replaced)
locations.loc[locations['address'] == 'Am Alten Markt 1, 14467 Potsdam, Berlin, Deutschland', ['latitude', 'longitude']] = 52.395137, 13.060613
locations.loc[locations['address'] == 'St Pauli (U-Bahn Station), 20359 Hamburg, Hamburg, Deutschland', ['latitude', 'longitude']] = 53.551133, 9.970232
locations.loc[locations['address'] == 'Königsstrasse 48, 47051 Duisburg, Nordrhein-Westfalen, Deutschland', ['latitude', 'longitude']] = 51.432888, 6.768693
locations.loc[locations['address'] == 'Universitätsstraße 150, 44801 Bochum, Nordrhein-Westfalen, Deutschland', ['latitude', 'longitude']] = 51.444380, 7.261103
#locations.loc[locations['address'] == '', ['latitude', 'longitude']] = 



locations = locations[['state', 'plz', 'municipality', 'location', 'latitude', 'longitude']]



# merge back with original data frame
strikes = strikes.merge(locations, on=['state', 'plz', 'municipality', 'location'])


# export
strikes.to_csv(z_strike_intermediate + z_prefix + 'fff_strikes_biggest_cities_social_media_geocoordinates.csv', sep=';', encoding='UTF-8', index=False)







