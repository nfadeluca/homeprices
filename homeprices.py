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

file_path = 'C:/Users/nfade/Documents/GitHub/homeprices/map/tl_2019_us_zcta510.shx'
map_us = gpd.read_file(file_path)

'''
ZCTA5CE10       object
GEOID10         object
CLASSFP10       object
MTFCC10         object
FUNCSTAT10      object
ALAND10          int64
AWATER10         int64
INTPTLAT10      object
INTPTLON10      object
geometry      geometry
'''


fig, ax = plt.subplots(1, figsize=(15, 8))
plt.title('Map of the United States Sub-Regions', size=16)
map_us[(map_us['ALAND10']) & (map_us['ALAND10'])].plot(column='ZCTA5CE10',                                                    
             cmap='Greens',      # Colormap for the states                     
             linewidth=0.4,      # line width for state borders
             ax=ax,              # plotting the map on 'ax'
             edgecolor='black'); # State border colors