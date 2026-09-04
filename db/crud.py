from sqlalchemy.orm import Session

from db.table import Portfolio

from backend.position_handling import get_current_price_for_asset as current_price

def create_position(db: Session, symbolCurrent: str, amountCurrent: float, entry_priceCurrent: float, trader_nameCurrent: str):

    new_position = Portfolio(symbol = symbolCurrent,
                             amount = amountCurrent,
                             entry_price = entry_priceCurrent,
                             trader_name = trader_nameCurrent,)

    db.add(new_position)
    db.commit()
    db.refresh(new_position)


def get_position_by_trader(db: Session, trader_nameCurrent: str):
    result = db.query(Portfolio).filter(Portfolio.trader_name == trader_nameCurrent).all()

    return result

def freeze_position(db: Session, trader_nameCurrent: str, current_price: float, ticker: str):
    db.query(Portfolio).filter(Portfolio.trader_name == trader_nameCurrent, Portfolio.entry_price > current_price, Portfolio.symbol == ticker).update({'is_frozen': True})

def get_positive_frozen_positions(db: Session, previousTrader: str):
    frozenPositions = db.query(Portfolio).filter(Portfolio.trader_name == previousTrader, Portfolio.is_frozen == True).all()

    result = [
        position for position in frozenPositions
        if position.entry_price <= current_price(position.symbol)
    ]

    return result