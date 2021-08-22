# -------------------------------------------#
# Script calls server values from the DB and
# current reboot count from pickle file
# -------------------------------------------- #

import sqlite3
import pickle
import json


# db_file = '/Users/matthewchadwell/server_environment/project_files/server_environment.db'
db_file = '/Users/matthewchadwell/server_environment/project_files/server_environment.db'

file_location = "/Users/matthewchadwell/server_environment/project_files/"
file_name = 'pickled_file'
pickled_file_location = file_location + file_name

####################################################################
            #configuration values#
####################################################################
with open("/Users/matthewchadwell/server_environment/project_files/config.json") as f:
    data = json.load(f)

    # interval = data["poll_check"]
interval = data["time_check"]

# specify in config.json if true or false , reset counter
reboot_reset = data["reset_reboot_counter"]
print("reboot_reset" + " " + str(reboot_reset))
# (warning level) A specified load avg checked for everytime script runs
one_min_thresh = data["load_average_threshold"]
five_min_thresh = data["load_average_threshold"]
fifteen_min_thresh = data["load_average_threshold"]
warning_one_min = data["load_above_threshold_count"]
warning_five_min = data["load_above_threshold_count"]
warning_fifteen = data["load_above_threshold_count"]


# TODO -- need to handle this with an Try Except if index error occurs

def poll_db_data(db_file):
    # provide a try : and except :  catch an error if failed connecto todb
    # https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
    # 1) create an object (connection to db) , 2) get the cursosr method from the object,
    # 3) execute method on an instance of it - specify query in it's param), 4) close connection to db
    #     poll_db_query = 'SELECT uptime_date, uptime_time, one_min_avg_load , five_min_avg_load , fifteen_min_avg_load , percent_memory_used, percent_of_swap_used, cpu_wait , cpu_idle FROM environment WHERE id=(SELECT max(id) FROM environment);'
    poll_db_query = 'SELECT * FROM environment WHERE id=(SELECT max(id) FROM environment);'
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row   # added

    poll_info = conn.cursor()
    poll_info.execute(poll_db_query)  # added
    result = [dict(row) for row in poll_info.fetchall()]

    # if result:
    #     print(result)
    # for row in poll_info:
    #     print(row)
    print(result[0])
    return result[0]


# def poll_db_data(db_file):
#     # provide a try : and except :  catch an error if failed connecto todb
#     # https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
#     # 1) create an object (connection to db) , 2) get the cursosr method from the object,
#     # 3) execute method on an instance of it - specify query in it's param), 4) close connection to db
#     #     poll_db_query = 'SELECT uptime_date, uptime_time, one_min_avg_load , five_min_avg_load , fifteen_min_avg_load , percent_memory_used, percent_of_swap_used, cpu_wait , cpu_idle FROM environment WHERE id=(SELECT max(id) FROM environment);'
#     poll_db_query = 'SELECT * FROM environment WHERE id=(SELECT max(id) FROM environment);'
#     conn = sqlite3.connect(db_file)
#     conn.row_factory = sqlite3.Row   # added
#
#     poll_info = conn.cursor()
#     poll_info.execute(poll_db_query)  # added
#     result = [dict(row) for row in poll_info.fetchall()]
#     # for row in poll_info:
#     #     print(row)
#     return result[0]


#################################################
# Pickle file check - Reboot & Load warning check
# Get warnings directly from pickle so warning files do not keep incrementing when called by init
##################################################

def read_pickel_get_min_values():
    in_file = open(pickled_file_location, 'rb')
    new_dict = pickle.load(in_file)
    # returns the values form the pickled file , reboot count
    reboot_checkaboot = new_dict["reboot_count"]

    in_file.close()
    return reboot_checkaboot


def read_pickel_check_updated_values():
    # Read the pickled file for amount of times load value exceeded specified, if over warn count throw a warning

    in_file = open(pickled_file_location, 'rb')
    new_dict = pickle.load(in_file)
    in_file.close()
    if new_dict["fifteen_min_thresh"] >= warning_fifteen:
        load_warning = "WARN"
        message = 'Warning for {} or more cycles {} min load greater than {},{} {}'.format(warning_fifteen, interval, fifteen_min_thresh, date_now, time_now)
        return load_warning, message
    if new_dict["five_min_thresh"] >= warning_five_min:
        load_warning = "WARN"
        message = 'Warning for {} or more cycles {} min load greater than {},{} {}'.format(warning_five_min, interval, five_min_thresh, date_now, time_now)
        return load_warning, message
    if new_dict["one_min_thresh"] >= warning_one_min:
        load_warning = "WARN"
        message = 'Warning for {} or more cycles {} min load greater than {},{} {}'.format(warning_one_min, interval, one_min_thresh, date_now, time_now)
        return load_warning, message
    else:
        # catch if load threshold does not exceed , return "No error" not None , None is checked for if data is invalid/possible issue getting load data
        # bad regex check performed in server info area , None returned if so. No error returned her if threshold not met
        message = 'None'
        load_warning = 'None'
        # --TODO check how represented in warning logs
        print(message,load_warning)
        return load_warning, message

# def record_reboot_count_to_config(self, reboot_counto):





config_dict = data
# dict of config


row_data = poll_db_data(db_file)
# dict of db values

date_and_time = row_data['date_and_time']
date_now = row_data['date']
time_now = row_data['time']
uptime_date = row_data['uptime_date']
uptime_time = row_data['uptime_time']
reboot_check = row_data['reboot_check']
ambient_temp = row_data['ambient_temperature']
cpu_temp = row_data['cpu_temperature']
gpu_temp = row_data['gpu_temperature']
one_min_load = row_data['one_min_avg_load']
five_min_load = row_data['five_min_avg_load']
fifteen_min_load = row_data['fifteen_min_avg_load']
memory_used_percent = row_data['percent_memory_used']
swap_used_percent = row_data['percent_of_swap_used']
cpu_user_time = row_data['cpu_user_time']
kernel_use_time = row_data['kernel_time']

cpu_wait_time = row_data['cpu_wait']
cpu_idle = row_data['cpu_idle']

reboot_coutified = read_pickel_get_min_values()
# pickled reboot count

warning, load_message = read_pickel_check_updated_values()
# read the pickled file to get the updated high load and reboot count
message_about_load = load_message
warning_given = warning


print(message_about_load)
print(warning_given)
print(reboot_coutified)







# print(poll_db_data(db_file))
#
#
# print(swap_used_percent)






# pickeled_dict(load_and_reboot_count["reboot_count"])