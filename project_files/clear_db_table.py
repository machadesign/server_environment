#!/usr/bin/env python

from sqlalchemy import *
from db_init import engine
from db_creation import environment

metadata = MetaData()
metadata.bind = engine
# access table information


def clear_table():
    con = engine.connect()
    trans = con.begin()

    for name, table in metadata.tables.items():
        print(table.delete())
    con.execute(environment.delete())
    trans.commit()

clear_table()