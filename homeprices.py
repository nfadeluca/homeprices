import quandl
import matplotlib.pyplot as plt

# This authenticates your account so that you may use data from Quandl
# You can find your authentication key in your Quandl account settings
quandl.ApiConfig.api_key = "s6x8gXSardesDec_nbyH"

# This is how we plot our x's and y's
plt.plot([1,2,3],[5,7,4])
plt.show()