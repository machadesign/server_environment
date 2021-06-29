# https://code.tutsplus.com/tutorials/managing-cron-jobs-using-python--cms-28231
from crontab import CronTab
import json


# user PUTs /submits a new value, before the cron job runs new scripts
# log the interval set in json file
# if the value is different than last recorded
  # run the script



# user PUTs /submits a new value
# script runs
  # value is changed in the JSON file
  # the scripts will now run at the new specified cron time



with open('/Users/matthewchadwell/server_environment/project_files/config.json') as config_file:
    config = json.load(config_file)
    interval = config["interval_check"]
# open json file access the key value for minute duration

my_cron = CronTab(user='matthewchadwell')
# access cron file  , crontab -e

my_cron.remove_all()
# clear all previous jobs

job = my_cron.new(command='python /home/jay/writeDate.py #Monitor_Job')
# how to create entire new cron job

job.minute.every(interval)
# specify every minute

# specify schedule for job to run
my_cron.write()
# specified time will append to cron command

# use comments to id jobs


# check added crons , print all jobs within cron file
for job in my_cron:
    print(job)