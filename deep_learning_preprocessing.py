import logging
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler
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
        self.cleaned_data = None

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
            data['Date'] = data.apply(
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
            logging.info('full dataframe before dropping nan row for first date', data.head())
            data = data[1:]
            # change the date columns from unix epoch to format dd-mm-yy
            data['Date'] = data.apply(
                lambda row: epoch_to_calendar(row['Date']), axis=1)
            # save a copy of the cleaned data as a class variable
            self.cleaned_data = data
            return data

        else:
            # log the data type of the object
            logging.info('The data for cleaning is not a dataframe. It is\
                    type {0}'.format(str(type(data))))
            # exit the program
            exit()

    def _transformation_pipeline(self):
        """
        This function uses the sklearn pipeline method to add transformations
        to the raw data. The data as to be in numpy arrays first.

        Params: data (numpy array)

        Returns: transformed_data (numpy array)
        """
        if isinstance(self.X_train, np.ndarray) and isinstance(self.X_test, np.ndarray) and \
                isinstance(self.y_test, np.ndarray) and isinstance(self.y_train, np.ndarray):
            # perform log transformation on the price returns
            logging.debug('The dep_vals before log transformation: ', self.y_train)
            # transformers for Y values
            y_pipeline = ColumnTransformer([
                ('logging', np.log()),
            ])
            # drop the last column for Dates first and save a copy as object variable
            self.data_dates = self.X_train[:, -1]
            # transformers for X values
            X_pipeline = Pipeline([
                ('std_scalar', StandardScaler()),
            ])
            # call the full transformation pipeline sequentially then return both transformed X and Y values
            full_pipeline = FeatureUnion(transformer_list=[
                ('y_pipeline', y_pipeline),
                ('X_pipeline', X_pipeline),
            ])
            # execute full pipeline
            pass
        else:
            logging.INFO('training and testing data in transformation_pipeline not numpy array...')
            exit()

    @staticmethod
    def pandas_to_numpy(dataframe):
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

    @staticmethod
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

    def _train_test_split(self, X_vals, Y_vals):
        """
        private class method to split the cleaned data into training and testing set, then splitting again to X and Y
        train and test sets respectively.

        :return: X_train (np.array), X_test (np.array), y_train (np.array), y_test (np.array)
        """
        if isinstance(X_vals, np.ndarray) and isinstance(Y_vals, np.ndarray):
            X_train, X_test, y_train, y_test = train_test_split(
                X_vals,
                Y_vals,
                test_size=0.2,
                random_state=None,
                shuffle=False)
            # set object variables
            self.X_train = X_train
            self.X_test = X_test
            self.y_train = y_train
            self.y_test = y_test
        else:
            logging.info('cannot split data into training and testing, function argument was not a numpy array')
            exit()
