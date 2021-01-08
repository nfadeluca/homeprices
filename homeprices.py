#!/usr/bin/env python
import quandl
import matplotlib.pyplot as plt
import pandas as pd
import numpy
import geopandas as gpd 


# Making use of Zillow data
"""
This method reads the Zillow data file and then outputs a csv file containing
only the home price data for a certain month and type of home
@:returns Returns the unsorted but filtered dataframe
"""
def pullDataSubset():
    print("Reading file")
    df = pd.read_csv("ZILLOW_DATA.csv")
    print("File loaded!")
    #The date here is the date that will be outputted
    df = df.copy()[df['date'] == '2020-01-31']
    #index = False gets rid of the first column
    df.to_csv("ZILLOW_JAN.csv", index = False)
    print("File copied!")
    df = df.copy()[df['indicator_id'] == 'ZATT']
    df.to_csv("ZILLOW_ZATT.csv", index = False)
    print("File copied!")
    return df


"""
This method sorts the data and returns it
@:returns The sorted dataframe
"""
def sortData():
    df = pd.read_csv("ZILLOW_ZATT.csv")
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.sort_values(by='value')
    return df

#sortData()['value'].plot(kind='hist', bins=100, grid=True, range=[0, 1000000])
#plt.show()

'''
activate myenv to work with conda (for nick on visual studio)
'''

map_us = gpd.read_file('C:/Users/nfade/Documents/GitHub/homeprices/map/tl_2019_us_zcta510.shx')

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

print(map_us.head())