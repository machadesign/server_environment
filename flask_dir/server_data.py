# create a json object from bash scripts / dictionary
# provides all parsed system data , ambient temp provided from sesnsor_probe_info.py

import subprocess
import json
# import ast
# https://www.digitalocean.com/community/tutorials/how-to-use-subprocess-to-run-external-programs-in-python-3

cpu_usage_sys = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/TEST_system_capture_logs.sh"
server_data_file = '/Users/matthewchadwell/server_environment/flask_dir/server_data_dict.json'
temp_diretory = '/Users/matthewchadwell/server_environment/project_tests/test_temp_reading'
config_file_location = '/Users/matthewchadwell/server_environment/project_files/config.json'

result = subprocess.run([cpu_usage_sys], capture_output=True, text=True)
# result = subprocess.run([sys.executable, "-c", "print('ocean')"])
# option to add args to make sjustments edited json file
# -c component is a python command l-c component is a python command
# line option that allows you to pass a string with an entire Python program to executeine option that allows you to


output = result.stdout
text = output.split('\n')
length_of_list = len(text)
# determine length  , number of 'key value'
print(length_of_list)


def bash_to_json():
    file1 = open(server_data_file, "w")
    value = length_of_list
    for i in text:
        if value == length_of_list:
            # if length of entire list of key/values  + '{'
            j = "{"
            file1.writelines(j)
            value -= 1
            print(type(j))
        if value == 1:
            value -= 1
            j = str(i)
            # no need for (,) end of dict
            print(j)
            file1.writelines(j)
        if value > 1 < length_of_list:
            value -= 1
            j = (i + ',')
            # remove ,
            print(j)
            file1.writelines(j)
        if value == 0:
            j = '}'.replace(",", "")
            # j.replace(',', "")
            # remove ,
            # print(j)
            file1.writelines(j)
            value -= 1
            print(j)
    file1.close()


def access_system_data():
    # data excluding data from sensor probe / ambient temp
    with open(server_data_file) as f:
        y = json.load(f)
    system_load_data = y["system_load"]
    gpu_temp_reading_data = y["gpu_temp_reading"]
    # sudo usermod -aG video <username>   , add user name permission to run   vcgencmd
    cpu_temp_reading_data = y["cpu_temp_reading"]
    system_memory_data = y["system_memory"]
    cpu_user_sys_data = y["cpu_user_sys"]
    current_and_uptime_data = y["current_and_uptime"]
    swap_average_use_data = y["swap_average_use"]
    cpu_usage = y["cpu_usage"]
    print(y)
    return system_load_data,gpu_temp_reading_data,cpu_temp_reading_data,system_memory_data,cpu_user_sys_data,\
           current_and_uptime_data,swap_average_use_data,cpu_usage


bash_to_json()

system_load_data, gpu_temp_reading_data, cpu_temp_reading_data, system_memory_data, cpu_user_sys_data, \
current_and_uptime_data, swap_average_use_data,cpu_usage = access_system_data()
print(current_and_uptime_data)

