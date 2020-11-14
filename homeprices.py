#!/usr/bin/env python
import quandl
import matplotlib.pyplot as plt
import pandas as pd
""""""



# Making use of Zillow data
"""
This method reads the Zillow data file and then outputs a csv file containing
only the home price data for a certain month and type of home
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
    #This
    df = df.copy()[df['indicator_id'] == 'ZATT']
    df.to_csv("ZILLOW_ZATT.csv", index = False)
    print("File copied!")

