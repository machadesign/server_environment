#!/usr/bin/env python

# from gather_data import current_time
# from db_engine import engine
# from db_creation import environment

# from gather_data import date_now, time_now, uptime_date, uptime_time, date_and_time

# mock ambient
#from gather_data import Mock_ambient_temp
# real data
# from sensor_probe_info import ambient_temp_reading

# from reboot_check import reboot_counted
# from server_info import cpu_temp_reading, gpu_temp_reading, one_min_avg_load, five_min_avg_load, fifteen_min_avg_load, \
#     percent_memory_used, cpu_idle,cpu_wait, percent_of_swap_used, kernel_time, cpu_user_time

from db_engine import engine
from db_creation import environment

from server_info import uptime_date,uptime_time,date_now,time_now,date_and_time
from server_info import cpu_temp_reading, gpu_temp_reading, one_min_avg_load, five_min_avg_load, fifteen_min_avg_load, \
    percent_memory_used, cpu_idle,cpu_wait, percent_of_swap_used, kernel_time, cpu_user_time
from sensor_probe_info import current_ambient_temp
from reboot_check import reboot_counted


def add_data_to_temp():
    ins = environment.insert().values(
                                      date=date_now,
                                      time=time_now,
                                      uptime_date=uptime_date,
                                      uptime_time=uptime_time,
                                      reboot_check=reboot_counted,
                                      ambient_temperature=current_ambient_temp,
                                      cpu_temperature=cpu_temp_reading,
                                      gpu_temperature=gpu_temp_reading,
                                      one_min_avg_load=one_min_avg_load,
                                      five_min_avg_load=five_min_avg_load,
                                      fifteen_min_avg_load=fifteen_min_avg_load,
                                      percent_memory_used=percent_memory_used,
                                      cpu_wait=cpu_wait,
                                      cpu_idle=cpu_idle,
                                      percent_of_swap_used=percent_of_swap_used,
                                      cpu_user_time=cpu_user_time,
                                      kernel_time=kernel_time,
                                      date_and_time=date_and_time,
                                      )


    connection = engine.connect()
    result = connection.execute(ins)

    print(result)

# Way to handle multiple tables  (example)
# environment = Table('environment', meta,
#                     # the collection of tables are defined in the MetaData cataloge
#                     Column('id', Integer, primary_key=True),



add_data_to_temp()

