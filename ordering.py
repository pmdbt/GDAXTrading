"""This document is for functions related to ordering securities, buy/sell, and logic needed for safeguard against 
unintended orders etc"""



def order(price_today, predicted_price, position_held):
	#first determine if the account currently has an open order or any positions
	#If pending order exists, cancel it. If positions held, liquidate asap
	#When it's confirmed that no pending orders exist and no positions are held, begin the ordering process
	#If predicted_price > price_today, initialize long position.
	#If predicted_price < price_today, initialize short position.
	#If predicted_price == price_today, do nothing, no position will be initialized