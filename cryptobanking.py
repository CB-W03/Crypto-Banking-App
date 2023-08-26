import cbpro
import time
import datetime
import CoinGecko

api_secret = "YOUR API SECRET"
api_key = "YOUR API KEY"
api_pass = "YOUR PASSPHRASE"


class TextWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = 'wss://ws-feed-public.sandbox.pro.coinbase.com'
        self.message_count = 0

    def on_message(self, msg):
        self.message_count += 1
        msg_type = msg.get('type', None)
        if msg_type == 'ticker':
            time_val = msg.get('time',('-'*27))
            parsed_time = datetime.datetime.strptime(time_val, "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_time = parsed_time.strftime("%B %d, %Y %H:%M:%S")
            price_val = msg.get('price',None)
            price_val = float(price_val) if price_val is not None else 'None'
            product_id = msg.get('product_id', None)

            print(f"{formatted_time}\t{price_val:3f} {product_id}")

    def on_close(self):
        print(f"<---Websocket connection closed--->\n\tTotal messages: {self.message_count}")


url = 'https://api-public.sandbox.pro.coinbase.com'  # can also be the real link for cbpro and not sandbox url
client = cbpro.AuthenticatedClient(api_key,
                                   api_secret,
                                   api_pass,
                                   api_url=url)
method_id = ""

currencies = list()
method_ids = list()
payment_methods = client.get_payment_methods()

for method in payment_methods:
    currencies.append(method.get('currency', None))
    method_ids.append(method.get('id', None))


def home_menu():

    print(f"<============Hello {username}============>\n")
    print("1. Withdraw from account")
    print("2. Deposit into account")
    print("3. Check account history")
    print("4. Place market order")
    print("5. View live feed")
    print("6. Find price of coins and more data")
    print("7. Find data for specific coins")
    print("8. Exchange rates for BTC-to-Currency")
    print("9. Find trending coins")
    print("<===================================>")
    print("press 0 to exit\n")
    operator = ""

    try:
        operator = int(input("What would you like to do? "))
    except ValueError:
        print("The input was not a valid choice, please try again...")
        home_menu()

    choose_operation(operator)


def choose_operation(operation):
    match operation:
        case 0:
            print("Exiting...")
            time.sleep(0.5)
            quit()

        case 1:  # withdraw from account
            amount = input("How much would you like to Withdraw? ")
            withdrawal_currency = input("What currency (In this format - USD/EUR/GBP)? ")
            index = currencies.index(withdrawal_currency)
            withdraw(amount, withdrawal_currency, method_ids[index])

        case 2:  # Deposit into account
            amount = input("How much would you like to Deposit? ")
            deposit_currency = input("What currency (In this format - USD/EUR/GBP)? ")  
            index = currencies.index(deposit_currency)
            deposit(amount, deposit_currency, method_ids[index])

        case 3:  # Check account history for given currency
            print("Which currency would you like to check the history for? ")
            currency = input("BTC, ETH, USDC, EUR etc...")
            check_account_history(account_currency=currency)

        case 4:  # Place market order
            buy_or_sell = input("Would you like to buy or sell? (b/s) ")
            if buy_or_sell == 'b':
                buy_or_sell = 'buy'
            elif buy_or_sell == 's':
                buy_or_sell = 'sell'
            else:
                print("invalid choice, returning to home screen...")
                time.sleep(0.5)
                home_menu()
            coin = input(f"What coin would you like to {buy_or_sell}? BTC, ETH, etc... ")
            size = input(f"how much {coin} would you like to {buy_or_sell}? ")
            place_market_order(product_id=coin, buy_or_sell=buy_or_sell, size=size)

        case 5:
            coin = input("What coin would you like to view? BTC/ETH/USDC/etc... ")
            currency = input("What currency would you like to view? EUR/GBP/USD/etc... ")
            view_live_feed(coin, currency)

        case 6:
            currency = input("What currency would you like information on? gbp/usd/eur/etc... ")
            num_of_coins = input("How many coins would you like displayed? ")
            find_coins_data(currency, num_of_coins)

        case 7:
            price = input("Would you like to find ONLY the price? y/n")
            if price.upper() == "Y" or price.upper() == "YES":
                print("Here is a list of supported coins you can query: \n")
                time.sleep(0.5)
                CoinGecko.list_supported_coins()
                coin_query = input("\nWhich coin would you like to query? ")

                print("Here is a list of supported currencies you can query: \n")
                time.sleep(0.5)
                CoinGecko.get_currency_list()

                currency = list()
                print("What currency would you like displayed for the coin? gbp/usd/eur/eth\n")
                choice = input()
                currency.append(choice)

                while True:
                    print("Please enter another currency you want displayed (press 0 to finish)")
                    choice = input()

                    if int(choice) == 0:
                        break
                    else:
                        currency.append(choice)

                print("Fetching info on coin...")
                time.sleep(0.5)
                CoinGecko.get_coin_price(coin_query, currency)

                input("\nPress enter to return to Home Screen")
                print("Returning to Home Screen...")
                time.sleep(0.5)
                home_menu()

            elif price.upper() == "N" or price.upper() == "NO":
                print("Here is a list of supported coins you can query: \n")
                time.sleep(0.5)
                CoinGecko.list_supported_coins()
                coin_query = input("\nWhich coin would you like to query? ")

                find_coin_info(coin_query)
            else:
                print("Error: invalid choice...returning to home screen\n")
                time.sleep(0.5)
                home_menu()

        case 8:
            print("Please Wait...")
            time.sleep(0.3)
            btc_exchange_rate()
        case 9:
            print("Please Wait...")
            time.sleep(0.3)
            trending_coins()


def withdraw(amount, currency_of_amount, meth_id):
    print("Processing withdrawal...")
    client.withdraw(amount, currency_of_amount, meth_id)
    print("Withdrawal successful")

    print("Returning to home screen...\n")
    time.sleep(0.5)
    home_menu()


def deposit(amount, currency_of_amount, meth_id):
    print("Processing Deposit...")
    client.deposit(amount, currency_of_amount, meth_id)
    print("Deposit successful")

    print("Returning to home screen...\n")
    time.sleep(0.5)
    home_menu()


def check_account_history(account_currency):

    accounts = client.get_accounts()
    acc_id = ""
    for acc in accounts:
        currency = acc.get('currency')
        if currency.upper() == f'{account_currency}':
            acc_id = acc.get('id')
    acc_history = client.get_account_history(acc_id)
    history = dict()
    for hist in acc_history:
        history.update({'amount': hist.get('amount'),
                        'balance': hist.get('balance'),
                        'date': hist.get('created_at'),
                        'currencies': hist.get('product_id')
                        })
    for dictionary in history:
        for key, value in dictionary:
            print(f'{key}: {value}')

    time.sleep(2)
    return_to_home = input("Would you like to return to the home screen? (y/n) ")
    if return_to_home.upper() == 'Y':
        home_menu()


def place_market_order(product_id, buy_or_sell, size):
    product_id = f"{product_id}-USD"
    print("Processing order...")
    client.place_market_order(product_id, side=buy_or_sell, size=size)
    print("Order complete!")

    print("Returning to home screen...\n")
    time.sleep(0.5)
    home_menu()


def view_live_feed(coin, currency):
    stream = TextWebsocketClient(products=[f'{coin}-{currency}'], channels=['ticker'])
    stream.start()
    time.sleep(5)
    stream.close()

    choice = input("Would you like to continue viewing the live feed? y/n ")
    if choice.upper() == "Y" or choice.upper() == "YES":
        stream.start()
        time.sleep(5)
        stream.close()
    elif choice.upper() == "N" or choice.upper() == "NO":
        stream.close()
        print("Returning to Home Screen...")
        time.sleep(0.5)
        home_menu()
    else:
        print("incorrect option, returning to Home Screen")
        home_menu()

    print("Press Enter to return to Home Screen...")
    input()
    time.sleep(1)
    home_menu()


def find_coin_info(coin_id):
    print("Fetching coin data...")
    CoinGecko.get_coin_data(coin_id)

    input("\nPress enter to return to Home Screen")
    print("Returning to Home Screen...")
    time.sleep(0.5)
    home_menu()


def find_coins_data(currency, num_of_coins):
    print("Fetching information...")
    time.sleep(0.1)
    print("The coins are listed in order of Market cap descending: \n")
    time.sleep(0.5)
    CoinGecko.list_coins_data(currency, num_of_coins)

    input("\nPress enter to return to Home Screen")
    print("Returning to Home Screen...")
    time.sleep(0.5)
    home_menu()


def btc_exchange_rate():
    print("Fetching exchange rates...")
    CoinGecko.btc_exchange_rate()

    input("\nPress enter to return to Home Screen")
    print("Returning to Home Screen...")
    time.sleep(0.5)
    home_menu()


def trending_coins():
    print("Fetching data for trending coins...\n")
    CoinGecko.trending_coins()

    input("\nPress Enter to return to Home Screen")
    print("Returning to Home Screen")
    time.sleep(0.5)
    home_menu()


username = input("What is your name/username? ")
home_menu()
