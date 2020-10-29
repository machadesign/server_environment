#!/usr/bin/env python

from sqlalchemy import MetaData
from sqlalchemy.sql import select
from db_engine import engine
from db_creation import environment

metadata = MetaData()
metadata.bind = engine


def query_data(table_name):
    selected_table = select([table_name])
    connect = engine.connect()
    result = connect.execute(selected_table)
    for row in result:
        print(row)


query_data(environment)