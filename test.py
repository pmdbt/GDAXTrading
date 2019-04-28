import gdax
import datetime
from math import log
from numpy import exp
import MySQLdb
from pystats import py_calc
from pytz import timezone

#MySQL DB creditials
host = 'rds-mysql-pricepredictions.cdrzp6diy4i4.us-east-1.rds.amazonaws.com' #aws server and database
user = 'masterUsername'
password = 'Forest93*'
db = 'PricePredictions'

#initialization of credentials
key = '199c0fe32877ecf80aefd2be74ed2794'
b64secret = 'EujC/x79zGYxsfHwb7J+MhgCpANZt1t2AGmG+i17gCKiH30IBrWsvlxS47fbuWaNcHbDV++r1zC+q6SiwFwhdg=='
passphrase = 'bnwjgg5m885'
api_url = "https://api-public.sandbox.gdax.com"
product_id = 'BTC-USD'
time_differential = [100, 130, 150, 170]
#gdax time values
gdax_min = '60'
gdax_five_min = '300'
gdax_fifteen_min = '900'
gdax_hour = '3600'
gdax_six_hour = '21600'
gdax_day = '86400'


#public_client = gdax.PublicClient()
#creating the authorized client object
auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase)
#function to grab historical data set with specific parameters, converts data set into r readable data with only prices
def historic_data(product_id, granularity, time_differential):
	end_time = datetime.datetime.now(timezone('UTC'))
	start_time = datetime.datetime.now(timezone('UTC')) - datetime.timedelta(days=time_differential)

	data = auth_client.get_product_historic_rates(product_id=product_id,
												  start=start_time.isoformat(),
												  end=end_time.isoformat(),
												  granularity=granularity)
	closing_prices = []
	for i in range(len(data)): #gdax returns a list within a list. The 5th element of inner list is close price
		closing_prices.append(data[i][4])
	closing_prices_sorted = list(reversed(closing_prices))

	return closing_prices_sorted #gdax gives most recent days first, we want them last

#dynamically set up the resulting model from R regression
def model_creation(prices, time_differential):
	coef_results, adj_rsquared, has_const = py_calc(prices, time_differential) #stores the 3 values returned by py_calc
	logged_result = 0
	V1 = coef_results
	index = V1.index
	if len(V1) == 1 and has_const is True:
		print("Model is not accurate enough, only the intercept is significant")
	elif len(V1) > 1 and has_const is True:
		for i in range(1, len(V1)):
			day_lag = int(index[i][3:])-1 #turns the day lag name into an int, -1 is to shift days since we want to predict tomorrow's price
			print(day_lag)
			logged_result = logged_result + (V1[i]*log(prices[len(prices)-1-day_lag])) #len(prices)-day_lag gives the price on the lagged day

		logged_result = logged_result + V1[0] #adds the constant at the end
	#the only thing different for this loop is that it doesn't account for the constant being there
	elif len(V1) >= 1 and has_const is False:
		for i in range(0, len(V1)):
			day_lag = int(index[i][3:])-1
			print(day_lag)
			logged_result = logged_result + (V1[i]*log(prices[len(prices)-1-day_lag]))
	else:
		print("Something probably went wrong.") #helps with bug checks
	predicted_price = exp(logged_result) #must transform result back to prices instead of log prices
	print("Today's closing price is: " + str(prices[len(prices)-1]))
	print("The predicted price for tomorrow's close is: " + str(predicted_price))
	return predicted_price
#Testing model_creation
#prices = historic_data(product_id, gdax_day, time_differential)
#model_creation(prices, time_differential)

#Main executables
my_sql_input = []
my_sql_input.append(str(datetime.datetime.now(timezone('UTC')) + datetime.timedelta(days=1)))
#execute calculations for all the time differentials
for days in time_differential:
	prices = historic_data(product_id, gdax_day, days)
	my_sql_input.append(model_creation(prices, days))
my_sql_input.append(prices[len(prices)-1])
#my_sql_input.append(str(prices[len(prices)-2]))
print(my_sql_input)
#MySQL interface
