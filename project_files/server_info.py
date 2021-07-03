#!/usr/bin/env python
# Returns formatted CPU temp , GPU temp, SYS load, Memory, Swap , CPU usage, CPU idle and wait


# - TODO if memory is running hot return the top consuming PIDs

import re
import logging
# import json
from gather_data import round_value
from gather_data import Mock_GPU_data, Mock_cpu_temp_data, Mock_memory,\
    mock_swap_average_use, mock_sys_usage, mock_cpu_usage, Mock_sys_load


# https://docs.python.org/3/library/logging.html
FORMAT = '%(levelname)s: %(asctime)-15s %(message)s LINE: %(lineno)d MODULE: %(module)s'
logging.basicConfig(filename="New_erro.log",filemode="a",level=logging.DEBUG, format=FORMAT)
loggerizing = logging
config_json = '/Users/matthewchadwell/server_environment/project_files/config.json'


def return_cpu_temp(arm_cpu_reading):
    # Mock data / 1000 , no use with bash sript - already in the script. Data format  56000, no need program for negative number
    # Regex not needed - CPU temperature is from Linux directly reading
    try:
        temp = int(arm_cpu_reading)
        temp_format = temp/1000
        rounded_cpu_temp = round_value(temp_format, "round_temp")
        return rounded_cpu_temp
    except Exception:
        loggerizing.error("arm cpu reading error")
        loggerizing.debug("arm cpu reading error", exc_info=True)

def return_gpu_temp(Mock_GPU):
    # GPU temperature is read via the firmware interface
    try:
        gpu_temp_data = re.search(r"(temp=\d*.\d*'C)", Mock_GPU)
        negative_gpu_temp_data = re.search(r"(temp=-\d*.\d*'C)", Mock_GPU)

        gpu_negative_number = re.findall(r'temp=(-\d*.\d*)', Mock_GPU)
        gpu_positive_number = re.findall(r'temp=(\d*.\d*)', Mock_GPU)

        if gpu_temp_data is not None:
            gpu_pos_number = gpu_positive_number[0]
            return round_value(float(gpu_pos_number), "round_temp")
        elif negative_gpu_temp_data is not None:
            gpu_neg_number = gpu_negative_number[0]
            return round_value(float(gpu_neg_number), "round_temp")
        else:
            loggerizing.error(msg="Load data regex mismatch")
            gpu_temp = "NULL"
            return gpu_temp
    except Exception:
        loggerizing.error("gpu temp reading error")
        loggerizing.debug("gpu temp reading error", exc_info=True)
        gpu_temp = "NULL"
        return gpu_temp


def return_system_performance(mock_sys_load):
    try:
        system = re.search(r"([0-9].[0-9]{2}), ([0-9].[0-9]{2}), ([0-9].[0-9]{2})", mock_sys_load)
        if system is not None:
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
        else:
            loggerizing.error(msg="Load data regex mismatch")
            one_min_avg_load_err, five_min_avg_load_err, fifteen_min_avg_load_err = ["NULL", "NULL", "NULL"]
            return one_min_avg_load_err, five_min_avg_load_err, fifteen_min_avg_load_err
    except Exception:
        loggerizing.error("system load read error")
        loggerizing.debug("system laod read error", exc_info=True)
        one_min_avg_load_err, five_min_avg_load_err, fifteen_min_avg_load_err = ["NULL", "NULL", "NULL"]
        return one_min_avg_load_err, five_min_avg_load_err, fifteen_min_avg_load_err




def return_system_memory(Mock_memory):
    # current total memory usage     total memory = ( free + cache + buffer )
    # memory usage  total memory usage / total memory * 100 = current total memory usage
    # Total Memory - (Free + Buffers + Cached) = memory used
    try:
        raw_memory = re.search(r"MiB Mem : ([0-9]+.[0-9]+) total, ([0-9]+.[0-9]+) free, [0-9]+.[0-9]+ used, ([0-9]+.[0-9])+ buff\/cache", Mock_memory)
        if raw_memory is not None:
            total_memory = float(raw_memory[1])
            free_memory = float(raw_memory[2])
            buff_cached = float(raw_memory[3])
            free_and_buffer = free_memory + buff_cached
            memory_usage = total_memory - free_and_buffer
        # handle divisible by zero errors
            calculate_percent_memory_used = int(memory_usage/total_memory * 100)
            rounded_memory_used = round_value(calculate_percent_memory_used, "round_memory")
            rounded_total_memory = round_value(total_memory, "round_memory")
            rounded_memory_usage = round_value(memory_usage, "round_memory")
            return rounded_memory_used, rounded_total_memory, rounded_memory_usage
        else:
            loggerizing.error(msg="memory data regex mismatch")
            rounded_memory_used, rounded_total_memory, rounded_memory_usage = ["NULL", "NULL", "NULL"]
            return rounded_memory_used, rounded_total_memory, rounded_memory_usage
    except Exception:
        loggerizing.error("memory read error")
        loggerizing.debug("memory read error", exc_info=True)
        rounded_memory_used, rounded_total_memory, rounded_memory_usage = ["NULL", "NULL", "NULL"]
        return rounded_memory_used, rounded_total_memory, rounded_memory_usage

