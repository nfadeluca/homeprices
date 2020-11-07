import quandl
import pandas

# This authenticates your account so that you may use data from Quandl
# You can find your authentication key in your Quandl account settings
quandl.ApiConfig.api_key = "s6x8gXSardesDec_nbyH"

# Making use of Zillow data
data = quandl.get_table('ZILLOW/DATA', indicator_id='ZSFH', region_id='99999')

