from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TraderUpdate(BaseModel):
    currentTrader: str
    newTrader: str


@app.post("/trader_change")
def change_trader(data: TraderUpdate):
    print(f"Trader change started. Changing trader from {data.currentTrader} to {data.newTrader}")

    return {"status": "success", "message": f"Changed {data.currentTrader} to {data.newTrader}"}