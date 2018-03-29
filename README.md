# PriceBot

[@IamCryptobot](https://t.me/IamCryptobot "@IamCryptobot") - enjoy it!

This is a light version of a [CryptoCoinsInfoBot v2 Telegram Bot](https://github.com/lytves/crypto-coins-info-bot-v2 "CryptoCoinsInfoBot v2 Telegram Bot"), it should been used in a group chat to receive a prices of the coins from CoinMarketCap.

Had been used [python-telegram-bot library](https://github.com/python-telegram-bot/python-telegram-bot "python-telegram-bot library Library GitHub Repository"), you can use *start_polling* or *webhook* updates methods for recieve the messages (see pricebot.py code)

For use unicode emojis must be installed [Emoji Library](https://github.com/carpedm20/emoji "Emoji for Python.")

API of [CoinMarketCap](https://coinmarketcap.com/api/ "CoinMarketCap") is used

---

#### Use:

To recive actual price of a crypto coin send a command "/p coin", you can send a coin name and also a coin ticker, you can get global market cap info with a command "/cap" e.g.:

> /p VeChain
> 
> /p OMG
> 
> /p neo
>
> /cap

---

Screenshot of the working bot:

![PriceBot](pricebot.png "PriceBot")
