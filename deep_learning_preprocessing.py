import logging
import sklearn
import pandas as pd
import numpy as np
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
        3. Turn data into percentage changes

        params:
        
        historical_data (dataframe)

        returns:

        cleaned_dataframe (pandas.DataFrame)
        """

        def epoch_to_calendar(epoch_time):
            """
            This function turns epoch_time to string format of human
            readable datetime

            params: epoch_time (datetime object)

            returns: human_format (str)
            """

            # from epoch to datetime
            date_obj = datetime.datetime.fromtimestamp(epoch_time)
            return date_obj.strftime('%d-%m-%Y')


        def datetime_conversion(str_datetime):
            """
            This function converts string datetime data into epoch int values.

            params: str_datetime (str)

            returns: epoch_time (int)
            """
            date_obj = datetime.datetime.strptime(str_datetime, '%Y-%m-%d')
            epoch_time = date_obj.timestamp()
            return epoch_time


        if isinstance(data, pd.DataFrame):
            # find out all the datatypes for each column
            logging.info('data types of columsn before cleaning')
            logging.info(data.dtypes)
            # change the date columns from unix epoch to format dd-mm-yy
            data['Date'] =  data.apply(
                    lambda row: datetime_conversion(row['Date']), axis=1)
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
            # replace all values of 0 with 1 to prevent inf % change
            data.replace(0, 1, inplace=True)
            # split out the date column from next calculation
            date_column = data['Date']
            # turn data into percentage changes and then drop date column
            data = data.pct_change().drop('Date', axis=1)
            # join the split out data column with main frame then drop 1st row
            data['Date'] = date_column
            data = data[1:]
            # change the date columns from unix epoch to format dd-mm-yy
            data['Date'] =  data.apply(
                    lambda row: epoch_to_calendar(row['Date']), axis=1)
            return data

        else:
            # log the data type of the object
            logging.info('The data for cleaning is not a dataframe. It is\
                    type {0}'.format(str(type(data))))
            # exit the program
            exit()


    def transformation_pipeline(self, data):
        """
        This function uses the sklearn pipeline method to add transformations
        to the raw data. The data as to be in numpy arrays first.

        Params: data (numpy array)

        Returns: transformed_data (numpy array)
        """

        def X_Y_split(array):
            """
            This function splits an entire numpy array into the X and Y
            variables for modeling purposes. It assumes the first column in
            the array is the dependent variable (Y).

            Params: array (np.ndarray)

            Returns: ind_vals (np.ndarray), dep_vals (np.ndarray)
            """
            ind_vals = array[:, 1:]
            dep_vals = array[:, 0]
            return ind_vals, dep_vals

        if isinstance(data, np.ndarray):
            # perform log transformation on the price returns
            ind_vals, dep_vals = X_Y_split(data)
            print(dep_vals)
        else:
            logging.INFO('param in transformation_pipeline not numpy array...')
            exit()


    def pandas_to_numpy(self, dataframe):
        """
        Turns a pandas dataframe into a numpy array before passing into
        deep learning models. Split out pandas series of date columsn or
        time based columns and returns them seperately as another object for
        later use.

        params: data (Pandas.DataFrame)

        returns: split_obj (Pandas.Series), data (numpy array)
        """
        if isinstance(dataframe, pd.DataFrame):
            return dataframe.to_numpy()
        else:
            logging.INFO('parameter in pandas_to_numpy func not a dataframe.')
            exit()

