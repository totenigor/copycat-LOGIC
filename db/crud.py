from sqlalchemy.orm import Session

from table import Portfolio
from database import SessionLocal

session = SessionLocal()

def create_position(db: Session, symbolCurrent: str, amountCurrent: float, entry_priceCurrent: float, trader_nameCurrent: str):

    new_position = Portfolio(symbol = symbolCurrent,
                             amount = amountCurrent,
                             entry_price = entry_priceCurrent,
                             trader_name = trader_nameCurrent,)

    db.add(new_position)
    db.commit()
    db.refresh()


def