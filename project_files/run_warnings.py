# from server_info import gpu_temp_reading, cpu_temp_reading, percent_memory_used, percent_of_swap_used
# from gather_data import current_date, current_time
# from sensor_probe_info import current_ambient_temp


from reboot_check import reboot_counted
# need to find out where getting value

# from reboot_check import single_reboot_count
from Load_and_reboot_check import message_about_load


from poll_data import date_and_time, date_now, time_now, uptime_date, uptime_time, reboot_check, ambient_temp, cpu_temp, gpu_temp, \
    memory_used_percent, cpu_idle, swap_used_percent, cpu_wait_time, cpu_idle



import json
import sys
import os
import smtplib
import getpass
#
# mail_pass = getpass.getpass('Password')


# multiple errors can be given at poll
list_of_warnings = []

config_json = '/Users/matthewchadwell/server_environment/project_files/config.json'
warning_log = '/Users/matthewchadwell/server_environment/flask_dir/static/warning_log.txt'


# "Contact_email": "svp.chadwell@gmail.com",
# "Sender_email": "svp.chadwell@gmail.com",


with open(config_json) as f:
    data = json.load(f)
    contact_email = data["Contact_email"]
    sender_email = data["Sender_email"]
    # --TODO check if user wants warnings on at all ,and if so display warning options
    # warning_check = data["Warning_check"]

    cpu_temp_warn = data["cpu_temp_warning"]
    # cpu_temp_warn_float = float(cpu_temp_warn)

    gpu_temp_warn = data["gpu_temp_warning"]
    # gpu_temp_warn_float = float(gpu_temp_warn)
    ambient_temp_warn = data["ambient_temp_warning"]
    # ambient_temp_warn_float = float(ambient_temp_warn)

    percent_memory_warning = data["percent_memory_warning"]
    percent_swap_warning = data["percent_swap_warning"]

    reboot_warning = data["reboot_warning"]
    poll_check = data["poll_check"]

    cpu_idle_warn = data["cpu_idle"]
    cpu_wait_warn = data["cpu_wait"]



# if data["Warning_check"] is True:
# if there are multiple conditions udner a section , for instance load - can specify another if data["load_warnin_ckeck"] before evaluating each load condition */

    # ----------- temperature check -------------- #
    # check if temperature exceeds provided temp in config json file
    print(str(cpu_temp) + ">=" + str(cpu_temp_warn))
    if cpu_temp >= cpu_temp_warn:

        # print(str(cpu_temp) + ">=" + str(cpu_temp_warn))
        list_of_warnings.append("CPU temperature" + " " + str(cpu_temp) + "," + str(date_now) + " " + str(time_now))
    if gpu_temp >= gpu_temp_warn:
        list_of_warnings.append("GPU temperature" + " " + str(gpu_temp) + "," + str(date_now) + " " + str(time_now))
    if ambient_temp >= ambient_temp_warn:
        list_of_warnings.append("Ambient temperature" + " " + str(ambient_temp) + "," + str(date_now) + " " + str(time_now))

    # ------------ Percent of memory/swap used ----------- #

    if memory_used_percent >= percent_memory_warning:
        print("memory high")
        # check print(str(cpu_temp) + ">=" + str(cpu_temp_warn))
        list_of_warnings.append("Memory used" + " " + str(memory_used_percent) + "," + str(date_now) + " " + str(time_now))

    if swap_used_percent >= percent_swap_warning:
        print("swap high")
        list_of_warnings.append("Swap used" + " " + str(swap_used_percent) + "," + str(date_now) + " " + str(time_now))

    # ------------ Load warning  ----------- #

    if message_about_load is not None:
        list_of_warnings.append(message_about_load)
        print(message_about_load)

    # ------------ Reboot warning ----------- #

    if reboot_warning == "ON":
        # previosu issue == was is
        # reboot warnings checked on by user
        if reboot_counted == 1:
            list_of_warnings.append("Reboot occurred" + "," + str(date_now) + " " + str(time_now))

    # ------------ Cpu idle / wait ----------- #

    if cpu_idle >= cpu_idle_warn:
        print("HIGH cpu_idle_high")
        # check print(str(cpu_temp) + ">=" + str(cpu_temp_warn))
        list_of_warnings.append("Cpu idle" + " " + str(memory_used_percent) + "," + str(date_now) + " " + str(time_now))

    if cpu_wait_time >= cpu_wait_warn:
        print("HIGH cpu_wait_time")
        list_of_warnings.append("Wait time" + " " + str(swap_used_percent) + "," + str(date_now) + " " + str(time_now))


# def display_list():
#     print(list_of_warnings)


    # message from current list of warnings
# TODO -- Add functionality warnings sent - sms message
# At poll function gathers most current warnings displayed and sent in an email
# def display_list():
#     # make a direct SMTP connection over SSL/TLS to server.
#     mail_server = smtplib.SMTP_SSL('smtp.example.com')
#     # see any warnings
#     mail_server.set_debuglevel(1)
#
#     mail_server.login(sender, mail_pass)
#     # for i in list_of_warnings:
#
#     mail_server.send_message(message)
#
#     print(list_of_warnings)


def edit_file(log_file):
    if os.path.exists(log_file):
        # append just occurred warnings to it
        editing = "a"
    else:
        editing = "w"
    return editing


def work_with_file(log_file,a_or_w):
    with open(log_file, a_or_w) as file:
        # with open , opens file and closes file for you no need to .close
        for i in list_of_warnings:
            file.write(i + "\n")
            # file.(write) is specified same for "a" and "w"
    print(list_of_warnings)

# def send_email():
# display_list()


to_append_or_create_and_write = edit_file(warning_log)
work_with_file(warning_log, to_append_or_create_and_write)



