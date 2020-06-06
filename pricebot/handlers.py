import requests
import json

from telegram.ext.dispatcher import run_async

from pricebot.config import *
from pricebot.parse_apis import parse_api_coinmarketcapjson, parse_api_globalinfoapijson, module_logger


# bot's update error handler
def error(update, context):
    module_logger.warning('Update caused error "%s"', context.error)

    # TODO send a message for the admin with error from here


# "/p coin" command's handler
@run_async
def price(update, context):
    """
    the handler of the user command "price"
    """

    usr_chat_id = update.effective_chat.id

    # logging
    if update:
        usr_command = str(update.message.text) if update.message.text else 'None'

        usr_name = update.message.from_user.first_name

        if update.message.from_user.last_name:
            usr_name += ' ' + update.message.from_user.last_name

        if update.message.from_user.username:
            usr_name += ' (@' + update.message.from_user.username + ')'

        module_logger.info("Has received a command \"{}\" from user {}, with id {}".format(usr_command, usr_name, usr_chat_id))
    # logging

    # to concatenate items from the user command
    usr_msg_text = ' '.join(context.args)

    # for always work with a text in a uppercase
    usr_msg_text = usr_msg_text.upper()

    text_response = parse_api_coinmarketcapjson(usr_msg_text)

    """
    if text_response is not empty, bot sends a response to user
    """
    if text_response:
        context.bot.send_message(usr_chat_id, text_response, parse_mode="Markdown")
        module_logger.info("Has sent a message to a channel %s", usr_chat_id)


# "/cap" command's handler
@run_async
def cap(update, context):
    """
    the handler of the user command "price"
    """

    usr_chat_id = update.effective_chat.id

    # logging
    if update:
        usr_command = str(update.message.text) if update.message.text else 'None'

        usr_name = update.message.from_user.first_name

        if update.message.from_user.last_name:
            usr_name += ' ' + update.message.from_user.last_name

        if update.message.from_user.username:
            usr_name += ' (@' + update.message.from_user.username + ')'

        module_logger.info("Has received a command \"{}\" from user {}, with id {}".format(usr_command, usr_name, usr_chat_id))
    # logging

    text_response = parse_api_globalinfoapijson()

    """
    if text_response is not empty, bot sends a response to user
    """
    if text_response:
        context.bot.send_message(usr_chat_id, text_response, parse_mode="Markdown")
        module_logger.info("Has sent a message to a channel %s", usr_chat_id)


# job queue to download CoinMarket API all coins list
@run_async
def download_api_coinslists_handler(context):
    """
    the handler for download the lists of coins from API agregators by job_queue of telegram.ext

    :param  bot: a telegram bot main object
    :type   bot: Bot

    :param  job: job.context is a name of the site-agregator, which has been send from job_queue.run_repeating... method
    :type   job: Job
    """

    module_logger.info('Start a request to %s API', context.job.context)

    response = requests.get(COINMARKET_API_URL_COINLIST.format(CMC_API_KEY))

    # extract a json from response to a class 'dict' or 'list'
    response_dict_list = response.json()

    if response.status_code == requests.codes.ok:

        # check if one of the APIs response is an error
        if 'status' in response_dict_list and response_dict_list['status']['error_code'] != 0:

            error_msg = response_dict_list['status']['error_message']
            module_logger.error('%s error message: %s' % (context.job.context, error_msg))

        else:
            module_logger.info('Success download a coinslist from %s', context.job.context)

            with open(FILE_JSON_COINMARKET, 'w') as outfile:
                json.dump(response_dict_list, outfile)
                module_logger.info('Success save it to %s', FILE_JSON_COINMARKET)

            # save a json to variable
            if context.job.context == 'coinmarketcap':
                jsonfiles.update_cmc_json(response_dict_list)

    else:
        module_logger.error('%s API has not been response successfully', context.job.context)


# job queue to download CoinMarket API Global Data
@run_async
def download_api_global_handler(context):
    """
    the handler for download global Coin Market Cap API Info by job_queue of telegram.ext
    """

    module_logger.info('Start a request to CoinMarketCap API')

    response = requests.get(COINMARKET_API_URL_GLOBAL.format(CMC_API_KEY))

    # extract a json from response to a class 'dict' or 'list'
    response_dict_list = response.json()

    if response.status_code == requests.codes.ok:

        module_logger.info('Success download a global CoinMarketCap JSON API')

        with open(FILE_JSON_GLOBALINFOAPI, 'w') as outfile:
            json.dump(response_dict_list, outfile)
            module_logger.info('Success save it to %s', FILE_JSON_GLOBALINFOAPI)

        jsonfiles.update_globalcmc_json(response_dict_list)

    else:
        module_logger.error('CoinMarketCap JSON API /global not responses successfully')
