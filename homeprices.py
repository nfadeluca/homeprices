#!/usr/bin/env python
import quandl
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import geopandas as gpd
from shapely import wkt


"""
This method reads the Zillow data file and then outputs a csv file containing
only the home price data for a certain month and type of home
@:returns Returns the unsorted but filtered dataframe
"""
def pullDataSubset():
    print("Opening up")
    df = pd.read_csv("ZILLOW_DATA.csv")
    #The date here is the date that will be outputted
    df = df.copy()[df['date'] == '2020-01-31']
    #index = False gets rid of the first column
    df.to_csv("ZILLOW_JAN.csv", index = False)
    df = df.copy()[df['indicator_id'] == 'ZSFH']
    df.to_csv("ZILLOW_ZSFH.csv", index = False)

def cleanRegionsMethod():
    final = []
    with open('ZILLOW_REGIONS.csv') as f:
        lines = f.readlines()
        with open('ZILLOW_REGIONS.csv', 'w') as g:
            for line in lines:
                if 'zip' in line:
                    g.write(line)
    with open('ZILLOW_REGIONS.csv') as h:
        lines = h.readlines()
        for line in lines:
            line = line.split(',')
            for item in line:
                if item == 'zip': line.remove('zip')
            line = ','.join(line)
            line = line.split(';')
            final.append(line[0])
    with open('ZILLOW_REGIONS.csv', 'w') as j:
        for item in final:
            item = item.strip('\n')
            j.write(str(item))
            j.write('\n')

def addZipCodes():
    df = pd.read_csv("ZILLOW_TEST.csv")
    df['zip_code'] = df['region_id'].apply(getZipCode)
    print("Done!")
    df.to_csv("ZILLOW_TEST.csv", index = False)
"""
This helper method takes a region ID and returns the corresponding zip code.
Sets the default zip code to 0, and only searches for the zip code in the regions lookup
@:param The zillow region ID
@:returns The zip code for the region
"""
def getZipCode(region_id):
    regions = pd.read_csv("ZILLOW_REGIONS.csv")
    print(region_id)
    zipCode = "None"
    if region_id in regions['region_id'].unique():
        print("FOUND!!!")
        zipCode = regions.at[[regions['region_id'] == region_id].index.values, 'region']
        print(zipCode)
    return zipCode

addZipCodes()
"""
This method sorts the data and returns it
@:returns The sorted dataframe
"""
def sortData():
    df = pd.read_csv("ZILLOW_REGIONS.csv")
    df['region_id'] = pd.to_numeric(df['region_id'], errors='coerce')
    df = df.sort_values(by='region_id')
    df.to_csv("ZILLOW_REGIONS.csv", index = False)
    return df.astype(int)
#Show the histogram of data
#sortData()['value'].plot(kind='hist', bins=100, grid=True, range=[0, 1000000])
#plt.show()

'''
activate myenv to work with conda (for nick on visual studio)
#Max file location: 
C:/Users/Max/PycharmProjects/homeprices/map/tl_2019_us_zcta510.shx
#Nick:
C:/Users/nfade/Documents/GitHub/homeprices/map/tl_2019_us_zcta510.shx

'''

# map_us = gpd.read_file('C:/Users/Max/PycharmProjects/homeprices/map/tl_2019_us_zcta510.shx')

'''
ZCTA5CE10       object  2010 Census 5-digit ZIP Code Tabulation Area code
GEOID10         object  2010 Census 5-digit ZIP Code Tabulation Area code
CLASSFP10       object  2010 Census FIPS 55 class code
MTFCC10         object  MAF/TIGER feature class code (G6350)
FUNCSTAT10      object  2010 Census functional status
ALAND10          int64  2010 Census land area
AWATER10         int64  2010 Census water area
INTPTLAT10      object  2010 Census latitude of the internal point
INTPTLON10      object  2010 Census longitude of the internal point
geometry      geometry
'''

# merged_map_df = pd.merge(map_us, sortData(), on='state')
# map_us.plot('GEOID10', figsize=(12,8), cmap=plt.cm.Greens)
# print(map_us.head())

#addZipCodes()
# print(getZipCode(96817))