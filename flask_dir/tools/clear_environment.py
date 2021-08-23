import os
from os import path
import pickle
import json
import sqlite3


DATABASE = '/Users/matthewchadwell/server_environment/project_files/server_environment.db'


conn = sqlite3.connect(DATABASE)
# provide location file
# check if file exists , if not create file


def trucate_table():
    conn = sqlite3.connect(DATABASE)
    query = "delete from environment;"
    conn.execute(query)
    conn.commit()
    print("db cleared")
    # for i in query:
    #     print(i)
    conn.close()

def pickled_file_location():
    file_location = "/Users/matthewchadwell/server_environment/project_files/"
    file_name = 'pickled_file'
    pickled_file_location = file_location + file_name
    return pickled_file_location

def store_data_set_to_zero(file_location):
    # write to the pickeled file with the updated high load incrementer global count and reboot count
    reset_value = 0
    load_and_reboot_count = {}
    load_and_reboot_count["one_min_thresh"] = reset_value
    load_and_reboot_count["five_min_thresh"] = reset_value
    load_and_reboot_count["fifteen_min_thresh"] = reset_value
    load_and_reboot_count["reboot_count"] = reset_value
    outfile = open(file_location, 'wb')  # write , byte format
    # open file for writing
    pickle.dump(load_and_reboot_count, outfile)
    # object want to pickle and file to which to save it to

    outfile.close()
    print('check' + str(load_and_reboot_count))

def check_if_pickeled_file_exist(file_location):
    # this checks if the file exists however does not check if it is empty , If file is empty Ran out of input error occurs
    # creates the pickled file if it doesn't exist and first server check performed / first server reading saved to the file
    if path.exists(file_location) and os.stat(file_location).st_size != 0:
        print("file exists and has data")
    else:
        print("no file, or file does not have any data")
        store_data(file_location)
        # no file create a pickled file with data

# file created with zero values, reset

def read_pickel_get_min_values(file_location):
    # read pickled file and assign these values to the global variables
    in_file = open(file_location, 'rb')
    new_dict = pickle.load(in_file)
    # returns the values form the pickled file

    print(new_dict["one_min_thresh"],new_dict["five_min_thresh"],new_dict["five_min_thresh"],new_dict["fifteen_min_thresh"],new_dict["reboot_count"])
    in_file.close()

def clear_warning_log():
    warning_log_file = "/Users/matthewchadwell/server_environment/flask_dir/static/warning_log.txt"

    with open(warning_log_file, 'r+') as f:
        f.truncate(0)
        print("warnings log cleared")


trucate_table()
location_file = pickled_file_location()
check_if_pickeled_file_exist(location_file)
store_data_set_to_zero(location_file)
clear_warning_log()


