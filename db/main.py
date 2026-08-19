from database import Base, engine
from table import Portfolio

Base.metadata.create_all(engine)