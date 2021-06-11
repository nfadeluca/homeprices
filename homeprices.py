#!/usr/bin/env python
import ntpath
from time import sleep
import zipfile
import os

import quandl
import matplotlib.pyplot as plt
import pandas as pd
#import geopandas as gpd


'''
NOTE:
activate myenv to work with conda (for nick on visual studio)
#Max file location: 
C:/Users/Max/PycharmProjects/homeprices/map/tl_2019_us_zcta510.shx
#Nick:
C:/Users/nfade/Documents/GitHub/homeprices/map/tl_2019_us_zcta510.shx
'''

"""
1. pullDataSubset takes original data file and retrieves specific month
   Also creates ZILLOW_ZSFH which contains indicator_id, region_id, date, and value

2.  cleanRegionsMethod creates new region file from ZILLOW_REGIONS with only
    region and region_id

3. sortHistogram sorts ZILLOW_ZSFH sorts ZILLOW_ZSFH by house value

4. 

"""

def importDataFiles():
    """
    Retrieves DATA and REGIONS zip files from quandl and extracts
    them from their respective zip files. Renames the extracted csv
    files to a more readable name.
    """
    # ApiConfig key from Quandl account, nessecary for using Quandl API here
    quandl.ApiConfig.api_key = 's6x8gXSardesDec_nbyH'

    # Checking if ZILLOW_REGIONS already exists..
    if (os.path.isfile("./ZILLOW_REGIONS.csv")):
        print("ZILLOW_REGIONS already exists!")
    else:
        # Retrieving zipfile
        quandl.export_table('ZILLOW/REGIONS', filename='./ZILLOW_REGIONS.zip')
        # Unzipping the file and getting the CSV
        with zipfile.ZipFile("./ZILLOW_REGIONS.zip", 'r') as zip_ref:
            zip_ref.extractall("./")
        # Removing zipfile and renaming CSV file
        os.remove("ZILLOW_REGIONS.zip")
        os.rename("ZILLOW_REGIONS_1a51d107db038a83ac171d604cb48d5b.csv", "ZILLOW_REGIONS.csv")
    
    # Checking if ZILLOW_DATA already exists..
    if (os.path.isfile("./ZILLOW_DATA.csv")):
        print("ZILLOW_DATA already exists!")
    else:
        # Retrieving zipfile
        quandl.export_table('ZILLOW/DATA', filename='./ZILLOW_DATA.zip')
        # Unzipping the file and getting the CSV
        with zipfile.ZipFile("./ZILLOW_DATA.zip", 'r') as zip_ref:
            zip_ref.extractall("./")
        # Removing zipfile and renaming CSV file
        os.remove("ZILLOW_DATA.zip")
        os.rename("ZILLOW_DATA_962c837a6ccefddddf190101e0bafdaf.csv", "ZILLOW_DATA.csv")
        
importDataFiles()

def createSnapshot(date):
    """
    :param date: The month you wish to pull in format '2020-01-21'
    :return: A CSV file named date.csv
    This is the master function that uses the other helper methods to create a Zillow subset with the
    data for a specific month
    """
    print("Verifying Prerequisite Files:")
    if not ntpath.isfile("ZILLOW_REGIONS_CLEAN.csv"):
        print("ZILLOW_REGIONS_CLEAN.csv not found, generating")
        generateRegions()
    if not ntpath.isfile("ZILLOW_ZSFH.csv"):
        print("ZILLOW_ZSFH.csv not found, generating")
        generateZSFH()
    print("Dependencies verified - opening up data file")
    df = pd.read_csv("ZILLOW_ZSFH.csv")
    #Filter out the other dates in the file
    df = df.copy()[df['date'] == date]
    #index = False gets rid of the first column
    df.to_csv("ZILLOW_"+date+".csv", index = False)
    print("Adding zip codes")
    addZipCodes("ZILLOW_"+date+".csv")
    print("Filtering zip codes")
    filterZipCodes("ZILLOW_"+date+".csv")
    print("Sorting by zip code")
    sortByRegionId("ZILLOW_"+date+".csv")
    print("Finished! ZILLOW_"+date+".csv is complete.")

def generateRegions():
    """
    Creates new ZILLOW_REGIONS csv file that overwrites the old one,
    keeping only region and region_id columns.
    """
    final = []
    df = pd.read_csv("ZILLOW-REGIONS.csv")
    df.to_csv("ZILLOW_REGIONS_CLEAN.csv", index=False)
    # Opens ZILLOW_REGIONS and write only lines with zipcodes
    with open('ZILLOW_REGIONS_CLEAN.csv') as f:
        lines = f.readlines()
        with open('ZILLOW_REGIONS_CLEAN.csv', 'w') as g:
            for line in lines:
                if 'zip' in line:
                    g.write(line)
    # Removing commas and joining newly written lines
    with open('ZILLOW_REGIONS_CLEAN.csv') as h:
        lines = h.readlines()
        for line in lines:
            line = line.split(',')
            for item in line:
                if item == 'zip': line.remove('zip')
            line = ','.join(line)
            line = line.split(';')
            final.append(line[0])
    # Writing zip codes
    with open('ZILLOW_REGIONS_CLEAN.csv', 'w') as j:
        j.write("region,region_id\n")
        for item in final:
            item = item.strip('\n')
            j.write(str(item))
            j.write('\n')

