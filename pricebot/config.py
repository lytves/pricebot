import os

# the token of your bot
TOKEN_BOT = '...'

TIME_INTERVAL = 150

URL_COINMARKET_SIMPLE_API = "https://api.coinmarketcap.com/v1/ticker/{}"

COINMARKET_API_URL_COINSLIST = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'

FILE_JSON_COINMARKET = os.path.dirname(os.path.realpath(__file__)) + '/coinmarketcoins.json'


class JSONFiles:
    def __init__(self):
        self.coinmarketcapjson = []

    def change_coinmarketcapjson(self, json1):

        assert isinstance(json1, list)
        self.coinmarketcapjson = json1
        return json1


# the object of class JSONFiles for save json API coins lists
jsonfiles = JSONFiles()
