import quandl
import matplotlib.pyplot as plt
import pandas as pd

# This authenticates your account so that you may use data from Quandl
# You can find your authentication key in your Quandl account settings
quandl.ApiConfig.api_key = "s6x8gXSardesDec_nbyH"

# This is how we plot our x's and y's using matplotlib
plt.plot([1,2,3],[5,7,4])
plt.show()

# Making use of Zillow data
data = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id='99999')
print(data)