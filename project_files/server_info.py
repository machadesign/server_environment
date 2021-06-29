#!/usr/bin/env python
# Return the current formatted cpu and gpu temperatures
# Return the system load averages 1,5,15


# - TODO throw errors and send out an email if
# - TODO if memory is running hot return the top consuming PIDs

import re
# import json
from gather_data import round_value
from gather_data import Mock_GPU_data, Mock_cpu_temp_data, Mock_sys_load, Mock_memory,\
    mock_swap_average_use, mock_cpu_usage, mock_sys_usage


config_json = '/Users/matthewchadwell/server_environment/project_files/config.json'

#arm_cpu_reading = "/sys/class/thermal/thermal_zone0/temp"
# location of the cpu data

# -------------------------------------------
# bash scripts assigned to variable names
# -------------------------------------------
# mock_arm_cpu_temp = "68000"
# arm_cpu_temperature = mock_arm_cpu_temp

# directly used -  mock_cpu_usage , mock_swap_average_use, Mock_cpu_temp_data

#
# Mock_GPU_data = "temp=100.99'C"
gpu_temperature = Mock_GPU_data

# Mock_sys_load = "2.94, 2.58, 1.50"
system_load = Mock_sys_load

# Mock_memory = "MiB Mem : 7759.2 total, 6718.3 free, 389.0 used, 652.0 buff/cache"
system_memory = Mock_memory


# arm_cpu_reading = "/Users/matthewchadwell/server_environment/mock_cpu_arm_temp/temp"
# data is found at this location linux  , format  56000


# mock_swap_page_in_out = "Total swap: 3000 Used swap: 0  Page swap ins: 0 Page swap outs: 0"
# Time cpu running user code and kernel(system) code and

def return_cpu_temp(arm_cpu_reading):
    # Mock data / 1000 , no use with bash sript - already in the script. Data format  56000, no need work with a negative number
    #CPU temperature is from Linux directly reading

    # with open(arm_cpu_reading) as arm_readline:
    #     cpu_temp = arm_readline.readline()
    #     temp = int(cpu_temp)
    #     temp_format = temp/1000
    #     rounded_cpu_temp = round_value(temp_format, "round_temp")
    # return rounded_cpu_temp
    temp = int(arm_cpu_reading)
    temp_format = temp/1000
    rounded_cpu_temp = round_value(temp_format, "round_temp")
    return rounded_cpu_temp




def return_gpu_temp(Mock_GPU):
    # GPU temperature is read via the firmware interface  
    gpu_temp_data = re.search(r"(temp=\d*.\d*'C)", Mock_GPU)
    negative_gpu_temp_data = re.search(r"(temp=-\d*.\d*'C)", Mock_GPU)

    gpu_negative_number = re.findall(r'temp=(-\d*.\d*)', Mock_GPU)
    gpu_positive_number = re.findall(r'temp=(\d*.\d*)', Mock_GPU)

    if gpu_temp_data:
        gpu_pos_number = gpu_positive_number[0]
        return round_value(float(gpu_pos_number), "round_temp")
    elif negative_gpu_temp_data:
        gpu_neg_number = gpu_negative_number[0]
        return round_value(float(gpu_neg_number), "round_temp")
    else:
        return "error reading GPU temp"


def return_system_performance(mock_sys_load):
    system = re.search(r"([0-9].[0-9]{2}), ([0-9].[0-9]{2}), ([0-9].[0-9]{2})", mock_sys_load)
    one = float(system[1])
    one_min = float(one)
    five = system[2]
    five_min = float(five)
    fifteen = system[3]
    fifteen_min = float(fifteen)
    one_min_avg_load = round_value(one_min, "round_system_load")
    five_min_avg_load = round_value(five_min, "round_system_load")
    fifteen_min_avg_load = round_value(fifteen_min, "round_system_load")
    return one_min_avg_load, five_min_avg_load, fifteen_min_avg_load



