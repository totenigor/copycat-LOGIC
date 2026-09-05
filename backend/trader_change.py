from fastapi import APIRouter, Depends
from pydantic import BaseModel

from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.table import Portfolio
from db.crud import get_position_by_trader, freeze_position, create_previous_trader

from backend.position_handling import place_order,get_current_price_for_asset
from db.table import PreviousTrader

router = APIRouter()

routerCheckFreeze = APIRouter()

class TraderChange(BaseModel):
    currentTrader: str
    newTrader: str

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/trader-change")
def change_trader(data: TraderChange, db: Session = Depends(get_db)):
    print(f"Trader change started. Changing trader from {data.currentTrader} to {data.newTrader}")

    trader_to_erase = db.query(PreviousTrader).order_by(PreviousTrader.id.asc()).first()

    if trader_to_erase:
        db.delete(trader_to_erase)
        db.commit()
    else:
        print("No trader found to erase")

    all_positions = get_position_by_trader(db, data.currentTrader)

    print(f"Found {len(all_positions)} acquainted to this trader")

    for position in all_positions:

        currentPrice = get_current_price_for_asset(position.symbol)

        if position.entry_price > currentPrice:
            freeze_position(db, data.currentTrader,currentPrice,position.symbol)
        else:
            place_order(position.amount,position.symbol,"sell",data.currentTrader, db)

            db.delete(position)
            print(f"Sold {position.symbol} for {currentPrice-position.entry_price} profit")

    db.commit()

    create_previous_trader(db, data.currentTrader)

    return {"status": "success", "message": f"Changed {data.currentTrader} to {data.newTrader}"}

@router.post("/pull-out")
def pull_out(db: Session = Depends(get_db())):

    currEntryPrice: float = 0
    profitSum: float = 0
    try:

        positions = db.query(Portfolio).all()

        for position in positions:
            place_order(position.amount,position.symbol,"sell",position.trader_name,db)
            currEntryPrice = position.entry_price
            profitSum += (position.amount * get_current_price_for_asset(position.symbol)) - (currEntryPrice * position.amount)

        return {"status": "success", "message": "pull-out from your positions completed", "profit/loss": profitSum}

    except Exception as err:
        return {"status": "error", "message": str(err)}