#!/usr/bin/env python
# read the pickled file
import pickle
import logging
import json

error_file = '/Users/matthewchadwell/server_environment/project_files/error.log'
FORMAT = '%(levelname)s: %(asctime)-15s %(message)s LINE: %(lineno)d MODULE: %(module)s'
logging.basicConfig(filename=error_file, filemode="a", level=logging.ERROR, format=FORMAT)
loggerizing = logging


# with open("/Users/matthewchadwell/server_environment/project_files/config.json") as f:
#     data = json.load(f)

file_location = "/Users/matthewchadwell/server_environment/project_files/"
file_name = 'pickled_file'

pickled_file_location = file_location + file_name


def read_pickel_get_min_values():
    # read pickled file and assign these values to the global variables
    try:
        in_file = open(pickled_file_location, 'rb')
        new_dict = pickle.load(in_file)
        # returns the values form the pickled file
        one_min = new_dict["one_min_thresh"]
        five_min = new_dict["five_min_thresh"]
        fifteen_min = new_dict["fifteen_min_thresh"]
        reboot_count = new_dict["reboot_count"]

        in_file.close()
        return one_min, five_min, fifteen_min
    except Exception:
        loggerizing.error("Issue reading pickled load/reboot data")
        loggerizing.debug("Issue reading pickled load/reboot data", exc_info=True)




def store_data(one_min,five_min,fifteen_min):
        # write to the pickeled file with most recent load count
        # re write reboot count to zero, reset
    try:
        load_and_reboot_count = {}
        reset_reboot = 0
        load_and_reboot_count["one_min_thresh"] = one_min
        load_and_reboot_count["five_min_thresh"] = five_min
        load_and_reboot_count["fifteen_min_thresh"] = fifteen_min
        load_and_reboot_count["reboot_count"] = reset_reboot
        outfile = open(pickled_file_location, 'wb')  # write , byte format
        # open file for writing
        pickle.dump(load_and_reboot_count, outfile)
        # object want to pickle and file to which to save it to
        outfile.close()
        print('check' + str(load_and_reboot_count))
    except Exception:
        loggerizing.error("Issue writing reset reboot to pickled file")
        loggerizing.debug("Issue writing reset reboot to pickled file", exc_info=True)


def reset_reboots():
    one,five,fifteen = read_pickel_get_min_values()
    print(one,five,fifteen)
    store_data(one,five,fifteen)
    # check if reboot value changed ( do not use in production )
    # one,five,fifteen = read_pickel_get_min_values()

#
# store_data(0,6,6)

print(read_pickel_get_min_values())







# one,five,fifteen = read_pickel_get_min_values()
# print(one,five,fifteen)
# store_data(one,five,fifteen)
#
# # check if reboot value changed ( do not use in production )
# one,five,fifteen = read_pickel_get_min_values()

# if __name__ == '__main__':
#     one,five,fifteen = read_pickel_get_min_values()
#     print(one,five,fifteen)
#     store_data(one,five,fifteen)
#
#     # check if reboot value changed ( do not use in production )
#     one,five,fifteen = read_pickel_get_min_values()