def return_system_memory(Mock_memory):
    # current total memory usage     total memory - ( free + cache + buffer )
    # memory usage  total memory usage / total memory * 100 = current total memory usage
    # Total Memory - (Free + Buffers + Cached) = current total memory usage

    raw_memory = re.search(r"MiB Mem : ([0-9]+.[0-9]+) total, ([0-9]+.[0-9]+) free, [0-9]+.[0-9]+ used, ([0-9]+.[0-9])+ buff\/cache", Mock_memory)
    total_memory = float(raw_memory[1])
    free_memory = float(raw_memory[2])
    buff_cached = float(raw_memory[3])
    free_and_buffer = free_memory + buff_cached
    memory_usage = total_memory - free_and_buffer

    # handle divisible by zero errors
    try:
        calculate_percent_memory_used = int(memory_usage/total_memory * 100)
        rounded_memory_used = round_value(calculate_percent_memory_used, "round_memory")
        rounded_total_memory = round_value(total_memory, "round_memory")
        rounded_memory_usage = round_value(memory_usage, "round_memory")
        return rounded_memory_used, rounded_total_memory, rounded_memory_usage
    except ZeroDivisionError:
        rounded_memory_used,rounded_total_memory,rounded_memory_usage = ["Error", "Error", "Error"]
        return rounded_memory_used,rounded_total_memory,rounded_memory_usage


def return_percent_swap_used(mock_swap_average_use):
    system_swap_data = re.search(r"^Total swap: (\d*) Used swap: (\d*) Free swap: (\d*)$", mock_swap_average_use)
    if system_swap_data is None:
        total_swap, total_used_swap, free_swap = ['', '', '']
        # specify null values in DB accepted for swap values
        print('Regex: Swap data did not match')
        return total_swap, total_used_swap, free_swap
    else:
        try:
            total_swap = int(system_swap_data[1])
            total_used_swap = int(system_swap_data[2])
            calculate_percent_swap_used = total_used_swap / total_swap * 100
            rounded_percent_swap_used = round_value(calculate_percent_swap_used, "round_swap")
            return total_swap, total_used_swap, rounded_percent_swap_used
        except ZeroDivisionError:
            # swap has not been configured for the server
            total_swap, total_used_swap,rounded_percent_swap = [0,0,0]
            print("division by zero! no swap information yet")
            return total_swap,total_used_swap,rounded_percent_swap

def cpu_usage(mock_cpu_usage):
    cpu_idle_wait = re.search(r"^Cpu idle: (\d*.\d*) Io wait: (\d*.\d*)$", mock_cpu_usage)
    cpu_idle = cpu_idle_wait[1]
    cpu_wait = cpu_idle_wait[2]
    if cpu_idle_wait is None:
        cpu_idle, cpu_wait = ['','']
        # --TODO need error handling ,db can only accept float , not string
        print('Regex: Cpu usage data did not match')
        return cpu_idle, cpu_wait
    return cpu_idle, cpu_wait


def user_and_sys_CPU_usage(mock_sys_user):
    user_and_sys = re.search(r"^%user: (\d*.\d*) %system: (\d*.\d*)$", mock_sys_user)
    cpu_time_running_user_code = user_and_sys[1]
    # average since boot
    cpu_time_running_kernel_code = user_and_sys[2]
    return cpu_time_running_user_code, cpu_time_running_kernel_code


one_min_avg_load, five_min_avg_load, fifteen_min_avg_load = return_system_performance(Mock_sys_load)
cpu_temp_reading = return_cpu_temp(Mock_cpu_temp_data)
gpu_temp_reading = return_gpu_temp(gpu_temperature)
percent_memory_used, total_memory, memory_used = return_system_memory(Mock_memory)
print('the' + str(percent_memory_used))

total_swap, total_used, percent_of_swap_used = return_percent_swap_used(mock_swap_average_use)
cpu_idle, cpu_wait = cpu_usage(mock_cpu_usage)
cpu_user_time, kernel_time = user_and_sys_CPU_usage(mock_sys_usage)


# values parsed form system calls

print(percent_memory_used, total_memory, memory_used)
# 5 7759.2 388.9
print(one_min_avg_load, five_min_avg_load,fifteen_min_avg_load)
# 2.9 2.6 1.5
print(cpu_temp_reading)
# 99.67
print(gpu_temp_reading)
# 101.0
print(total_swap, total_used, percent_of_swap_used)
# 0 0 0
print(cpu_user_time, kernel_time)
# 0.01 0.02
print(total_swap, total_used, percent_of_swap_used)
# 33 1000 3030.3