def generateZSFH():
    df = pd.read_csv("ZILLOW_DATA.csv")
    #index = False gets rid of the first column
    df = df.copy()[df['indicator_id'] == 'ZSFH']
    df.to_csv("ZILLOW_ZSFH.csv", index = False)

def addZipCodes(fileName):
    """
    @:param filename: The name of the file to populate with zip codes
    @:returns filename: A modified file containing a new zip codes column
    This function will add a new column to the dataset containing the zip codes
    """
    df = pd.read_csv(fileName)
    global regions
    regions = pd.read_csv("ZILLOW_REGIONS_CLEAN.csv")
    df['zip_code'] = df['region_id'].apply(getZipCode)
    print("Outputting CSV file.")
    print("Found " + str(len(df.index)) + " zip codes!")
    df.to_csv(fileName, index = False)

def getZipCode(region_id):
    """
    @:param The zillow region ID
    @:returns The zip code for the region
    This helper method takes a region ID and returns the corresponding zip code.
    Sets the default zip code to 0, and only searches for the zip code in the regions lookup
    """
    zipCode = "None"
    if region_id in regions['region_id'].unique():
        zipCode = regions.loc[regions.region_id == region_id]
        zipCode = zipCode.iloc[0]['region']
        #print("Zip code found: " + str(zipCode))
    return zipCode

def filterZipCodes(fileName):
    """
    @:param fileName: The file to be processed
    @:returns New CSV file with zipcodes only (ZILLOW_TEST_Filtered)
    This function reads and writes from the TEST File (originally ZSFH) after the zipcode column
    has been added along with all of its zip codes. It filters the file by removing all of the
    "None" values inside of the zipcodes column.
    """
    df = pd.read_csv(fileName)
    df = df[~df.zip_code.str.contains("None")]
    df.drop(['indicator_id', 'date'], axis=1, inplace=True)
    df.to_csv(fileName, index=False)

def sortByRegionId(fileName):
    """
    @:param fileName: The file to process and sort
    @:returns The sorted dataframe
    This method sorts the file by region_id and returns it
    """
    df = pd.read_csv(fileName)
    df['region_id'] = pd.to_numeric(df['region_id'], errors='coerce')
    df = df.sort_values(by='region_id')
    df.to_csv(fileName, index = False)
    return df.astype(int)

# def sortHistogram(fileName):
#     """
#     @:param fileName: The file to sort
#     @:returns The sorted dataframe
#     This method sorts the file by region_id and returns it
#     """
#     df = pd.read_csv(fileName)
#     df['value'] = pd.to_numeric(df['value'], errors='coerce')
#     df = df.sort_values(by='value')
#     return df

# def visualizeMap():
#     """
#     @:returns A plotted heatmap with zipcodes and their values as a heatmap
#     This function reads housing values from Zillow and matches them to their zipcodes and then
#     plots each value for each zipcode on a visual 2D heatmap of the United States.
#     """
#     # Getting Home Data
#     home_data = pd.read_csv("./ZILLOW_ZSFH_Filtered.csv")
#     home_data = home_data[['zip_code','value']]
#     # Getting Geometry
#     map_us = gpd.read_file('./map/tl_2019_us_zcta510.shx')
#     map_us = map_us[['ZCTA5CE10','geometry']]
#     map_us.rename(columns = {'ZCTA5CE10' : 'zip_code'}, inplace = True)
#     map_us['zip_code'] = map_us['zip_code'].astype(int)
#     # Merging
#     map_us = map_us.merge(home_data, on = 'zip_code')
#     # Plotting
#     maxVal = 3_000_000
#     map_us.loc[map_us['value'] >= maxVal, 'value'] = maxVal
#     map_us.plot(column = 'value',cmap = 'Spectral' ,legend = True)
#     plt.show()
#
#
# visualizeMap()

#Show the histogram of data
# sortHistogram("ZILLOW_ZSFH.csv")['value'].plot(kind='hist', bins=100, grid=True, range=[0, 1000000])
# plt.show()

# filterZipCodes("ZILLOW_ZSFH.csv")
# print(getZipCode(96817))
#createSnapshot("2020-01-31")