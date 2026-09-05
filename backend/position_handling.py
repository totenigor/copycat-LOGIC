import requests as rq
import os
from dotenv import load_dotenv

import yfinance as yf
from fastapi.params import Depends

from backend.tr212_to_yfinance_ticker import convert_tr212_to_yfinance

from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.table import Portfolio, PreviousTrader
from db.crud import create_position, get_positive_frozen_positions

load_dotenv()

urlSummary = "https://demo.trading212.com/api/v0/equity/account/summary"
urlOrders = "https://demo.trading212.com/api/v0/equity/orders/market"

authorization = {
    "apiId": os.getenv("TR212_API_ID"),
    "apiKey": os.getenv("TR212_API_KEY")
}

def place_order(quantitylocal: float,symbol: str, sellOrBuy: str, traderName: str, db: Session):

    if sellOrBuy == "sell":
        quantitylocal = -quantitylocal
    elif sellOrBuy == "buy":
        quantitylocal = quantitylocal

        try:
            ticker = yf.Ticker(convert_tr212_to_yfinance(symbol))

            currentPrice = ticker.info.get("currentPrice")
        except Exception as e:
            print(f"An error occured during function execution: {e}")
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
        if sellOrBuy == "buy":
            create_position(db, symbol, quantitylocal, currentPrice, traderName)
        elif sellOrBuy == "sell":
            position_to_erase = db.query(Portfolio).filter(Portfolio.trader_name == traderName, Portfolio.symbol == symbol).first()
            db.delete(position_to_erase)
            db.commit()
    else:
        print(f"Err: {response.status_code}")


def get_current_price_for_asset(symbol: str):

    try:
        ticker = yf.Ticker(convert_tr212_to_yfinance(symbol))

        currentPrice = ticker.info.get("currentPrice")

        return currentPrice

    except Exception as e:
        print(f"An error occured during function execution: {e}")


def try_sell_positive_frozen_positions():

    db = SessionLocal()

    try:
        previousTraderOBJ = db.query(PreviousTrader).first()

        if not previousTraderOBJ:
            print("No previous trader available in the database")
            return

        previousTraderSTR = previousTraderOBJ.trader_name

        positive_positions = get_positive_frozen_positions(db,previousTraderSTR)


        if positive_positions:

            positionCount: float = 0
            currEntryPrice: float = 0
            profitSum: float = 0
            for position in positive_positions:
                place_order(position.amount,position.symbol,"sell",previousTraderSTR,db)
                positionCount += 1
                currEntryPrice = position.entry_price
                profitSum += (position.amount * get_current_price_for_asset(position.symbol)) - (currEntryPrice * position.amount)

            print(f"sold {positionCount} positions for overall profit of: {profitSum}")
        else:
            print("No positive frozen positions could be found")

    except Exception as err:
        print(f"encountered an error: {err}")
    finally:
        db.close()