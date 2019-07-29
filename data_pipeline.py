# 3rd party imports
import pandas as pd
import cbpro
import logging
import datetime
from pytz import timezone
from datetime import timedelta
from math import floor

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


    def number_of_requests(self, start, end):
        """
        This method takes in 2 paramters, then finds out the number
        of requests it takes to obtaint he entire historical data set
        off of coinbase's api.

        params:

        start (start datetime object, object)
        end (end datetime object, object)

        returns:

        requests_needed (int)
        """

        time_delta = end - start
        num_requests = floor(time_delta.days / 300)
        remainder = time_delta.days % 300
        if remainder != 0:
            num_requests += 1

        logging.info("Total number of requests: {}".format(num_requests))
        logging.info("Remainder is: {}".format(remainder))

        return num_requests, remainder


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
        num_requests, remainder = self.number_of_requests(start_time, end_time)

        iter_start = None
        iter_end = None
        for i in range(0, num_requests-1):
            if i == 0:
                iter_start = start_time
                iter_end = iter_start + timedelta(300)
            else:
                iter_start = timedelta((i*300)+1)+start_time
                iter_end = iter_start + timedelta(300)
            logging.info(iter_start.strftime("%m-%d-%Y"))
            logging.info(iter_end.strftime("%m-%d-%Y"))

        if remainder != 0:
            iter_start = iter_end + timedelta(1)
            iter_end = end_time
            logging.info(iter_start.strftime("%m-%d-%Y"))
            logging.info(iter_end.strftime("%m-%d-%Y"))
        

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
