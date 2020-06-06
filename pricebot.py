from telegram.ext import Updater
from telegram.ext import CommandHandler

from pricebot.handlers import price, cap, error, download_api_coinslists_handler, download_api_global_handler
from pricebot.config import TOKEN_BOT, TIME_INTERVAL

from pricebot.parse_apis import module_logger


def main():
    module_logger.info("Start the pricebot!")

    # create an object "bot"
    updater = Updater(token=TOKEN_BOT, use_context=True)
    dispatcher = updater.dispatcher

    # bot's error handler
    dispatcher.add_error_handler(error)

    # bot's command handlers
    price_handler = CommandHandler('p', price)
    dispatcher.add_handler(price_handler)

    cap_handler = CommandHandler('cap', cap)
    dispatcher.add_handler(cap_handler)

    #
    # *** here put the job for the bot ***
    #
    # add tasks to parse CoinMarketCap API to local JSON-files, is used time interval, coz
    # APIs (CMC) have pricing plans with limits
    job_queue = updater.job_queue
    job_queue.run_repeating(download_api_global_handler, TIME_INTERVAL, 5)
    job_queue.run_repeating(download_api_coinslists_handler, TIME_INTERVAL, 10, context='coinmarketcap')

    # for use start_polling() updates method
    updater.start_polling()
    updater.idle()

    # for use start_webhook updates method,
    # see https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
    # updater.start_webhook(listen='127.0.0.1', port=5006, url_path=TOKEN_BOT)
    # updater.bot.set_webhook(url='https://0.0.0.0/' + TOKEN_BOT,
    #                   certificate=open('/etc/nginx/PUBLIC.pem', 'rb'))


if __name__ == '__main__':
    main()
