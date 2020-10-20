#!/usr/bin/env python

from db_init import engine
from db_creation import environment
from sensor_info import current_temp, current_time, todays_date


def add_data_to_temp():
    ins = environment.insert().values(date=todays_date, time=current_time, temperature=current_temp)
    connection = engine.connect()
    result = connection.execute(ins)
    print(result)

    
add_data_to_temp()