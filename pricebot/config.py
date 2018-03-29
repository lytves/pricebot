import os

# the token of your bot
TOKEN_BOT = '...'

TIME_INTERVAL = 30

URL_COINMARKET_SIMPLE_API = "https://api.coinmarketcap.com/v1/ticker/{}"

COINMARKET_API_URL_COINSLIST = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'

COINMARKET_API_URL_GLOBAL = 'https://api.coinmarketcap.com/v1/global/'

FILE_JSON_COINMARKET = os.path.dirname(os.path.realpath(__file__)) + '/coinmarketcoins.json'
FILE_JSON_GLOBALINFOAPI = os.path.dirname(os.path.realpath(__file__)) + '/globalinfoapijson.json'


class JSONFiles:
    def __init__(self):
        self.coinmarketcapjson = []
        self.globalinfoapijson = {}

    def change_coinmarketcapjson(self, json1):

        assert isinstance(json1, list)
        self.coinmarketcapjson = json1
        return json1

    def change_globalinfoapijson_json(self, json2):
        assert isinstance(json2, dict)
        self.globalinfoapijson = json2
        return json2


# the object of class JSONFiles for save json API coins lists
jsonfiles = JSONFiles()
