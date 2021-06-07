#!/usr/bin/env python
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

2.  cleanRegionsMethod overwrites old regions file with new one that contains
    only region and region_id columns

3. sortHistogram sorts ZILLOW_ZSFH

4. 

"""

def pullDataSubset():
    """
    @:returns Returns the unsorted but filtered dataframe
    This function reads the Zillow data file and then outputs a csv file containing
    only the home price data for a certain month and type of home
    """
    print("Opening up")
    df = pd.read_csv("ZILLOW_DATA.csv")
    #The date here is the date that will be outputted
    df = df.copy()[df['date'] == '2020-01-31']
    #index = False gets rid of the first column
    df.to_csv("ZILLOW_JAN.csv", index = False)
    df = df.copy()[df['indicator_id'] == 'ZSFH']
    df.to_csv("ZILLOW_ZSFH.csv", index = False)


def cleanRegionsMethod():
    """
    Creates new ZILLOW_REGIONS csv file that overwrites the old one,
    keeping only region and region_id columns.
    """
    final = []
    # Opens ZILLOW_REGIONS and write only lines with zipcodes
    with open('ZILLOW_REGIONS.csv') as f:
        lines = f.readlines()
        with open('ZILLOW_REGIONS.csv', 'w') as g:
            for line in lines:
                if 'zip' in line:
                    g.write(line)
    # Removing commas and joining newly written lines
    with open('ZILLOW_REGIONS.csv') as h:
        lines = h.readlines()
        for line in lines:
            line = line.split(',')
            for item in line:
                if item == 'zip': line.remove('zip')
            line = ','.join(line)
            line = line.split(';')
            final.append(line[0])
    # Writing zip codes
    with open('ZILLOW_REGIONS.csv', 'w') as j:
        j.write("region,region_id\n")
        for item in final:
            item = item.strip('\n')
            j.write(str(item))
            j.write('\n')


cleanRegionsMethod()

def addZipCodes(fileName):
    """
    @:param filename: The name of the file to populate with zip codes
    @:returns filename: A modified file containing a new zip codes column
    This function will add a new column to the dataset containing the zip codes
    """
    df = pd.read_csv(fileName)
    global regions
    regions = pd.read_csv("ZILLOW_REGIONS.csv")
    df['zip_code'] = df['region_id'].apply(getZipCode)
    print("Outputting CSV file.")
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
        print("Zip code found: " + str(zipCode))
    return zipCode


def filterZipCodes(fileName):
    """
    @:param fileName: The file to be processed
    @:returns New CSV file with zipcodes only (ZILLOW_TEST_Filtered)
    This function reads and writes from the TEST File (originally ZSFH) after the zipcode column
    has been added along with all of its zip codes. It filters the file by removing all of the
    "None" values inside of the zipcodes column.
    """
    with open(fileName, 'r') as file:
        rows = file.readlines()
        with open('ZILLOW_ZSFH_Filtered.csv', 'w') as newfile:
            for row in rows:
                if 'None' not in row:
                    newfile.write(row)

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


def sortHistogram(fileName):
    """
    @:param fileName: The file to sort
    @:returns The sorted dataframe
    This method sorts the file by region_id and returns it
    """
    df = pd.read_csv(fileName)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.sort_values(by='value')
    return df

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