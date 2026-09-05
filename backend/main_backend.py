from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from backend.trader_change import router as tradeRouter

from backend.position_handling import try_sell_positive_frozen_positions as tspfs

import uvicorn


@asynccontextmanager
async def cycle(app: FastAPI):

    print("generuje gazylion dolarow...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(tspfs,trigger='interval',seconds=60)
    scheduler.start()

    yield

    print("przestaje generowac gazylion dolarow")
    scheduler.shutdown()

app = FastAPI(lifespan=cycle)

app.include_router(tradeRouter)

if __name__ == "__main__":
    uvicorn.run("main_backend:app", host="127.0.0.1", port=8000, reload=True)