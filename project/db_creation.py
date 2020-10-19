# Create table schema and engine created to interact with the DB

from sqlalchemy import *
from db_init import engine

meta = MetaData()

environment = Table('environment', meta,
                    # the collection of tables are defined in the MetaData cataloge
                    Column('id', Integer, primary_key=True),
                    Column('date', String(20)),
                    Column('time', String(20)),
                    Column('temperature', Float(20)))

meta.create_all(engine)
