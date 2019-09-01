import sklearn


class Preprocessing(object):

    """
    This class is the template for all the preprocessing needs of deep learning
    model architectures for using time series analysis with historical
    crypto currency prices
    """

    def __init__(self, historical_data):
        self.historical_data = historical_data


    def data_cleaning(self):
        """
        This method is meant to clean the data using pandas methods before
        transformation into numpy array.

        1. make time column into datetime string format
        2. Turn rest of columns into float values
        3. reverse the order of the dataframe

        params:
        
        self.historical_data (dataframe)

        returns:

        cleaned_dataframe (pandas.DataFrame)
        """
        pass


    def transformation_pipeline(self):
        pass


    def pandas_to_numpy(self):
        pass
