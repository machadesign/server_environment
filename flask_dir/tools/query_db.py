#!/usr/bin/env python

from sqlalchemy import MetaData
from sqlalchemy.sql import select
from db_engine import engine
from db_creation import environment
import sqlite3

metadata = MetaData()
metadata.bind = engine

db_file_1 = '/Users/matthewchadwell/server_environment/project_files/server_environment.db'
query = 'SELECT uptime_date, uptime_time, one_min_avg_load , five_min_avg_load , fifteen_min_avg_load , percent_memory_used, percent_of_swap_used, cpu_wait , cpu_idle FROM environment WHERE id=(SELECT max(id) FROM environment);'

def query_data(table_name):
    selected_table = select([table_name])
    connect = engine.connect()
    result = connect.execute(selected_table)
    for row in result:
        print(row)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def poll_query(conn):
    curr = conn.cursor()
    print(curr)
    curr.execute(query)

    rows = curr.fetchall()
    for row in rows:
        print(row)

# query_data(environment)


connection = create_connection(db_file_1)
poll_query(connection)
# panda_db_info(db_file_1)
