import cbpro


"""This document is for functions related to ordering securities, buy/sell, and logic needed for safeguard against
unintended orders etc"""


class Ordering(object):

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


    def find_products(self):

        """
        This class method searches for all the available cryptocurriencies
        that is available to trade.

        returns: product(s) (list) or None
        """

        available_products = self.client.get_products()
        return available_products


    def parser(input=None, string_to_match=''):
        """
        This function takes in a parameter from the user as a string to match
        to the non-base pair of the currency. If The result contains said string,
        then it's returned. Otherwise, None is returned

        params: string_to_match (str)

        returns: matched (str)
        """

        if str(input)[-3:].upper() == string_to_match.upper():
            return input


    def parse_list(input=None, string_to_match=None):
        """
        This function is meant to abstract the process of parsing a list of
        potentially tradable products, then using the parser() function to find
        and return only the currency pairs with USD as the base currency
        """

        matched = []
        for item in iter(input):
            temp_var = \
            parser(input=item['display_name'], string_to_match=string_to_match)
            if temp_var:
                matched.append(temp_var)
            else:
                next

        return matched
