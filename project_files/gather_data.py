# -------------------------------------------------
# Production env : Script gets the raw data from the server environment and format uptime_date,uptime_time,date_now,time_now,current_date,current_time
#
# System Date
# Temp sensor probe ( Ambient temperature ) data returned from sensor_probe_info.py
# CPU temperature    format:  temp=69.0'C
# GPU temperature    format:  temp=61.99'C
# System load        format:  load average: 0.17, 0.28, 0.26
# System memory      format:  MiB Mem : 7759.2 total, 6718.3 free, 389.0 used, 652.0 buff/cache
# -----------------------------------------------------------

import DateTime
import subprocess
import re
import os
import json

# --------------  System data  ----------------- #
# ambient temperature - from sensor_probe_info import current_ambient_temp , loaction w/ sensor id

# --------------   Mock data  ------------------ #

Mock_GPU_data = "temp=100.000'C"
Mock_cpu_temp_data = 10000
Mock_sys_load = "1.00, 1.00, 1.00"
Mock_memory = "MiB Mem : 50.0 total, 25.0 free, 22.0 used, 8.0 buff/cache"
# NOTE : memory_usage = total_memory - free_and_buffer  , total greater than free
Mock_date_time_uptime_and_now = '2021-06-21 00:20:00 2021-06-21 00:10:00'
# current date/ time   # uptime date / time
# data is parsed  with function   return_uptime_check  and   return_current_date_rb_check
# into values uptime_date, uptime_time, date_and_time, date_now, time_now
Mock_swap_average_use = "Total swap: 1000 Used swap: 200 Free swap: 300"
# mock_swap_page_in_out = "Total swap: 3000 Used swap: 0  Page swap ins: 0 Page swap outs: 0"
Mock_cpu_usage = "Cpu idle: 100.00 Io wait: 0.10"
Mock_sys_usage = "%user: 0.10 %system: 0.10"
# Time cpu running user code and kernel(system)
Mock_ambient_temp = 99.0


# # -------------- COPY  Mock data  ------------------ #
# Mock_GPU_data = "temp=100.670'C"
# Mock_cpu_temp_data = 79670
# Mock_sys_load = "2.94, 2.58, 1.50"
# Mock_memory = "MiB Mem : 7759.2 total, 6718.3 free, 389.0 used, 652.0 buff/cache"
# Mock_date_time_uptime_and_now = '2021-06-08 19:49:56 2021-06-08 19:48:56'
# # data is parsed  with function   return_uptime_check  and   return_current_date_rb_check
# # into values uptime_date, uptime_time, date_and_time, date_now, time_now
# Mock_swap_average_use = "Total swap: 33 Used swap: 1000 Free swap: 10000"
# # mock_swap_page_in_out = "Total swap: 3000 Used swap: 0  Page swap ins: 0 Page swap outs: 0"
# Mock_cpu_usage = "Cpu idle: 100.92 Io wait: 0.02"
# Mock_sys_usage = "%user: 0.01 %system: 0.02"
# # Time cpu running user code and kernel(system) code and






# --TODO create function to be ran at the begining of all processes checks the values of the JSON file
#-- TODO check for a valid json value, int

def round_value(n,json_key):
    # Option to round the CPU temp, GPU temp, Ambient Temp probe , System memory and System load values
    with open(config_file_location) as r:
        data = json.load(r)
        value = round(n, data[json_key])
        return value



# Python datetime module - return current time / date
# def return_current_date_time():
#     # returns current date format  2021/01/19 14:56:8.799679 US/Central
#     current_date = DateTime.DateTime()
#     return current_date
#
# def return_current_date(date_and_time):
#     # returns current date  , return_date()
#     formatted_date = date_and_time.strftime("%Y-%m-%d")
#     # return formatted_date
#     return formatted_date
#
#
# def return_current_time(date_and_time):
#     formatted_time = date_and_time.strftime("%H:%M:%S")
#     # return formatted_time
#     return formatted_time


# -----------------------------  Data from system / bash scripts ---------------------------------#

# Return from system calls  - date_and_time, date_now, time_now, uptime_date, uptime_time

def return_current_date_rb_check(current_and_uptime):
    # parse the return_current_dt_and_uptime  - return date now / time now / date time and now
    date_time = re.search(r'^(\d{4}-\d{2}-\d{2}) (\d*:\d{2}:\d{2}) (\d{4}-\d{2}-\d{2}) (\d*:\d{2}:\d{2})$', current_and_uptime)
    date_now = str(date_time[1])
    time_now = str(date_time[2])
    date_and_time = date_now + ' ' + time_now

    return date_and_time, date_now, time_now


def return_uptime_check(current_and_uptime):
    # parse the return_current_dt_and_uptime   returns uptime time / uptime date
    date_and_time = re.search(r'^(\d{4}-\d{2}-\d{2}) (\d*:\d{2}:\d{2}) (\d{4}-\d{2}-\d{2}) (\d*:\d{2}:\d{2})$', current_and_uptime)
    uptime_date = str(date_and_time[3])
    uptime_time = str(date_and_time[4])

    return uptime_date, uptime_time



def temp_function(sensor_id):
    # get sensor data from it's stored location , sensor id can change users discretion
    temp_file = temp_directory + sensor_id
    with open(temp_file) as temp_readline:
        # reads first line of the file , checks CRC(reading good or bad)
        temp_crc = temp_readline.readline()
        return temp_crc


get_cpu_temp = Mock_cpu_temp_data
# get_gpu_temp = gpu_temp()  # vcgen not recognized

get_gpu_temp = Mock_GPU_data
# get_system_memory = system_memory()

get_system_load = Mock_sys_load
# get_system_load = system_load()

get_system_memory = Mock_memory



# --------------------- Python datetime -------------------- #
# Current date / time from Python date time modul
# date_time = return_current_date_time()

# called from python module
# current_date = return_current_date(date_time)
# current_time = return_current_time(date_time)
# ---------------------------------------------------------- #


uptime_date, uptime_time = return_uptime_check(Mock_date_time_uptime_and_now)
# return date and time from bash script ubuntu config w/ flag s -s
date_and_time, date_now, time_now = return_current_date_rb_check(Mock_date_time_uptime_and_now)
# return date and time from bash script ubuntu config w/ flag s -s


print(get_cpu_temp)
# 79670
print(get_gpu_temp)
# temp=109.670'C
print(get_system_load)
# 1.94, 2.58, 1.50
print(get_system_memory)
# MiB Mem : 7759.2 total, 6718.3 free, 389.0 used, 652.0 buff/cache

print(uptime_date, uptime_time)
# 2021-06-04 19:48:56

print(date_and_time, date_now, time_now)
# 2021-06-04 19:49:56 2021-06-04 19:49:56





