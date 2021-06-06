import logging
import lib.mxc_v2 as mxc


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logger = logging.getLogger(__name__)


def get_pair_price(pair):
    try:
        price = float(mxc.get_ticker(pair)["data"][0]["last"])
        return price
    except Exception as e:
        logger.warning(f"We got an error: {e}")
    return 0


def get_usdt_balance():
    account_info = mxc.get_account_info()
    try:
        usdt_balance = int(float(account_info["data"]["USDT"]["available"]))

    except Exception as e:
        logger.warning(f"We got an error: {e}")
        return 0
    if usdt_balance >= 5:
        return usdt_balance
    else:
        return 0


def get_pair_balance(pair):
    account_info = mxc.get_account_info()
    logger.warning(account_info)
    try:
        pair_balance = float(account_info["data"][pair]["available"])
        return pair_balance

    except Exception as e:
        logger.warning(f"We got an error: {e}")
        return 0


def buy_coin_limit(pair, type="LIMIT_ORDER", quote=10):
    quantity = 0
    pair = f"{pair}_USDT".upper()
    logger.warning(f"Buy for {pair}.")
    usdt_balance = get_usdt_balance()
    pair_price = get_pair_price(pair)
    if usdt_balance > 5:
        if quote < usdt_balance:
            quantity = float(quote / pair_price)
        else:
            quantity == float(usdt_balance / pair_price)
    else:
        logger.warning("We got an error: USDT balance lower than 5.")
        return None

    try:
        response = mxc.place_order(pair, pair_price, quantity, 'BID', type)
        logger.warning(f"Buy Response : {response}")
        return response
    except Exception as e:
        logger.warning(f"We got an error: {e}")


def buy_coin_market(pair, type="MARKET_ORDER", quote=10):
    quantity = 0
    pair = f"{pair}_USDT".upper()
    logger.warning(f"buy for {pair}.")
    usdt_balance = get_usdt_balance()
    if usdt_balance > 5:
        if quote < usdt_balance:
            quantity = quote
        else:
            quantity == usdt_balance
    else:
        logger.warning("We got an error: USDT balance lower than 5.")
        return None

    try:
        response = mxc.place_order(pair, 1, quantity, 'BID', type)
        logger.warning(f"Buy Response : {response}")
        return response
    except Exception as e:
        logger.warning(f"We got an error: {e}")


def sell_coin_limit(pair, type="LIMIT_ORDER"):
    quantity = get_pair_balance(pair=pair)
    pair = f"{pair}_USDT".upper()
    logger.warning(f"Sell for {pair}.")
    pair_price = get_pair_price(pair)

    try:
        response = mxc.place_order(pair, pair_price, quantity, 'ASK', type)
        logger.warning(f"Buy Response : {response}")
        return response
    except Exception as e:
        logger.warning(f"We got an error: {e}")

def sell_coin_market(pair, type="MARKET_ORDER"):
    quantity = get_pair_balance(pair=pair)
    pair = f"{pair}_USDT".upper()
    logger.warning(f"Sell for {pair}.")
    try:
        response = mxc.place_order(pair, 1, quantity, 'ASK', type)
        logger.warning(f"Buy Response : {response}")
        return response
    except Exception as e:
        logger.warning(f"We got an error: {e}")

