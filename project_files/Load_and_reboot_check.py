# - TODO throw errors and send out an email if load is high
# - TODO if memory is running hot return the top consuming PIDs
# script pickles / saves the high load and reboot count
# Returns the high load count where the load consistently surpasses the threshold (specified in config.json) , be mindful of the interval script si ran better reprsentation for data tested
# (User has the option (change the interval) in the config.json file to monitor a single load every min, five or fifteen)
# Returns a reboot count for every time the system rebooted
# (User can reset the count back to zero fron config.json)
# warning file calls for

import os
from os import path
import pickle
import json
# from reboot_check import reboot_counted
# # need to capture data before it goes to DB
from poll_data import one_min_load, five_min_load, fifteen_min_load, reboot_check

print(one_min_load,five_min_load,fifteen_min_load,reboot_check)
# use the reboot count from db  ( 0 or 1 )


print(one_min_load,five_min_load,fifteen_min_load)
print(reboot_check)


class Check_system_processes:
    file_location = "/Users/matthewchadwell/server_environment/project_files/"
    file_name = 'pickled_file'

    pickled_file_location = file_location + file_name
    reboot_check = 0
    load_warning = "SYSTEM FINE"

    # actual load values reported
    load_value_one = one_min_load
    load_value_five = five_min_load
    load_value_fifteen = fifteen_min_load

    # increment , (default is zero) values read from pickled file
    one_min = 0
    five_min = 0
    fifteen_min = 0

    with open("/Users/matthewchadwell/server_environment/project_files/config.json") as f:
        data = json.load(f)

    # interval = data["poll_check"]
    interval = data["time_check"]



    # specify in config.json if true or false , reset counter
    reboot_reset = data["reset_reboot_counter"]
    print(reboot_reset)

    # (warning level) A specified load avg checked for everytime script runs

    # one_min_thresh = data["one_min_threshold"]
    # five_min_thresh = data["five_min_threshold"]
    # fifteen_min_thresh = data["fifteen_min_threshold"]

    one_min_thresh = data["load_average_threshold"]
    five_min_thresh = data["load_average_threshold"]
    fifteen_min_thresh = data["load_average_threshold"]


    # (warning level)
    # A specified amount of times a high reading for load avg can reach before reaching warning threshold
    # warning_one_min = data["warning_cycle_cnt_one_min"]
    # warning_five_min = data["warning_cycle_cnt_five_min"]
    # warning_fifteen = data["warning_cycle_cnt_fifteen"]

    warning_one_min = data["load_above_threshold_count"]
    warning_five_min = data["load_above_threshold_count"]
    warning_fifteen = data["load_above_threshold_count"]

    def check_if_pickeled_file_exist(self):
        # this checks if the file exists however does not check if it is empty , If file is empty Ran out of input error occurs

        # creates the pickled file if it doesn't exist and first server check performed / first server reading saved to the file
        if path.exists(self.pickled_file_location) and os.stat(self.pickled_file_location).st_size != 0:
            print("file exists and has data")
        else:
            print("yowzers")
            self.store_data(self.reboot_check)

    def check_reboots(self):
       # checks if reboot needs to be reset to zero ( specified in config.json )
       # reboot counter ,returns a reboot count from the pickled file plus 1 if a reboot had occured on the
       # front end needs to show zero count upon change w/o waiting for next poll
       # reset occurs but server continues to count and display future reboots

        if self.reboot_reset == "YES":
            # setting is checked
            rbt_count = 0
            print("Reset number of reboots")
        else:
            rbt_count = self.reboot_check + reboot_check
            print("Reboot count checked")
        return rbt_count

    def load_threshold_check_incrementer(self):
        # Add counts for reboots
        # Checks the server time interval chosen
        # If time interval for checking server is changed previous load counts set to zero
        # If the load checked does not report high for specified number of cycles the count is set back to zero
        if self.interval == 15:
            self.one_min = 0
            self.five_min = 0
            if self.load_value_fifteen >= self.fifteen_min_thresh:
                self.fifteen_min += 1
            elif self.load_value_fifteen < self.fifteen_min_thresh:
                self.fifteen_min = 0
        if self.interval == 5:
            self.one_min = 0
            self.fifteen_min = 0
            if self.load_value_five >= self.five_min_thresh:
                self.five_min += 1
            elif self.load_value_five < self.five_min_thresh:
                self.five_min = 0
        if self.interval == 1:
            self.five_min = 0
            self.fifteen_min = 0
            if self.load_value_one >= self.one_min_thresh:
                self.one_min += 1
            elif self.load_value_one < self.one_min_thresh:
                self.one_min = 0

    def store_data(self, reboot_countin):
        # write to the pickeled file with the updated high load incrementer global count and reboot count
        load_and_reboot_count = {}
        load_and_reboot_count["one_min_thresh"] = self.one_min
        load_and_reboot_count["five_min_thresh"] = self.five_min
        load_and_reboot_count["fifteen_min_thresh"] = self.fifteen_min
        load_and_reboot_count["reboot_count"] = reboot_countin
        outfile = open(self.pickled_file_location, 'wb')  # write , byte format
        # open file for writing
        pickle.dump(load_and_reboot_count, outfile)
        # object want to pickle and file to which to save it to

        outfile.close()
        print('check' + str(load_and_reboot_count))

    def read_pickel_get_min_values(self):
        # read pickled file and assign these values to the global variables
        in_file = open(self.pickled_file_location, 'rb')
        new_dict = pickle.load(in_file)
        # returns the values form the pickled file
        self.one_min = new_dict["one_min_thresh"]
        self.five_min = new_dict["five_min_thresh"]
        self.fifteen_min = new_dict["fifteen_min_thresh"]
        self.reboot_check = new_dict["reboot_count"]

        in_file.close()
        return new_dict


    # def read_pickel_check_updated_values(self):
    #     # Read the pickled file for amount of times load value exceeded specified, if over warn count throw a warning
    #     in_file = open(self.pickled_file_location, 'rb')
    #     new_dict = pickle.load(in_file)
    #     in_file.close()
    #     if new_dict["fifteen_min_thresh"] >= self.warning_fifteen:
    #         self.load_warning = "WARN"
    #         message = 'Warning for {} or more cycles {} min load greater than {},{} {}'.format(self.warning_fifteen, self.interval, self.fifteen_min_thresh, date_now, time_now)
    #         return self.load_warning, message
    #     if new_dict["five_min_thresh"] >= self.warning_five_min:
    #         self.load_warning = "WARN"
    #         message = 'Warning for {} or more cycles {} min load greater than {},{} {}'.format(self.warning_five_min, self.interval, self.five_min_thresh, date_now, time_now)
    #         return self.load_warning, message
    #     if new_dict["one_min_thresh"] >= self.warning_one_min:
    #         self.load_warning = "WARN"
    #         message = 'Warning for {} or more cycles {} min load greater than {},{} {}'.format(self.warning_one_min, self.interval, self.one_min_thresh, date_now, time_now)
    #         return self.load_warning, message
    #     else:
    #         # catch if load threshold does not exceed
    #         message = None
    #         return self.load_warning, message
    #
    # # def record_reboot_count_to_config(self, reboot_counto):


