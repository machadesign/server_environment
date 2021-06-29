# create a json object from bash scripts / dictionary
import subprocess
import json
import ast
# https://www.digitalocean.com/community/tutorials/how-to-use-subprocess-to-run-external-programs-in-python-3

cpu_usage_sys = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/system_capture_logs.sh"
server_data_file = '/Users/matthewchadwell/server_environment/flask_dir/server_data_dict.json'

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


try:
    with open(server_data_file, 'r') as fp:
        accounts = json.load(fp)
except IOError:
    print('server_data_dict not found, creating one')
    file1 = open(server_data_file, "w")


def bash_to_json():
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

bash_to_json()
# with open("myfile.txt") as f:
#     f.readline()
# print(f)


# # initializing string
# test_string = '{"Nikhil" : 1, "Akshat" : 2, "Akash" : 3}'
#
# # printing original string
# print("The original string : " + str(test_string))
#
# # using ast.literal_eval()
# # convert dictionary string to dictionary
# res = ast.literal_eval(test_string)



# data excluding data from sensor probe / ambient temp
with open(server_data_file) as f:
    y = json.load(f)
test_value = y["cpu_user_sys"]

print(test_value)
print(type(test_value))
