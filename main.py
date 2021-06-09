import logging
import time

from telethon import TelegramClient, events, sync
import lib.mxcApiOperations as mxcao
import lib.gateapi as gateio

borsa_name = "GATEIO"
logging.basicConfig(format='%(asctime)s :: %(name)s :: %(levelname)-8s ::  %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)


def listen_group():
    # Remember to use your own values from my.telegram.org!
    logger.warning("we started!!!!")
    api_id = 50819989 #id from my.telegram.org
    api_hash = '830436i793jec1d8f33d8122855ce1ca' #hash from my.telegram.org
    client = TelegramClient('anon', api_id, api_hash)

    #@client.on(events.NewMessage(chats='turkiyepumpgrubu_mxc'))
    #@client.on(events.NewMessage(chats=('pumpdenemegrubu','turkiyepumpgrubu_mxc')))
    @client.on(events.NewMessage(chats=("pumpdenemegrubu", "turkiye_pump_grup")))
    async def my_event_handler(event):
        logger.warning(event.raw_text)
        event_borsa_operation(message=event.raw_text)
        event_coin_operation(message=event.raw_text)

    client.start()
    client.run_until_disconnected()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    logger.warning(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def event_borsa_operation(message):
    global borsa_name
    message = f"abdulsamed {message}"
    if message.find("gate.io") > 0 or message.find("GATE.İO") > 0 or message.find("GATE.IO") > 0 or message.find(
            "gateio") > 0 or message.find("GATEIO") > 0 or message.find("GATEİO") > 0:
        borsa_name = "GATEIO"
        logger.warning(f"Spot operations will be made on {borsa_name}")
    elif message.find("MXC") > 0 or message.find("mxc") > 0 or message.find("mxc.com") > 0 or message.find(
            "MXC.COM") > 0:
        borsa_name = "MXC"
        logger.warning(f"Spot operations will be made on {borsa_name}")
    else:
        logger.warning(f"No borsa_name set. Last status {borsa_name}.")


def event_coin_operation(message):
    global borsa_name
    pump_message_control_en = message.find("ADI")
    pump_message_control_tr = message.find("ADİ")
    if pump_message_control_en > 0 or pump_message_control_tr > 0:
        for line in message.split('\n'):
            line_control_en = line.find("ADI")
            line_control_tr = line.find("ADİ")
            if line_control_en > 0 or line_control_tr > 0:
                message_list = line.split(":")
                pair = message_list[(len(message_list) - 1)].strip()
                logger.warning(f"Buy-Sell Pair : {pair}.")
                logger.warning(f"Spot operations will be made on {borsa_name}.")
                if borsa_name == "MXC":
                    buy = mxcao.buy_coin_market(pair=pair, quote=9)
                    time.sleep(30)
                    sell = mxcao.sell_coin_market(pair=pair)
                elif borsa_name == "GATEIO":
                    if gateio.check_pair(pair=pair) != -1:
                        buy = gateio.spot(pair=pair, side="BUY", quote=9)
                        time.sleep(30)
                        sell = gateio.spot(pair=pair, side="SELL")
                    else:
                        logger.warning(f"Pair {pair} not exist on market {borsa_name}")
                else:
                    logger.warning("Borsa can not found.")
    else:
        logger.warning("No coin found on message.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    listen_group()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
