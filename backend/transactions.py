import requests as rq
import os
from dotenv import load_dotenv

load_dotenv()

urlSummary = "https://demo.trading212.com/api/v0/equity/account/summary"
urlOrders = "https://demo.trading212.com/api/v0/equity/orders/market"

authorization = {
    "apiId": os.getenv("TR212_API_ID"),
    "apiKey": os.getenv("TR212_API_KEY")
}


def place_order(quantitylocal: float,symbol: str, sellOrBuy: str):

    if sellOrBuy == "sell":
        quantitylocal = -quantitylocal
    elif sellOrBuy == "buy":
        quantitylocal = quantitylocal
    else:
        raise Exception("Please choose option 'buy' or 'sell'")

    payload = {
        "extendHours": True,
        "quantity": quantitylocal,
        "ticker": symbol,
    }

    response = rq.post(urlOrders, json=payload, auth=(authorization["apiId"],authorization["apiKey"]))

    data = response.json()

    if response.status_code == 200:
        print(data)
    else:
        print(f"Err: {response.status_code}")


