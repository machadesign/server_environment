#!/usr/bin/env python

# File contains flask logic

import json
from flask import Flask, render_template
# from sensor_info import return_current_time, return_current_date, current_temp
from sensor_info import current_time, todays_date, current_temp
from server_info import rounded_CPU, rounded_GPU_temp
from server_info import system_load, sys_mem
from threshold_check import warning
from reboot_check import uptime
from query_db import num_reboots

print(num_reboots)
# import query_db
# from db_engine import engine
# from db_creation import environment
# from query_db import reboot_recordings


# add mb,kb etc. for memory being recorded
# add celsisu for temp check
# need add system up since uptime , this time should not change unless reboot occurs

app = Flask(__name__)

with open('/Users/matthewchadwell/server_environment/config') as config_file:
    config = json.load(config_file)

# reboot_times, reboot_count_check = reboot_recordings(environment)
sensor_id = config["sensor_id"]
# current_time = return_current_time()
current_date = todays_date
load_system = system_load
check_warning = warning
# current_temp = return_current_temp(sensor_id)
temp_plot = '/images/todays_temp_chart.png'

# how to set default value for all static files
# app.config['File'] = 300


@app.after_request
def add_header(response):
    # check if cache control is setup header ,if not do not store cache for static files
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

# TODO header instruction needed set cache to 0
@app.route('/')
def environment_dashboard():

    return render_template('homepage.html', date=current_date,
                           time=current_time,
                           temp=current_temp,
                           image=temp_plot,
                           cpu_temp=rounded_CPU,
                           gpu_temp=rounded_GPU_temp,
                           load=system_load,
                           high_load_warning=check_warning,
                           memory=sys_mem,
                           reboot=num_reboots,
                           uptime=uptime
                           )


if __name__ == "__main__":
    app.run(port=config["port"], debug=True)