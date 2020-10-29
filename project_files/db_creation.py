#!/usr/bin/env python

# Create table schema and engine created to interact with the DB

from sqlalchemy import *
# from sqlalchemy import MetaData
from db_engine import engine

meta = MetaData()

environment = Table('environment', meta,
                    # the collection of tables are defined in the MetaData cataloge
                    Column('id', Integer, primary_key=True),
                    Column('date', String(20)),
                    Column('time', String(20)),
                    Column('temperature', Float(20)))

meta.create_all(engine)
