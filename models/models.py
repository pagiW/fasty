from data_base.data_base import Base
from sqlalchemy import Column, String, Integer

class Games(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    console = Column(String)
    realized = Column(Integer)