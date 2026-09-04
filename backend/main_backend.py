from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from backend.trader_change import router as tradeRouter

import uvicorn


@asynccontextmanager
async def cycle(app: FastAPI):

    print("generuje gazylion dolarow...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(BigMoney,trigger='interval',seconds=15, args=["AAPL_US_EQ"])
    scheduler.start()

    yield

    print("przestaje generowac gazylion dolarow")
    scheduler.shutdown()

app = FastAPI(lifespan=cycle)

app.include_router(tradeRouter)

if __name__ == "__main__":
    uvicorn.run("main_backend:app", host="127.0.0.1", port=8000, reload=True)