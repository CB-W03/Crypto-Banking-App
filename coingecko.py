import requests
import json

# base urls for functions of coin-gecko api
simple_url = "https://api.coingecko.com/api/v3/simple"
coins_url = "https://api.coingecko.com/api/v3/coins"
exchange_url = "https://api.coingecko.com/api/v3/exchange_rates"
trending_url = "https://api.coingecko.com/api/v3/search/trending"
global_url = "https://api.coingecko.com/api/v3/global"


def get_coin_price(coin_id, *currencies):
    endpoint = f"/price?ids={coin_id}&vs_currencies="
    currency_string = currencies[0]

    if len(currencies) > 1:
        for i in range(1, len(currencies)):
            currency_string += f"%2C{currencies[i]}"
    request_url = simple_url + endpoint + currency_string
    response = requests.get(request_url)

    if response.status_code == 200:
        coin_price = response.json()
        coin_price = json.dumps(coin_price, indent=1)
        print("currency: price\n")
        print(coin_price[2:-2])
    else:
        print("Error fetching coin price data... Please try again")


def get_currency_list():  # prints list of supported COINS AND CURRENCIES
    endpoint = "/supported_vs_currencies"
    request_url = simple_url + endpoint
    response = requests.get(request_url)

    if response.status_code == 200:
        currency_list = response.json()
        print(currency_list)
    else:
        print("Error fetching list of supported Coins & Currencies... Please try again")


def list_supported_coins():  # specifically crypto
    endpoint = "/list"
    request_url = coins_url + endpoint
    response = requests.get(request_url)

    if response.status_code == 200:
        coins_list = response.json()
        for coin in coins_list:
            print("{")
            print(f"id: {coin['symbol']},")
            print(f"Name: {coin['name']}")
            print("},")
    else:
        print("Error fetching list of coins...Please try again")


def list_coins_data(currency_id, number_of_coins): # lists coins in order of market cap

    endpoint1 = f"/markets?vs_currency={currency_id}&order=market_cap_desc&per_page={number_of_coins}"
    endpoint2 = "&page=1&sparkline=false&locale=en"

    endpoint = endpoint1 + endpoint2
    request_url = coins_url + endpoint
    response = requests.get(request_url)

    if response.status_code == 200:
        coins_data = response.json()

        for coin in coins_data:
            print("{")
            print(f"Name: {coin['name']}")
            print(f"id: {coin['symbol']}")
            print(f"Price in {currency_id}: {coin['current_price']:.2f}")
            print(f"Market Cap: {coin['market_cap']}")
            print(f"Market Rank: {coin['market_cap_rank']}")
            print(f"Price change in last 24h: {coin['price_change_24h']:.3f}")
            print(f"Price change(%): {coin['price_change_percentage_24h']:.3f}%")
            print("},")
    else:
        print("Error fetching coins data...Please try again")


def get_coin_data(coin_id):  # prints data on specific coin
    endpoint = f"/{coin_id}"
    request_url = coins_url + endpoint
    response = requests.get(request_url)

    if response.status_code == 200:
        coin_data = response.json()

        print(f"Name: {coin_data['name']}")
        print(f"id: {coin_data['symbol']}")
        print("Price in other Currencies:")

        for currency, price in coin_data['market_data']['current_price'].items():
            print(f"\t{currency}: {price}")
        print("% Change in price in last 24h:")

        for currency, percentage in coin_data['market_data']['price_change_percentage_24h_in_currency'].items():
            print(f"\t{currency}: {percentage:.4f}%")
    else:
        print("Error fetching coin data...Please try again")


def btc_exchange_rate():
    response = requests.get(exchange_url)

    if response.status_code == 200:
        exchange_rates = response.json()

        for coin, dictionary in exchange_rates['rates'].items():
            print(f"Name: {dictionary['name']}")
            print(f"Currency Sign: {dictionary['unit']}")
            print(f"Cost: {dictionary['value']}\n")
    else:
        print("Error fetching BTC exchange rates...Please try again")


def trending_coins():
    response = requests.get(trending_url)

    if response.status_code == 200:
        trending_coin = response.json()

        for info in trending_coin['coins']:
            print(f"Name: {info['item']['name']}")
            print(f"Symbol: {info['item']['symbol']}")
            print(f"Market Rank: {info['item']['market_cap_rank']}")
            print(f"BTC exchange rate: {info['item']['price_btc']:}\n")
    else:
        print("Error fetching trending coins...Please try again")


def global_data():
    response = requests.get(global_url)

    if response.status_code == 200:
        global_info = response.json()
        global_info = global_info['data']

        print(f"No. of Active Currencies: {global_info['active_cryptocurrencies']}")
        print("Total Market Cap: ")

        for coin, market_cap in global_info['total_market_cap'].items():
            print(f"\t{coin}: {market_cap:.2f}")
        print("Market Cap %:")

        for coin, cap_percentage in global_info['market_cap_percentage'].items():
            print(f"\t{coin}: {cap_percentage:.3f}%")
    else:
        print("Error fetching global crypto data")
