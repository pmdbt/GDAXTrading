from timeseries_model import TimeseriesTrading
import configuration as config


def main():

	# create instance of TimeseriesTrading Class
	trading_obj = TimeseriesTrading(
		config.key,
		config.b64secret,
		config.passphrase,
		config.time_differential,
		config.btc_usd,
		config.gdax_day
	)
	prediction = trading_obj.execute()
	print(prediction)

# main executable
if __name__ == "__main__":

	# do something
	main()
