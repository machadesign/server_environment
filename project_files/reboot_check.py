# -----------------------------------
# script runs at bootup
# Checks the difference between System time and Uptime
# If no difference between current date and uptime AND the time between two is within 5 mins, reboot count of 1, into DB
# reboot counted will hold value of 1 if reboot occurs
# -----------------------------------

from poll_data import uptime_date, uptime_time, date_now, time_now






# TODO -- send an email with time of the reboot
# web page should show number of reboots

def time_format_to_minutes(time):
    # https://stackoverflow.com/questions/48447123/convert-time-hhmmss-to-minutes-in-python
    t = 0
    time_split = time.split(':')
    for i in time_split:
        t = 60 * t + int(i)
    time_in_minutes = t/60
    return time_in_minutes
    # return value - rounded to minute


def difference_between_up_and_current():
    # Check for a reboot, if dates are the same check for difference in minutes between uptime and current time
    # when a reboot occurs system comes up and dates should be the same and the time differecne of <5 minutes

    # convert time to minutes, minutes from 12am
    uptime_minutes = time_format_to_minutes(uptime_time)
    current_minutes = time_format_to_minutes(time_now)

    # return difference_minutes
    difference_in_minutes = current_minutes - uptime_minutes

    # round minute difference
    # rounded_min_difference = round_value(difference_minutes,  "reboot_time_difference_rounded")
    # TODO -- no need to round , possibly remove

    return difference_in_minutes


def reboot_check_compare_dates(current_date_only, up_time_date_only, uptime_current_time_difference):
    # compares the current date and uptime date
    # every time their is a reboot the time is given and reboot count increases
    diff_list = []
    # if list is empty , no differences between dates
    # current_time_only, current_date_only
    current_date_list = current_date_only.split("-")
    up_time_dates_list = up_time_date_only.split("-")

    for i in current_date_list:
        # compares the current date and uptime date
        if i not in up_time_dates_list:
            diff_list.append(i)
# TODO - replace w/ list comprehension

    if len(diff_list) < 1 and uptime_current_time_difference <= 5:
        # if there is no difference in uptime and current time (same date)
        # and time difference is less than 5 mins,reboot occured
        # reboot_uptime = uptime_time  , return uptime or system time when reboot count is 1
        reboot_count = 1
        # return reboot_uptime, reboot_count
        return reboot_count
# TODO - print("System rebooted around {}".format(uptime))
        # reboot occurred , user will reference time reboot reported.(rough estimate when reboot may have occurred
    else:
        reboot_count = 0
        return reboot_count
# TODO - print("System up since {}".format(uptime))
        # this will print the uptime after bootup
        # reboot did not occur, no value inserted into DB


uptime_in_minutes = time_format_to_minutes(uptime_time)
time_now_in_minutes = time_format_to_minutes(time_now)
difference_minutes = difference_between_up_and_current()
reboot_counted = reboot_check_compare_dates(date_now, uptime_date, difference_minutes)
# if a reboot occured 1 is th value, if not 0 is
# reboot time reported , or none if reboot did not occur .
# single_reboot_count = reboot_check_compare_dates(date_now, uptime_date, difference_minutes)
print(reboot_counted)
