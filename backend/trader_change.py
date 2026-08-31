from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.crud import get_position_by_trader

app = FastAPI()

class TraderChange(BaseModel):
    currentTrader: str
    newTrader: str

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.post("/trader_change")
def change_trader(data: TraderChange, db: Session = Depends(get_db)):
    print(f"Trader change started. Changing trader from {data.currentTrader} to {data.newTrader}")

    all_positions = get_position_by_trader(db, data.currentTrader)

    print(f"Found {len(all_positions)} acquainted to this trader")

    for position in all_positions:


    return {"status": "success", "message": f"Changed {data.currentTrader} to {data.newTrader}"}