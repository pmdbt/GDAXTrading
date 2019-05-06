import cbpro
import datetime
from math import log
from numpy import exp
import sqlalchemy
from pystats import py_calc
from pytz import timezone
from time import sleep
import configuration as config
from pystats import py_calc


class TimeseriesTrading:

    def __init__(self, **kwargs):
        self.key = kwargs['key']
        self.b64secret = kwargs['b64secret']
        self.passphrase = kwargs['passphrase']
        self.product_id = kwargs['product_id']
        self.granularity = kwargs['granularity']
        self.time_differential = kwargs['time_differential']


    def set_public_client(self):
        # create the public client to obtain data from api
        self.public_client = cbpro.PublicClient()

    #function to grab historical data set with specific parameters, converts data set into r readable data with only prices
    def historic_data(self, client, product_id, granularity, time_differential):

        end_time = datetime.datetime.now(timezone('UTC'))

        start_time = datetime.datetime.now(timezone('UTC')) \
        - datetime.timedelta(days=time_differential)

        data = client.get_product_historic_rates(
                product_id=product_id,
                start=start_time.isoformat(),
                end=end_time.isoformat(),
                granularity=granularity)

        closing_prices = []

        for i in range(len(data)): #gdax returns a list within a list. The 5th element of inner list is close price
            closing_prices.append(data[i][4])
        closing_prices_sorted = list(reversed(closing_prices))
        # print the last 5 days closing_prices
        print(closing_prices_sorted[-5:])
        return closing_prices_sorted #gdax gives most recent days first, we want them last


    #dynamically set up the resulting model from R regression
    def model_creation(self, prices, time_differential):
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


    # method to execute everything class method in desired order
    def execute(self):
        self.set_public_client()
        historical_prices = self.historic_data(
            self.public_client,
            self.product_id,
            self.granularity,
            self.time_differential)

        predicted_price = self.model_creation(
            historical_prices,
            self.time_differential
        )
        return predicted_price


#Testing model_creation
#prices = historic_data(product_id, gdax_day, time_differential)
#model_creation(prices, time_differential)

#Main executables
#my_sql_input = []
#my_sql_input.append(str(datetime.datetime.now(timezone('UTC')) + datetime.timedelta(days=1)))
##execute calculations for all the time differentials
#for days in time_differential:
#    prices = historic_data(product_id, gdax_day, days)
#    my_sql_input.append(model_creation(prices, days))
#    sleep(1)
#
#my_sql_input.append(prices[len(prices)-1])
##my_sql_input.append(str(prices[len(prices)-2]))
#print(my_sql_input)
##MySQL interface
#connection = MySQLdb.connect(host=host, user=user, passwd=password, db=db)
#
#cursor = connection.cursor()
#cursor.execute(
#    """INSERT INTO different_predictions (times, btc100, btc130, btc150, btc170, btc200, btc250, price)
#    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (my_sql_input))
#connection.commit()
##cursor.execute("""SELECT * FROM different_predictions""")
##print(cursor.fetchall())
#cursor.close()
