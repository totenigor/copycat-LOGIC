from sqlalchemy import Column, Integer, String, Float, Boolean

from db.database import Base

class Portfolio(Base):
    __tablename__ = "portfolio"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    amount = Column(Float)
    entry_price = Column(Float)
    trader_name = Column(String)
    is_frozen = Column(Boolean, default = False)

class PreviousTrader(Base):
    __tablename__ = "previous_trader"
    id = Column(Integer, primary_key=True)
    trader_name = Column(String)