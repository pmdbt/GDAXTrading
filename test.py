import cbpro
from ordering import Ordering
import configuration as config


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


def account_info(auth_client):
    """
    This function is meant to request an authenticated user's account info
    from coinbase pro. We want to use this to find out whether we have any
    existing current cryto position size

    params: auth_client (object)

    returns: result (dict/json)
    """

    accounts = auth_client.get_accounts()
    for account in iter(accounts):
        if str(account['currency']) == 'LTC':
            # get_account_history() method returns a generator expression
            # have to use list() to print the actual results
            ltc_history = auth_client.get_account_history(account['id'])
            return list(ltc_history)


client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(
    key=config.key,
    b64secret=config.b64secret,
    passphrase=config.passphrase
)

order_object = Ordering(auth_client, 'buy')

available_usd_products = client.get_products()
print(parse_list(input=available_usd_products, string_to_match='USD'))
print(account_info(auth_client))
