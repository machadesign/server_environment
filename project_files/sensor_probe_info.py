#!/usr/bin/env python

# This script reads,checks the temp and returns it in the intended format
# Input required temp_id to acquire temperature reading for the probe

import re
import DateTime
import json
from reboot_check import round_value


with open('/Users/matthewchadwell/server_environment/config') as r:
    data = json.load(r)

temp_directory = '/Users/matthewchadwell/mock_temp/temp_id/'
# Test - Mock data locally stored in a .txt file


def temp_function(sensor):
    # Return a positive or negative value for temp if CRC is good
    temp_file = temp_directory + sensor
    with open(temp_file) as temp_readline:
        # reads first line of the file , checks CRC(reading good or bad)
        temp_crc = temp_readline.readline()
        temp_crc_check = re.search(r'YES$', temp_crc)
        if temp_crc_check:
            temp_line = temp_readline.readline()
            # read the next line from temp output
            negative_check = re.search(r'(t=-\d*)', temp_line)
# TODO (currently works w/o positive check first,would like to change) positive_check = re.search(r'(t=\d*)', check)
            positive_number = re.findall(r't=(\d*)', temp_line)
            negative_number = re.findall(r't=(-\d*)', temp_line)
            if negative_check is None:
                return positive_number
            elif negative_check:
                return negative_number
            else:
                return 'error'
        else:
            return 999999


def temp_formatted(current_temp):
    if current_temp == 999999:
        temp_error_code = 999999
        return temp_error_code
    else:
        temp_int = int(current_temp[0])
        temp_data = temp_int / 1000
        whole_num_to_float = format(temp_data, '.2f')
        return whole_num_to_float


def return_current_date():
    # returns current date
    current_date = DateTime.DateTime()
    formatted_date = current_date.strftime("%Y-%m-%d")
    return formatted_date


def return_current_time():
    # returns current military time CST
    current_time = DateTime.DateTime()
    formatted_time = current_time.strftime("%H:%M:%S")
    return formatted_time


def return_current_temp(id_sensor):
    temp = temp_function(id_sensor)
    formatted_temp = temp_formatted(temp)
    return formatted_temp


sensor_id = data['sensor_id']
raw_temp = float(return_current_temp(sensor_id))
print(raw_temp)
current_temp = round_value(raw_temp, 'temp_format_round')
print(current_temp)
current_time = return_current_time()
todays_date = return_current_date()