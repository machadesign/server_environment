# -------------------------------------------#
# Script calls server values from the sql db and
# current reboot count from pickle file
# -------------------------------------------- #

import sqlite3
import pickle



# db_file = '/Users/matthewchadwell/server_environment/project_files/server_environment.db'
db_file = '/Users/matthewchadwell/server_environment/project_files/server_environment.db'

file_location = "/Users/matthewchadwell/server_environment/project_files/"
file_name = 'pickled_file'
pickled_file_location = file_location + file_name


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


def read_pickel_get_min_values():
    in_file = open(pickled_file_location, 'rb')
    new_dict = pickle.load(in_file)
    # returns the values form the pickled file
    reboot_checkaboot = new_dict["reboot_count"]

    in_file.close()
    return reboot_checkaboot



row_data = poll_db_data(db_file)
# dcitionary of queried values
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

print(poll_db_data(db_file))


print(swap_used_percent)


reboot_coutified = read_pickel_get_min_values()
print(type(reboot_coutified))



# pickeled_dict(load_and_reboot_count["reboot_count"])