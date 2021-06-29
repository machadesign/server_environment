#!/usr/bin/env python

# from gather_data import current_time
from db_engine import engine
from db_creation import environment

from gather_data import date_now, time_now, uptime_date, uptime_time, date_and_time
# mock ambient
from gather_data import mock_ambient_temp
# real data
# from sensor_probe_info import ambient_temp_reading

from reboot_check import reboot_counted
from server_info import cpu_temp_reading, gpu_temp_reading, one_min_avg_load, five_min_avg_load, fifteen_min_avg_load, \
    percent_memory_used, cpu_idle,cpu_wait, percent_of_swap_used, kernel_time, cpu_user_time




def add_data_to_temp():
    ins = environment.insert().values(
                                      date_and_time=date_and_time,
                                      date=date_now,
                                      time=time_now,
                                      uptime_date=uptime_date,
                                      uptime_time=uptime_time,
                                      reboot_check=reboot_counted,
                                      one_min_avg_load=one_min_avg_load,
                                      five_min_avg_load=five_min_avg_load,
                                      fifteen_min_avg_load=fifteen_min_avg_load,
                                      # ambient_temperature=ambient_temp_reading,
                                      # real amb temp
                                      ambient_temperature=mock_ambient_temp,
                                      # mock amb temp
                                      cpu_temperature=cpu_temp_reading,
                                      gpu_temperature=gpu_temp_reading,
                                      percent_memory_used=percent_memory_used,
                                      percent_of_swap_used=percent_of_swap_used,
                                      cpu_idle=cpu_idle,
                                      cpu_wait=cpu_wait,
                                      cpu_user_time=cpu_user_time,
                                      kernel_time=kernel_time
                                      )

    connection = engine.connect()
    result = connection.execute(ins)

    print(result)

# Way to handle multiple tables  (example)
# environment = Table('environment', meta,
#                     # the collection of tables are defined in the MetaData cataloge
#                     Column('id', Integer, primary_key=True),



add_data_to_temp()

