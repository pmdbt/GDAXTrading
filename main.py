from timeseries_model import TimeseriesTrading
import configuration as config


def main():

	# create instance of TimeseriesTrading Class
	trading_obj = TimeseriesTrading(
		key=config.key,
		b64secret=config.b64secret,
		passphrase=config.passphrase,
		time_differential=config.time_differential[0],
		product_id=config.btc_usd,
		granularity=config.gdax_day
	)

	prediction = trading_obj.execute()

# main executable
if __name__ == "__main__":

	# do something
	main()
