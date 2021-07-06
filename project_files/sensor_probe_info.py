#!/usr/bin/env python

# This script reads,checks the ambient temp and returns it
# Input required temp_id to acquire temperature reading for the probe

import re
import json
from server_info import round_value
import logging



# https://docs.python.org/3/library/logging.html
FORMAT = '%(levelname)s: %(asctime)-15s %(message)s LINE: %(lineno)d MODULE: %(module)s'

logging.basicConfig(filename="New_erro.log",filemode="a",level=logging.DEBUG, format=FORMAT)
loggerizing = logging
config_file_location = '/Users/matthewchadwell/server_environment/project_files/config.json'

config_json = '/Users/matthewchadwell/server_environment/project_files/config.json'

with open(config_json) as r:
    data = json.load(r)

sensor_id = data['ambient_sensor_id']
mock_temp_directory = '/Users/matthewchadwell/mock_temp/temp_id/'
# Test - Mock data locally stored in a .txt file


def temp_function(sensor_id):
    # get sensor data from it's stored location , from config.json sensor can be changed at users discretion
    try:
        # temp_file = temp_directory + sensor_id
        temp_file = '/Users/matthewchadwell/mock_temp/temp_id/'
        with open(temp_file) as temp_readline:
            # reads first line of the file , checks CRC(reading good or bad)
            temp_crc = temp_readline.readline()
            return temp_crc
    except Exception:
        loggerizing.error("temp crc check error")
        temp_crc = None
        return temp_crc


def return_ambient_temp():
    # Checks if temperature reading(CRC) good or bad
    try:
        temp_file = mock_temp_directory + sensor_id
        with open(temp_file) as temp_readline:
            # reads first line of the file
            # checks if CRC(reading good or bad) ,returns either positive,negative reading or an error
            temp_crc = temp_readline.readline()
            good_temp_crc_check = re.search(r'YES$', temp_crc)
            bad_temp_crc_check = re.search(r'NO$',temp_crc)
            # re.search() searches for the whole string

            if good_temp_crc_check is not None:
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
                    loggerizing.error("ambient temperature data regex mismatch")
                    loggerizing.debug("ambient temperature data regex mismatch", exc_info=True)
                    # debug traceback available determine positive or negative reading error
                    return None
            elif bad_temp_crc_check is not None:
                temp_reading_error = 999999
                return temp_reading_error
            else:
                loggerizing.error("ambient crc regex mismatch")
                return None
    except Exception:
        loggerizing.error("ambient reading error")
        loggerizing.debug("ambient reading error", exc_info=True)
        ambient_reading = None
        return ambient_reading


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
