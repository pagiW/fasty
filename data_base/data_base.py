import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlitefile = '../my_data_base.sqlite'

base_dir = os.path.dirname(os.path.realpath(__file__))

url = f'sqlite:///{os.path.join(base_dir, sqlitefile)}'

engine = create_engine(url, echo=True)

sesion = sessionmaker(bind=engine)

Base = declarative_base()