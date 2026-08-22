from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os

baseDir = os.path.dirname(os.path.abspath(__file__))

dbUrl = f"sqlite:///{os.path.join(baseDir, 'bot.db')}"

engine = create_engine(
    dbUrl,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()