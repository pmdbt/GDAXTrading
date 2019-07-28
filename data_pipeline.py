# 3rd party imports
import pandas as pd
import cbpro
import logging
import datetime
from pytz import timezone

# custom imports
import configuration as config

# logging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class Data_Pipeline(object):
    """
    This class contains all the relevant methods to download, clean, and
    preprocess data needed for the neural network to train. It leverages
    preprocessing pipelines from sklearn
    """
    def __init__(self, key, b64secret, passphrase, product_id, granularity,
                 time_differential):
        self.key = key
        self.b64secret = b64secret
        self.passphrase = passphrase
        self.product_id = product_id
        self.granularity = granularity
        self.time_differential = time_differential

    def set_public_client(self):
        """
        This method sets the public client from gdax pro to a class variable
        """

        self.public_client = cbpro.PublicClient()

    def get_data(self, client):
        """
        This method uses the gdax client to obtain the entire historical
        time series of a crypto currency asset, then converts the data
        format into pandas dataframe, then reverses the order, so that
        the first row is the oldest data and the last row is the newest data.

        params:

        client (the gdax trading client object)
        product_id (the product id from gdax for the asset, str)
        granularity (what time frame each row consists of, int)


        returns:
        
        historical_data (pandas dataframe)
        """

        end_time = datetime.datetime.utcnow().date()
        start_time =datetime.datetime.strptime(config.start_time,
                '%b %d %Y').date()

        # api does not allow fetching of more than 300 days worth of data
        # at once, so we must do it iteratively
        time_delta = end_time - start_time
        print(time_delta.days)


        data = client.get_product_historic_rates(product_id=self.product_id,
                                                 end=end_time.isoformat(),
                                                 granularity=self.granularity)

        logging.info('The length of original historical dataset is: {}'\
                .format(str(len(data))))

        headers = ['time', 'low', 'high', 'open', 'close', 'volume']
        data_frame = pd.DataFrame(data, columns=headers)

        print(data_frame.head())

    def clean_data(self):
        pass

    def preprocessing_pipeline(self):
        pass

    def execute_all(self):
        pass


if __name__ == "__main__":

    # test code
    test_obj = Data_Pipeline(config.key, config.b64secret, config.passphrase,
            config.btc_usd, config.gdax_day, config.time_differential)

    test_obj.set_public_client()
    test_obj.get_data(test_obj.public_client)
