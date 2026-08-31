import requests as rq
import os
from dotenv import load_dotenv

import yfinance as yf
from tr212_to_yfinance_ticker import convert_tr212_to_yfinance

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


def get_current_price_for_asset(symbol: str) -> float:

    try:
        ticker = yf.Ticker(convert_tr212_to_yfinance(symbol))

        currentPrice = ticker.info.get("currentPrice")

        return currentPrice

    except Exception as e:
        print(f"An error occured during function execution: {e}")
