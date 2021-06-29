#!/usr/bin/env python

# This script reads,checks the ambient temp and returns it
# Input required temp_id to acquire temperature reading for the probe

import re
import json
from gather_data import round_value

# config_file_location = '/Users/matthewchadwell/server_environment/project_files/config.json'
config_json = '/Users/matthewchadwell/server_environment/project_files/config.json'

with open(config_json) as r:
    data = json.load(r)

sensor_id = data['ambient_sensor_id']
mock_temp_directory = '/Users/matthewchadwell/mock_temp/temp_id/'
# Test - Mock data locally stored in a .txt file


def return_ambient_temp():
    # Checks if temperature reading(CRC) good or bad

    temp_file = mock_temp_directory + sensor_id
    with open(temp_file) as temp_readline:
        # reads first line of the file
        # checks if CRC(reading good or bad) ,returns either positive,negative reading or an error
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


def check_and_format_temp(temperature_reading):
    # Returns formatted temp and an error code if there is a bad CRC from the reading

    if temperature_reading == 999999:
        temp_error_code = 999999
        return temp_error_code
    else:
        temp_int = int(temperature_reading[0])
        temp_data = round_value(temp_int / 1000, "round_temp")
        return temp_data


# calls temp function check for good CRC
# calls check return checks/returns error code if error occurs temp, otherwise returns temp formatted
temp = return_ambient_temp()
ambient_temp_reading = check_and_format_temp(temp)
current_ambient_temp = ambient_temp_reading
print(current_ambient_temp)
# return cpu_temp
