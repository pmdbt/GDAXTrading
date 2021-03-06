from deep_learning_preprocessing import Preprocessing
import configuration as config
from DataBases import aws_mysql_database as aws_mysql
import datetime
import traceback
import pandas as pd

# global date for this script
global_date_today = datetime.datetime.utcnow().date() - datetime.timedelta(1)
global_date_yesterday = (global_date_today - datetime.timedelta(1))
global_date_twodays = (global_date_today - datetime.timedelta(2))


# function to compare yesterday's prediction with today's result
def walkforward_accuracy(two_days_ago, yesterday, today_close):
    # the logic is to measure directional accuracy
    """
    If today's closing price is higher than yesterday's closing price AND if
    yesterday's prediction was higher than two days ago's prediction, the
    forecasted directional move was correct.

    If today's closing price is LOWER than yesterday's closing price AND if
    yesterday's prediction was LOWER than two days ago's prediction, the
    forecasted directional move was also correct.

    If the above scenario was true for equality instead of greater than or
    less than, also considered correct.

    All OTHER scenarios are considered to be incorrect
    """


    # comparison logic, a must be older data than b
    def compare_values(a, b):
        if float(a) < float(b):
                return 'less_than'
        elif float(a) > float(b):
                return 'greater_than'
        else:
                return 'equal_to'


    if isinstance(two_days_ago, pd.DataFrame) and \
            isinstance(yesterday, pd.DataFrame):
        if two_days_ago.empty == False and yesterday.empty == False:
            # variable is ranked by starting alphebet, a < b < c etc for time ranking
            a_prediction = two_days_ago['tomorrow_predicted_close']
            b_close = yesterday['close']
            b_prediction = yesterday['tomorrow_predicted_close']
            c_close = today_close

            # compare results
            compare_close_prices = compare_values(b_close, c_close)
            compare_predictions = compare_values(a_prediction, b_prediction)
            if compare_close_prices == compare_predictions:
                return True
            else:
                return False
    else:
        return None # since accuracy cannot be computed

# function to organize upload data into a fixed dataframe before uploading
def organize_upload(today_close, tomorrow_predicted_close, past_data=None):
    if isinstance(past_data, pd.DataFrame):
        yesterday = past_data.loc[past_data['date'] == \
                global_date_yesterday]
        two_days = past_data.loc[past_data['date'] == \
                global_date_twodays]

        prior_prediction_accuracy = walkforward_accuracy(
            two_days,
            yesterday,
            today_close)
    else:
        prior_prediction_accuracy = None

    dict_to_upload = {
                        'date': global_date_today,
                        'close': today_close,
                        'tomorrow_predicted_close': tomorrow_predicted_close,
                        'prior_day_prediction_accuracy': \
                                prior_prediction_accuracy
                    }

    upload_data = pd.DataFrame([dict_to_upload])
    return upload_data

# main function to execute the entire script flow
def main():
    try:
        past_data_query = "select * from btc_trading_v025 where date\
                > CURDATE()-4 and date < CURDATE()-1;"
        past_data = aws_mysql.downloading(
                user=config.user,
                password=config.password,
                host=config.host,
                db=config.db,
                query=past_data_query)
        print(past_data)
        print(type(past_data['date'][0]))
    except:
        traceback.print_exc(limit=5)
        past_data = None

    try:
        # create instance of TimeseriesTrading Class
        trading_obj = TimeseriesTrading(
                key=config.key,
                b64secret=config.b64secret,
                passphrase=config.passphrase,
                time_differential=config.time_differential[0],
                product_id=config.btc_usd,
                granularity=config.gdax_day
        )

        # organize data for uploading to mysql
        today_close_price, prediction = trading_obj.execute()

        if isinstance(past_data, pd.DataFrame):
            upload_data = organize_upload(
                today_close_price,
                prediction,
                past_data=past_data)
            print(upload_data)
        else:
            upload_data = organize_upload(
                today_close_price,
                prediction)
            print(upload_data)

        # upload logic here to mysql
        aws_mysql.uploading(
            user=config.user,
            password=config.password,
            host=config.host,
            db=config.db,
            table='btc_trading_v025',
            upload_data=upload_data
        )
    except:
        traceback.print_exc(limit=5)


# main function to train neural network
def neural_main():
    # create Data_Pipeline object to get new data
    pass

    # create Preprocessing_Pipeline to clean data
    # for testing, use the csv file in directory
    test_data = pd.read_csv('test_data.csv') 
    print(test_data.head())
    preprocessing_obj = Preprocessing(test_data)
    preprocessing_obj.data_cleaning(test_data)
    print(preprocessing_obj.cleaned_data.head())
    # turn data into numpy array
    cleaned_array = preprocessing_obj.pandas_to_numpy(preprocessing_obj.cleaned_data)
    # call prepare data method
    preprocessing_obj.nn_data_prepare(cleaned_array)


# main executable
if __name__ == "__main__":

    # do something
    #main()
    neural_main()
