#!/usr/bin/env python

# File contains flask logic

from flask import Flask, render_template
from sensor_info import return_current_time, return_current_date, return_current_temp

app = Flask(__name__)
sensor_id = 'id0101'

current_time = return_current_time()
current_date = return_current_date()
current_temp = return_current_temp(sensor_id)
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
    return render_template('homepage.html', date=current_date, time=current_time, temp=current_temp, image=temp_plot)


if __name__ == "__main__":
    app.run(port=3639, debug=True)