###################################################################
#                # REBOOT CHECK / COUNT                           #
###################################################################
# gloabal reboot count
# Steps:

# pickeled file checked to see if it exists itself
# if file exists current global value stored -> store_data(self.reboot_check)

# check if setting is YES , if so reboot_cnt set to zero
# if setting is NO ,  rbt_count = self.reboot_check + reboot_counted




# if __name__ == "__main__":
check_it = Check_system_processes()

check_it.check_if_pickeled_file_exist()
# create pickeled file if it does not exist already

check_it.read_pickel_get_min_values()
# print('look' + str(che['reboot_count']))
# read pickled file for values , set values to global variables

reboot_number = check_it.check_reboots()
# if a reboot occurred reboot value returned from uptime_read_aftr_reboot , this value is added to read value from pickle file
# number of times reboots have occurred to be written to pickled file (reboot_number)

check_it.load_threshold_check_incrementer()
# increments global values for high loads
check_it.store_data(reboot_number)
# write to pickled file number of high load occurrences and reboot count




####-------------- add to Poll data area, calling this script will keep inrmenteing laod checks ----------------########
# warning, load_message = check_it.read_pickel_check_updated_values()
# # read the pickled file to get the updated high load and reboot count
#
# message_about_load = load_message
# warning_given = warning
####-------------- add to Poll data area, calling this script will keep inrmenteing laod checks ----------------########


reboot_count_checkin = check_it.check_reboots()
print(reboot_count_checkin)
# count added up


# open json and write reboot count to it , than reference count to rendered template show in poll block
# config_file = "/Users/matthewchadwell/server_environment/project_files/config.json"
# with open(config_file, "w") as g:
#     data = json.load(g)
#     data["reboot_counto"] = reboot_count_checkin
#     json.dump(data, g)

# example : Warning for 10 or more cycles 1 min load greater than 10,2021-06-09 19:58:56




# store reboot count in config


# --TODO -- if Warning occurs report top 10 Pids return top consuming processes

