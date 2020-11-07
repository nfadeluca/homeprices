import quandl
import matplotlib.pyplot as plt
import pandas as pd



# Making use of Zillow data
# This code uses the mass file
print("Reading file")
df = pd.read_csv("ZILLOW_DATA.csv")
print("File loaded!")
df = df.copy()[df['date'] == '2020-01-31']
df.to_csv("ZILLOW_JAN.csv", index = False)
print("File copied!")
df = df.copy()[df['indicator_id'] == 'ZATT']
df.to_csv("ZILLOW_ZATT.csv", index = False)
print("File copied!")


# print(list(df.columns))
#print(df['date'].head())



# print(df.head(10))
# print(df.size)