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
        pass


    def transformation_pipeline(self):
        pass


    def pandas_to_numpy(self):
        pass
