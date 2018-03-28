import logging
from logging.handlers import TimedRotatingFileHandler

import locale
import re

from emoji import emojize

from pricebot.config import *

locale.setlocale(locale.LC_NUMERIC, 'en_GB.utf8')

# start logging - print it to console for test cases
# logging.basicConfig(level=logging.INFO,
#                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# module_logger = logging.getLogger(__name__)

# start logging to the file with log rotation at midnight
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler(os.path.dirname(os.path.realpath(__file__)) + '/../pricebot.log',
                                   when='midnight',
                                   backupCount=10)
handler.setFormatter(formatter)
module_logger = logging.getLogger(__name__)
module_logger.addHandler(handler)
module_logger.setLevel(logging.INFO)
# end of log section


def parse_api_coinmarketcapjson(message_ticker):
    """
    the function to download API from the agregators sites to local file

    :param  message_ticker: a message with a ticker from user's request
    :type   message_ticker: str
    """

    # list of all conis from coinmarketcapjson from single class "jsonfiles" of config.py
    coinmarketcapjson = jsonfiles.coinmarketcapjson

    msg_parse_api = ''

    # temporaly while do not download API file
    # for read coinslist from a json file
    #
    # if os.path.isfile(FILE_JSON_COINMARKET):
    #     # Read configuration
    #     with open(FILE_JSON_COINMARKET) as coinmarketcapjson:
    #         try:
    #             import json
    #             coinmarketcapjson = json.load(coinmarketcapjson)
    #         except:
    #             module_logger.error('api.coinmarketcap.com! bad json file to read: %s', coinmarketcapjson)
    #             msg_parse_api += error_information()

    if coinmarketcapjson and 'error' in coinmarketcapjson:

        error = coinmarketcapjson['error']
        module_logger.error('api.coinmarketcap.com! Error message: %s', error)
        msg_parse_api += error_information()

        # TODO send a message to the admin (a chat, a group, a channel)

    elif coinmarketcapjson:

        # find the ticker (by name or symbol of the coin) and parsing of json file to show data
        for ticker in coinmarketcapjson:

            if ticker['name'].upper() == message_ticker or \
                            ticker['symbol'].upper() == message_ticker:

                price_usd = '$?'
                price_btc = ''
                rate1h = '?'
                rate1h_emoji = ''
                rate24h = '?'
                rate24h_emoji = ''
                rate7d = '?'
                rate7d_emoji = ''
                marketcap = '$?'

                # to put a header of the message
                msg_parse_api  += msg_title_parse_api(str(ticker['name']), str(ticker['symbol']))

                   # current price
                if ticker['price_usd']:
                    price_usd_float = float(ticker['price_usd'])

                    # for cut paddind zeros at the end of the price
                    if price_usd_float >= 1.0:
                        price_usd = '$' + str(locale.format("%.2f", price_usd_float, True))
                    else:
                        price_usd = '$' + str(locale.format("%.6f", price_usd_float, True)).rstrip('0')

                # current price in BTC (if the ticket is not BTC)
                if ticker['symbol'] != 'BTC':
                    if ticker['price_btc']:
                        price_btc = ' (' + str(locale.format('%.8f', float(ticker['price_btc']), True)) + ' BTC)'

                # 1 hour price change with emoji
                if ticker['percent_change_1h']:
                    rate1h_float = float(ticker['percent_change_1h'])
                    rate1h_emoji = parse_price_change(rate1h_float)
                    rate1h = locale.format('%.2f', rate1h_float, True)

                # 24 hours price change with emoji
                if ticker['percent_change_24h']:
                    rate24h_float = float(ticker['percent_change_24h'])
                    rate24h_emoji = parse_price_change(rate24h_float)
                    rate24h = locale.format('%.2f', rate24h_float, True)

                # 7 days price change with emoji
                if ticker['percent_change_7d']:
                    rate7d_float = float(ticker['percent_change_7d'])
                    rate7d_emoji = parse_price_change(rate7d_float)
                    rate7d = locale.format('%.2f', rate7d_float, True)

                # current market cap
                if ticker['market_cap_usd']:
                    marketcap = '$' + str(locale.format('%.0f', float(ticker['market_cap_usd']), True))

                msg_parse_api += '\nPrice: *' + price_usd + '*' + price_btc \
                    + '\nLast 1 hour changed: *' + rate1h + '%*' + rate1h_emoji \
                    + '\nLast 24 hours changed: *' + rate24h + '%*' + rate24h_emoji \
                    + '\nLast 7 days changed: *' + rate7d + '%*' + rate7d_emoji \
                    + '\nCoinMarketCap rank: *' + str(ticker['rank']) + '*' \
                    + '\nMarket Cap: ' + marketcap + '\n'

        if msg_parse_api == '':
            msg_parse_api += error_ticker()

    else:
        module_logger.error('api.coinmarketcap.com! Error in def parse_api_coinmarketcapjson')
        msg_parse_api += error_information()

        # TODO send a message to the admin (a chat, a group, a channel)

    return '💲 *CoinMarketCap*' + msg_parse_api


# compare percent and add an emoji adequate
def parse_price_change(percent):
    emoji = ''

    if percent > 20:
        emoji = emojize(' :rocket:', use_aliases=True)

    elif percent <= -20.0:
        emoji = emojize(' :sos:', use_aliases=True)

    elif percent < 0:
        emoji = emojize(' :small_red_triangle_down:', use_aliases=True)

    elif percent > 0:
        emoji = emojize(' :white_check_mark:', use_aliases=True)

    return emoji


# to add a title, info of the API parsing with name and ticker of the coin
def msg_title_parse_api(ticker_name, ticker_symbol):

    # is a strange case of token with *, which telegram markdown is provoking an error
    if ticker_symbol.find('*') >= 0:
        ticker_symbol = re.sub(r'[\*]+', '', ticker_symbol)

    # re.sub(...) is to cut all symbols
    msg_parse_api = '\nCoin Name: #' + re.sub(r'[^\S\n\t]+', '', ticker_name).strip() \
                        + '\nTicker: #' + ticker_symbol

    return msg_parse_api


# add a message with info of request problem
def error_information():
    error_text = '\n🇷🇺️ Сожалеем, нет актуальной информации. Повторите Ваш запрос позже!' \
                 '\n🇬🇧 Sorry, there is no actual information now. Please, try again later!\n'
    return error_text


# add a message if there is no ticket
def error_ticker():
    error_text = '\n🇷🇺️ Нет данных по этому тикеру' \
                 '\n🇬🇧 There is no data for this ticker\n'
    return error_text
