import base64
import configparser
import logging
import math

import requests

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('lib/config.ini')
#config.read('config.ini')

API_KEY = config['probit']['key']  # 'mx0g3UtwiwTqgU8m6j'
SECRET_KEY = config['probit']['secret']  # 'aea8cdf8ae874d60897a37f1c18f2abc'

url = "https://api.probit.com/api/exchange/v1/new_order"


def get_request_headers():
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               "Authorization": f"Bearer {get_token()}"}
    return headers


def get_token():
    url = "https://accounts.probit.com/token"

    payload = {"grant_type": "client_credentials"}
    headers = {
        "Accept": "application/json",
        "Authorization": base64_encode(),
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()["access_token"]


def buy_coin_market(pair=None, cost=None):
    if not check_pair_status(pair=pair):
        logger.error(f"{pair} closed for market.")
        return None
    global url
    usdt_amount=decide_usdt_amount(cost)
    body = {

        "cost": f"{usdt_amount}",
        "market_id": f"{pair.upper()}-USDT",
        "side": "buy",
        "time_in_force": "ioc",
        "type": "market"
    }
    logger.warning(body)
    response = requests.request("POST", url, json=body, headers=get_request_headers())
    return response.json()


def sell_coin_market(pair):
    """
    :param pair: coin pair to buy
    :param quote: sell operation usdt amount
    :return: json
    """

    if not check_pair_status(pair=pair):
        logger.error(f"{pair} closed for market.")
        return None

    global url
    body = {

        "market_id": f"{pair.upper()}-USDT",
        "quantity": f"{get_currency_balance(pair=pair)}",
        "side": "sell",
        "time_in_force": "ioc",
        "type": "market"
    }
    logger.warning(body)
    response = requests.request("POST", url, json=body, headers=get_request_headers())
    print(response.text)


def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier


def get_currency_balance(pair=None):
    url = "https://api.probit.com/api/exchange/v1/balance"

    response = requests.request("GET", url, headers=get_request_headers())
    json_response = response.json()
    data = json_response["data"]
    for coin in data:

        if coin["currency_id"] == pair:
            logger.warning(f"{pair} available amount {coin['available']}")
            available = float(coin["available"])
            return round_down(available, 3)

    return 0


def check_pair_status(pair):
    url = "https://api.probit.com/api/exchange/v1/market"

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers)
    json_response = response.json()
    data = json_response["data"]
    for coin in data:

        if coin["id"] == f"{pair.upper()}-USDT":
            if coin["closed"] == False:
                return True

            else:
                return False


def base64_encode():
    """
    Encodes api id and secret to basic auth
    :return: Basic + key
    """
    global API_KEY
    global SECRET_KEY
    data = f"{API_KEY}:{SECRET_KEY}"
    encodedBytes = base64.b64encode(data.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")

    return f"Basic {encodedStr}"


def decide_usdt_amount(wanted_usdt_amount):
    available_usdt_amount = float(get_currency_balance("USDT"))
    wanted_usdt_amount = float(wanted_usdt_amount)
    if available_usdt_amount > 1.0:
        if wanted_usdt_amount > 1.0:
            if wanted_usdt_amount < available_usdt_amount:
                return wanted_usdt_amount
            else:
                return available_usdt_amount-((available_usdt_amount*0.2)/100)
        else:
            return available_usdt_amount


#if __name__ == "__main__":
    # base64_encode()
    # get_token()
    # buy_coin_market("TRX", 2)
    # check_pair_status("MCASH")
    #logger.warning(get_currency_balance("USDT"))
    #logger.warning(decide_usdt_amount(1.10))
    # time.sleep(30)
    # sell_coin_market(pair="TRX")
    # logger.warning(get_currency_balance(pair="TRX"))
