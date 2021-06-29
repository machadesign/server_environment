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

config_file_location = '/Users/matthewchadwell/server_environment/project_files/config.json'
temp_directory = '/Users/matthewchadwell/mock_temp/temp_id/'
# Test - Mock data locally stored in a .txt file
arm_cpu_reading = "/Users/matthewchadwell/server_environment/mock_cpu_arm_temp/temp"
get_load_avg = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/load_avg.sh"
get_system_memory_info = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/memory.sh"
get_current_time_andup = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/date_uptime_check.sh"
get_cpu_temperature = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/cpu_temperature.sh"
get_swap_total_used_free = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/used_swap.sh"
get_cpu_usage = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/cpu_usage.sh"
cpu_user_sys = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/cpu_usage_user_kernel.sh"
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
mock_swap_average_use = "Total swap: 1000 Used swap: 200 Free swap: 300"
# mock_swap_page_in_out = "Total swap: 3000 Used swap: 0  Page swap ins: 0 Page swap outs: 0"
mock_cpu_usage = "Cpu idle: 100.00 Io wait: 0.10"
mock_sys_usage = "%user: 0.10 %system: 0.10"
# Time cpu running user code and kernel(system)
mock_ambient_temp = 99.0


# # -------------- COPY  Mock data  ------------------ #
# Mock_GPU_data = "temp=100.670'C"
# Mock_cpu_temp_data = 79670
# Mock_sys_load = "2.94, 2.58, 1.50"
# Mock_memory = "MiB Mem : 7759.2 total, 6718.3 free, 389.0 used, 652.0 buff/cache"
# Mock_date_time_uptime_and_now = '2021-06-08 19:49:56 2021-06-08 19:48:56'
# # data is parsed  with function   return_uptime_check  and   return_current_date_rb_check
# # into values uptime_date, uptime_time, date_and_time, date_now, time_now
# mock_swap_average_use = "Total swap: 33 Used swap: 1000 Free swap: 10000"
# # mock_swap_page_in_out = "Total swap: 3000 Used swap: 0  Page swap ins: 0 Page swap outs: 0"
# mock_cpu_usage = "Cpu idle: 100.92 Io wait: 0.02"
# mock_sys_usage = "%user: 0.01 %system: 0.02"
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
def return_current_dt_and_uptime():
    # get dates,times from bash script
    # current and uptime ,  2021-01-19 20:58:57 2021-01-19 00:45:56
    current_and_uptime = subprocess.Popen([get_current_time_andup], stdout=subprocess.PIPE, universal_newlines=True)
    # return current_and_uptime
    output = current_and_uptime.stdout.readline()
    return output

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

def cpu_temp():

    process = subprocess.Popen([get_cpu_temperature], stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout.readline()
    return output

    # remove this excerpt ---
    # with open(arm_cpu_reading) as cpu_reading:
    #     cpu_temp_reading = cpu_reading.readline()
    #     return cpu_temp_reading


def gpu_temp():
    # format temp=69.0'C
    # sudo usermod -aG video <username>   , add user name permission to run   vcgencmd
    gpu_temperature = os.system('vcgencmd measure_temp')
    return gpu_temperature


def system_load():
    # load_avg.sh
    process = subprocess.Popen([get_load_avg], stdout=subprocess.PIPE, universal_newlines=True)
    # Another thing that you’ll notice is that the output is of type bytes.
    # You can solve that by typing stdout.decode('utf-8') or by adding universal_newlines=True when calling subprocess
    output = process.stdout.readline()
    # reads the first line, otherwise if put readlines would capture all the info and than the response ( 0 or 1 )
    return output

def system_memory():
    # memory.sh  Memory in MiB
    process = subprocess.Popen([get_system_memory_info], stdout=subprocess.PIPE, universal_newlines=True)
    output = process.stdout.readline()
    return output

def return_swap_used():
    current_and_uptime = subprocess.Popen([get_swap_total_used_free], stdout=subprocess.PIPE, universal_newlines=True)
    # return current total,used and free swap
    output = current_and_uptime.stdout.readline()
    return output


def cpu_usage():
    cpu_idle_and_wait = subprocess.Popen([get_cpu_usage], stdout=subprocess.PIPE, universal_newlines=True)
    output = cpu_idle_and_wait.stdout.readline()
    return output

def cpu_usage_us_sys():
    cpu_usage_and_sys = subprocess.Popen([cpu_user_sys], stdout=subprocess.PIPE, universal_newlines=True)
    output = cpu_usage_and_sys.stdout.readline()
    return output


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


