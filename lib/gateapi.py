# coding: utf-8
import requests
import time
import hashlib
import hmac
import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger(__name__)

host = "https://api.gateio.ws"
prefix = "/api/v4"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}



def gen_sign(method, url, query_string=None, payload_string=None):
    key = config['gateio']['key']  # api_key
    secret = config['gateio']['secret']  # api_secret

    current_time = time.time()
    m = hashlib.sha512()
    if payload_string is not None:
        m.update(payload_string.encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, current_time)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(current_time), 'SIGN': sign}


def spot(pair, side, quote=1):
    quantity = 0.1
    global host
    global prefix
    global headers
    pair_usdt = f"{pair}_USDT"
    url = '/spot/orders'
    pair_price = float(get_pair_price(pair_usdt, side))
    logger.warning(f"{side} Price {pair_price}. ")
    if side.upper() == "BUY":
        usdt_balance = get_currency_balance("USDT")
        if usdt_balance > 5:
            if quote < usdt_balance:
                quantity = float(quote / pair_price)
            else:
                quantity = float(usdt_balance / pair_price)
        else:
            logger.error(f"USDT balance lower than 5. Amount {usdt_balance} ")
            return None
        query_param = ''
        # body='{"text":"t-123456","currency_pair":"TRX_USDT","type":"limit","account":"spot","side":"sell","iceberg":"0","amount":"1","price":"5.00032","time_in_force":"gtc","auto_borrow":false}'
        body = '{"text": "t-123456", "currency_pair": "%s", "type": "limit", "account": "spot", "side":"%s","iceberg": "0",' \
               '"amount": "%s","price": "%s","time_in_force": "gtc","auto_borrow": false}' % (str(pair_usdt.upper()),
                                                                                              str(side.lower()),
                                                                                              str(quantity),
                                                                                              str(pair_price))
        logger.warning(f"Buy request : {body}")
        # for `gen_sign` implementation, refer to section `Authentication` above
        sign_headers = gen_sign('POST', prefix + url, query_param, body)
        headers.update(sign_headers)
        r = requests.request('POST', host + prefix + url, headers=headers, data=body)
        logger.warning(f"Buy response : {r.json()}")
        return r.json()

    elif side.upper() == "SELL":
        pair_balance = float(get_currency_balance(pair))
        if pair_balance > 0:
            query_param = ''
            # body='{"text":"t-123456","currency_pair":"TRX_USDT","type":"limit","account":"spot","side":"sell","iceberg":"0","amount":"1","price":"5.00032","time_in_force":"gtc","auto_borrow":false}'
            body = '{"text": "t-123456", "currency_pair": "%s", "type": "limit", "account": "spot", "side":"%s","iceberg": "0",' \
                   '"amount": "%s","price": "%s","time_in_force": "gtc","auto_borrow": false}' % (
                   str(pair_usdt.upper()),
                   str(side.lower()),
                   str(pair_balance),
                   str(pair_price))

            logger.warning(f"Sell request : {body}")
            # for `gen_sign` implementation, refer to section `Authentication` above
            sign_headers = gen_sign('POST', prefix + url, query_param, body)
            headers.update(sign_headers)
            r = requests.request('POST', host + prefix + url, headers=headers, data=body)
            logger.warning(f"Sell request : {r.json()}")
            return r.json()
        else:
            logger.error(f"We got an error: {pair} balance equals to zero(0). Pair balance = {pair_balance}")
            return 0




def get_currency_balance(currency):
    global host
    global prefix
    global headers

    url = '/spot/accounts'
    query_param = ''
    # for `gen_sign` implementation, refer to section `Authentication` above
    sign_headers = gen_sign('GET', prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url, headers=headers)
    response = r.json()
    logger.warning(response)

    for resp in response:
        if resp["currency"] == currency.upper():
            logger.warning(f"Available {currency} : {resp['available']}")
            available = float(resp['available'])
            return available

    return 0


def get_pair_price(pair="TRX_USDT", operation="BUY"):
    global host
    global prefix
    global headers

    url = '/spot/order_book'
    query_param = f'currency_pair={pair}'
    r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)

    request = r.json()
    if operation == "BUY":
        return request["asks"][0][0]
    elif operation == "SELL":
        return request["bids"][0][0]
    else:
        return 0

def check_pair(pair):
    """
    Checks if coin name exist or not.
    :param pair: Coin name like TRX
    :return: returns a number if exist -1 if not
    """
    global host
    global prefix
    global headers

    url = '/spot/currency_pairs'
    query_param = ''
    r = requests.request('GET', host + prefix + url, headers=headers)
    request = r.json()
    return str(request).find(pair)

if __name__ == "__main__":
    logger.warning(get_currency_balance("xmc"))
#    logger.warning(check_pair("WIN"))
#    pair_balance = float(get_currency_balance("XRP"))
#    print(pair_balance)
#    if 0 < pair_balance:
#        logger.error(f"We got an error: XRP balance equals to zero(0). Pair balance = {pair_balance}")

    #spot(pair="TRX",side="SELL",quote=5)

"""
Notlar
BID:Buy
ASK:Sell

response
buy
{"id": "48275956765", "text": "t-123456", "create_time": "1621324466", "update_time": "1621324466", "status": "closed", "currency_pair": "TRX_USDT", "type": "limit", "account": "spot", "side": "buy", "amount": "42.7642832706", "price": "0.11692", "time_in_force": "gtc", "iceberg": "0", "auto_borrow": None, "left": "0", "fill_price": "4.987170715017372", "filled_total": "4.987170715017372", "fee": "0.0855285665412", "fee_currency": "TRX", "point_fee": "0", "gt_fee": "0", "gt_discount": False, "rebated_fee": "0", "rebated_fee_currency": "USDT"}


sell
{"id": "48276820848", "text": "t-123456", "create_time": "1621324811", "update_time": "1621324811", "status": "closed", "currency_pair": "TRX_USDT", "type": "limit", "account": "spot", "side": "sell", "amount": "43.678754704", "price": "0.11677", "time_in_force": "gtc", "iceberg": "0", "auto_borrow": None, "left": "0", "fill_price": "5.10779357508576", "filled_total": "5.10779357508576", "fee": "0.01021558715017152", "fee_currency": "USDT", "point_fee": "0", "gt_fee": "0", "gt_discount": False, "rebated_fee": "0", "rebated_fee_currency": "TRX"}

"""
