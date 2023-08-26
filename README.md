# Crypto-Banking-App
A python project I've done using the Coinbase Pro API and Coingecko API to add functionalities of a crypto banking app.
Coinbase Pro deals with real transfers and withdrawals, the sandbox API was used for testing to avoid financial loss however this can be used with the
Real Coinbase pro, you just need to replace the url and use the API key and secret generated from the real Coinbase pro website. However you risk financial loss.
Coingecko deals with the latest market data and information, it was used to display all information for the different coins and gives real-time information. 
There are no coingecko libraries out there so I made a mini library with all the functions I would need to use in the project.
This project taught me a lot about API requests and handling the json responses, and Websockets.

To use this you need a Coinbase account. Then you must go to the Coinbase Pro Website, or the Sandbox Website, and create a new API Key.
You will need to enter your Passphrase, API Key, and API Secret into the given variables in the program or you will be unable to use the features 
Of the Coinbase Pro API.
