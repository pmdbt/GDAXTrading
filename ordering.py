import cbpro


"""This document is for functions related to ordering securities, buy/sell, and logic needed for safeguard against
unintended orders etc"""


class ordering(object):

    """
    This class is meant to deal and handle everything to do with ordering
    and executing an actual position based on user inputs as parameters. this
    can include buying, selling, determining position sizes, and finding
    products available to trade on coinbase pro.
    """


    def __init__(self, client, recommendation):

        """
        This function initializes variables for the class.

        client (client object): can be public or private cbpro clients
        recommendation (str): recommendation to buy or sell or hold based on
        a model's recommendation.

        returns: None
        """

        self.client = client
        self.recommendation = recommendation


    def find_products(self, search=None):

        """
        This class method searches for all the available cryptocurriencies
        that is available to trade. It allows one optional parameter called
        search, which is a string ticker input of a specific coin. If specified
        it will return the current market price of said coin or else it will
        return None.

        params: search (str)

        returns: product(s) (list) or None
        """

        if search == None:
            pass
        else:
            pass

    




def order(price_today, predicted_price, position_held):
	#first determine if the account currently has an open order or any positions
	#If pending order exists, cancel it. If positions held, liquidate asap
	#When it's confirmed that no pending orders exist and no positions are held, begin the ordering process
	#If predicted_price > price_today, initialize long position.
	#If predicted_price < price_today, initialize short position.
	#If predicted_price == price_today, do nothing, no position will be initialized