def return_percent_swap_used(mock_swap_average_use):
    # swap data handled if zero swap ,otherwise if data error NULL returned
    try:
        system_swap_data = re.search(r"^Total swap: (\d*) Used swap: (\d*) Free swap: (\d*)$", mock_swap_average_use)
        if system_swap_data is not None:
            try:
                total_swap = int(system_swap_data[1])
                total_used_swap = int(system_swap_data[2])
                calculate_percent_swap_used = total_used_swap / total_swap * 100
                rounded_percent_swap_used = round_value(calculate_percent_swap_used, "round_swap")
                return total_swap, total_used_swap, rounded_percent_swap_used
            except ZeroDivisionError:
                # swap has not been configured for the server
                total_swap_zero, total_used_swap_zero, rounded_percent_swap_zero = [0, 0, 0]
                print("division by zero! no swap information yet")
                return total_swap_zero, total_used_swap_zero, rounded_percent_swap_zero
        else:
            loggerizing.error(msg="swap regex mismatch")
            total_swap, total_used_swap, rounded_percent_swap_used = ["NULL", "NULL", "NULL"]
            return total_swap, total_used_swap, rounded_percent_swap_used
    except Exception:
        loggerizing.error("swap read error")
        loggerizing.debug("swap read error", exc_info=True)
        total_swap_err, total_used_swap_err, rounded_percent_swap_used_err = ["NULL", "NULL", "NULL"]
        return total_swap_err, total_used_swap_err, rounded_percent_swap_used_err


def cpu_idle_wait(mock_cpu_usage):
    try:
        cpu_idle_wait = re.search(r"^Cpu idle: (\d*.\d*) Io wait: (\d*.\d*)$", mock_cpu_usage)
        if cpu_idle_wait is not None:
            cpu_idle_data = cpu_idle_wait[1]
            cpu_wait_data = cpu_idle_wait[2]
            return cpu_idle_data, cpu_wait_data
        else:
            loggerizing.error(msg="swap regex mismatch")
            cpu_idle_err, cpu_wait_err = ["NULL", "NULL"]
            return cpu_idle_err, cpu_wait_err
    except Exception:
        loggerizing.error("cpu ilde_wait read error")
        loggerizing.debug("cpu ilde_wait read error", exc_info=True)
        cpu_idle_err, cpu_wait_err = ["NULL", "NULL"]
        return cpu_idle_err, cpu_wait_err


def user_and_sys_usage(mock_sys_user):
    try:
        user_and_sys = re.search(r"^%user: (\d*.\d*) %system: (\d*.\d*)$", mock_sys_user)
        if user_and_sys is not None:
            cpu_time_running = user_and_sys[1]
            # average since boot
            cpu_time_running_kernel = user_and_sys[2]
            return cpu_time_running, cpu_time_running_kernel
        else:
            loggerizing.error(msg="user_system reading regex mismatch")
            cpu_idle_err, cpu_wait_err = ["NULL", "NULL"]
            return cpu_idle_err, cpu_wait_err
    except Exception:
        loggerizing.error("user_system read error")
        loggerizing.debug("user_system read error", exc_info=True)
        user_usage_err, cpu_usage_err = ["NULL", "NULL"]
        return user_usage_err, cpu_usage_err




one_min_avg_load, five_min_avg_load, fifteen_min_avg_load = return_system_performance(Mock_sys_load)
cpu_temp_reading = return_cpu_temp(Mock_cpu_temp_data)
gpu_temp_reading = return_gpu_temp(gpu_temperature)
percent_memory_used, total_memory, memory_used = return_system_memory(Mock_memory)
print('the' + str(percent_memory_used))

total_swap, total_used, percent_of_swap_used = return_percent_swap_used(mock_swap_average_use)
cpu_idle, cpu_wait = cpu_idle_wait(mock_cpu_usage)
cpu_user_time, kernel_time = user_and_sys_usage(mock_sys_usage)


# values parsed form system calls

print(percent_memory_used, total_memory, memory_used)
# 5 7759.2 388.9
print(one_min_avg_load, five_min_avg_load,fifteen_min_avg_load)
# 2.9 2.6 1.5
print(cpu_temp_reading)
# 99.67
print(gpu_temp_reading)
# 101.0
print(mock_swap_average_use)
print(total_swap, total_used, percent_of_swap_used)
# 0 0 0
print(cpu_user_time, kernel_time)
# 0.01 0.02
