import logging
import sklearn
import pandas as pd
import datetime

# logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class Preprocessing(object):

    """
    This class is the template for all the preprocessing needs of deep learning
    model architectures for using time series analysis with historical
    crypto currency prices
    """

    def __init__(self, historical_data):
        self.historical_data = historical_data


    def data_cleaning(self, data):
        """
        This method is meant to clean the data using pandas methods before
        transformation into numpy array.

        1. make time column into datetime string format
        2. Turn rest of columns into float values
        3. reverse the order of the dataframe

        params:
        
        historical_data (dataframe)

        returns:

        cleaned_dataframe (pandas.DataFrame)
        """

        # function to convert unix epoch time to datetime
        def epoch_to_calendar(epoch_time):
            """
            This function turns epoch_time to string format of human
            readable datetime

            params: epoch_time (datetime object)

            returns: human_format (str)
            """

            # from epoch to datetime
            #date_obj = datetime.datetime.fromtimestamp(epoch_time)
            #return date_obj.strftime('%d-%m-%Y')
            # from datetime to epoch
            date_obj = epoch_time.timestamp()
            return date_obj

        if isinstance(data, pd.DataFrame):
            # find out all the datatypes for each column
            logging.info('data types of columsn before cleaning')
            logging.info(data.dtypes)
            # change the date columns from unix epoch to format dd-mm-yy
            data['time'] =  data.apply(
                    lambda row: epoch_to_calendar(row['Date']), axis=1)
            # change all data types to numerical/float
            data.apply(pd.to_numeric, errors='coerce')
            logging.info('data types of columns after cleaning')
            logging.info(data.dtypes)
            # use pandas fill methods to automatically fill missing values
            # with the average of the former + latter / 2
            data = (data.ffill() + data.bfill()) / 2
            # run ffill() and bfill() again incase first and last values are
            # also NaN
            data = data.bfill().ffill()
            # change the date columns from unix epoch to format dd-mm-yy
            data['time'] =  data.apply(
                    lambda row: epoch_to_calendar(row['time']), axis=1)

            return data

        else:
            # log the data type of the object
            logging.info('The data for cleaning is not a dataframe. It is\
                    type {0}'.format(str(type(data))))
            # exit the program
            exit()

    def transformation_pipeline(self):
        pass


    def pandas_to_numpy(self):
        pass
