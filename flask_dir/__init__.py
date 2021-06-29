#!/usr/bin/env python


# put correct database
# File contains flask logic
# from gather_data import current_time, current_date, uptime_time, uptime_date
from sensor_probe_info import current_ambient_temp
# from server_info import cpu_temp_reading, gpu_temp_reading, percent_of_swap_used, cpu_idle, cpu_wait, kernel_time, cpu_user_time
# from server_info import mock_sys_load, percent_memory_used, total_memory, memory_used, one_min_avg_load ,five_min_avg_load, fifteen_min_avg_load

import json
import DateTime
from flask import jsonify
import sqlite3
from flask import g
from flask import Flask, render_template
from flask import request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, ValidationError, SelectField, SelectMultipleField, RadioField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional
import datetime
import pandas as pd
import sqlite3
# from gather_data import date_now
import matplotlib.pyplot as plt
import matplotlib
import base64
from io import BytesIO
from datetime import date
import matplotlib.dates as mdates
# from Load_and_reboot_check import reboot_count_checkin



# this will run everytime browser refreshed, accumulating load warnings over and over

# from run_warnings import poll_check  , removed possible calling script twice
from poll_data import date_and_time, date_now, time_now, uptime_date, uptime_time, reboot_check, ambient_temp, cpu_temp, gpu_temp, \
    one_min_load, five_min_load, fifteen_min_load, memory_used_percent, cpu_idle, swap_used_percent, cpu_user_time, \
    kernel_use_time, cpu_wait_time, reboot_coutified


# poll data from database , checks latest entry


# imported values remain constant until script is ran , thus updating all values


# create an instance of current reboot count


# change the value of reboot count if reboot reset set to zero , this will store value temporaily


# reset option needs to be switched back to off
#



import numpy as np
matplotlib.use('Agg')
# Agg is a non-interactive backend, meaning it won't display chart on the screen, only save to files
# (FIX) added because of error being given (Warning UserWarning: Starting a Matplotlib GUI outside of the main thread will likely fail.)


today = date.today()
DATABASE = '/Users/matthewchadwell/server_environment/project_files/server_environment.db'
app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="Secret_key",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))


# ----------- old direct way calling data,not frm db  -----------#
# # current_time = return_current_time()
# current_date = date_now
# load = mock_sys_load
#
# # check_warning = warning
# sys_mem_used = percent_memory_used
# --------------------------------------------------------------------#




# current_temp = return_current_temp(sensor_id)
temp_plot = '/images/todays_temp_chart.png'

# --TODO  add error default handling
# error default handling
# if not (id or published or author):
#     return page_not_found(404)


def get_db():
    db = getattr(g, DATABASE, None)
    # db = getattr(g, '_DB_file.db', None)
    if db is None:
        db = g._DB_file = sqlite3.connect(DATABASE)
    return db

#     entered_student = ('SMokeyJoe', 'Austin')
#     conn.execute(entry, entered_student)

def query_function(entered_query):
    con = get_db()
    query = entered_query
    query_check = con.execute(query)
    # conn = sqlite3.connect(DATABASE)
    rv = query_check.fetchall()
    con.close()
    return rv[0][0]


class AForm(FlaskForm):
    # issues with WTFforms , 0 is not accepted as valid input
    # false can not be accpeted (true/false) , workaround is to replace the InputRequired validator with a AnyOf([True, False])

    # https://www.tutorialspoint.com/flask/flask_wtf.htm
    # TODO --If undefined value provided no warning needed
    # AForm used in login_test function UI inform user enter valid/ expected data
    #  strip_whitespace – If True (the default)  if user leaves empty spaces they are removed upon submittion
    # cont. also stop the validation chain on input which consists of only whitespace.


    poll_check = SelectField(u'Poll_check', choices=['1', '5', '15'])


    reset_reboot_counter = RadioField(u'Reset_reboot_counter', choices=['YES', 'NO'])
    # workaround is to replace the InputRequired validator with a AnyOf([True, False]).
    reboot_warning = RadioField(u'Reboot_warning', choices=['ON', 'OFF'])

    cpu_temp_warning = IntegerField('cpu_temp_warning', [DataRequired(message="Required"), Optional()])
    gpu_temp_warning = IntegerField('gpu_temp_warning', [DataRequired(), Optional()])
    ambient_temp_warning = IntegerField('ambient_temp_warning', [DataRequired(), Optional()])

    percent_memory_warning = IntegerField('percent_memory_warning', [DataRequired(), Optional()])
    percent_swap_warning = IntegerField('percent_swap_warning', [DataRequired(), Optional()])

    time_check = SelectField('time_check', choices=['1', '5', '15'])

    load_average_threshold = IntegerField('load_average_threshold', [DataRequired(), Optional()])
    load_above_threshold_count = IntegerField('load_above_threshold_count', [DataRequired(), Optional()])

    cpu_idle_warning = IntegerField('cpu_idle_warning', [DataRequired(), Optional()])
    wait_warning = IntegerField('wait_warning', [DataRequired(), Optional()])


    # User chooses one, five, or fifteen to be the threshold
    # TODO -- Need an option that only enables one pair to enter data in


    # choose minute load average want to capture warnings

    # load_average_minute = IntegerField('load_average_minute', [DataRequired(), Optional()])



    # reset_reboot_counter = RadioField('reset_reboot_counter', choices=['YES', 'NO'], default=reset_reboot)
    # poll_check = IntegerField('poll_check', [DataRequired(), Optional(strip_whitespace=True), NumberRange(min=2, max=6, message="Value out of range")],default=5)
    # time_check = IntegerField('time_check', [DataRequired(),Optional(), NumberRange(min=2, max=6, message="Value out of range")])
    # # 'time_check' specified in json file
    submit = SubmitField('Submit')
    # login_test function -> form.validate_on_submit() AFTER validation , dict iterated through and json written


# def db_frame_function(plot_title,data_types):
def db_frame_function(plot_title, start_date, end_date, data_types):

    # data types is the data being shown between range for each date/time specified
    years = mdates.YearLocator()  # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')

    # connect to database and use cursor to lazy load requested data from db( Not all at one once , fetchall())
    con = get_db() #.cursor()

    # Need to setup connection with flask request , and close connection after information retrieved
    # conn = sqlite3.connect(db_file)

    dframe = pd.read_sql_query("select * from environment", con)
    # close the connection to the db after data retrieved and data stored in dataframe
    con.close()

    # x = dframe.loc[lambda df: df['date'] == current_date]   (original)
    # dframe['date'] = pd.date_range('2021-1-19', periods=3, freq='D')

    # pd.date_range('2021-1-19', periods=3, freq='D')

    mask = (dframe['date_and_time'] > start_date) & (dframe['date_and_time'] <= end_date)
    # date_and_time is the column name for line entry in db , format 2021-01-19 21:32:57

    x = dframe.loc[mask]
    # returns the row as a Series, all dataframe information  for dates

    today_sorted = x.sort_values(by='date_and_time')
    # today_sorted is a dataframe specified to be sort accordingly  (original)

    plt.style.use(['dark_background'])
    plt.rcParams['lines.linestyle'] = '--'

    # plt.xlabel("Today")

    plt.rcParams.update({'figure.autolayout': True})

    # plt.tick_params(axis='x', labelbottom=False)
    # formatted_date_time =



    # today_sorted.plot(title=plot_title, x='date_and_time', y=data_types).get_figure()

    # today_sorted.plot(title=plot_title, x='date_and_time', xlabel="", y=data_types, figsize=(10, 7)).get_figure()
    today_sorted.plot(title="", x='date_and_time', xlabel="", y=data_types, figsize=(10, 7)).get_figure()


    # y is the data from the rows from specified categories from thedb
    # get current axes , chosen vert the yaxis values

    ax = plt.gca()
    ax.tick_params(axis='x', labelrotation=90)
    # plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))
    # ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',ncol=2, mode="expand", borderaxespad=0.)

    # ax.legend(loc="lower left", ncol=len(dframe.columns))
    # plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3))
    plt.subplots_adjust(bottom=.40)
    # plt.grid(axis='x')



    # set(gca, 'OuterPosition', [left bottom + 0.1 width height])



    # chart without bottom ticks
    # ax.axes.xaxis.set_visible(False)

    # ax.axes.xaxis.set_ticks([])

    # use this so the label is still shown


    # ax.tick_params(axis='x',labelrotation=90)

    # The location of the ticks is determined bya Locator object

    # save file to temporary buffer,save in a buffer rather than at a location
    # write byte object
    byte_stream = BytesIO()

    # plt.figure(frameon=True)
    plt.savefig(byte_stream, format="png")
    plt.close()
    # need to close out plots, otherwise images remain in memory .Starts to consume too much mem.Always close your Matplotlib figures
    # StringIO and BytesIO classes are most useful in scenarios where you need to mimic a normal file.(change dataframe into png file)
    # save byte object  to temporary buffer,save in a buffer rather than at a location
    data = base64.b64encode(byte_stream.getbuffer())
    data = data.decode("ascii")
    image_data = "data:image/png;base64,{data}".format(data=data)
    return image_data

# @app.after_request
# def add_header(response):
#     # check if cache control is setup header ,if not do not store cache for static files
#     if 'Cache-Control' not in response.headers:
#         response.headers['Cache-Control'] = 'no-store'
#     return response

def return_reboot_count():
    entered_query = "select COUNT(reboot_check) from environment where reboot_check = 1"
    reboot_count = query_function(entered_query)
    # returns total number of reboots
    return reboot_count

def graph_images(start,end):

    temp_data = ["cpu_temperature", "gpu_temperature", "ambient_temperature"]
    temp_image_data = db_frame_function("temperature_reading", start, end, temp_data)

    load_data = ["one_min_avg_load", "five_min_avg_load", "fifteen_min_avg_load"]
    load_image_data = db_frame_function("system_load", start, end, load_data)

    kernel_data = ["kernel_time", "cpu_user_time"]
    kernel_cpu_time = db_frame_function("Kernel_and_user_usage", start, end, kernel_data)

    memory_data = ["percent_memory_used", "percent_of_swap_used"]
    system_memory_used = db_frame_function("System_Memory", start, end, memory_data)

    cpu_data = ["cpu_idle", "cpu_wait"]
    cpu_state = db_frame_function("cpu_state", start, end, cpu_data)
    return temp_image_data, load_data, load_image_data, kernel_cpu_time, system_memory_used, cpu_state


# enter value in a form
# submit value
# open json if it exists
# write to json ,append value
# if not creates new json file

# -----------------------
# custom validator
# def length(min=-1, max=-1):

    # message = 'Must be between %d and %d characters long.' % (min, max)
    # def _length(form, field):
    #     l = field.data and len(field.data) or 0
    #     if l < min or max != -1 and l > max:
    #         raise ValidationError(message)
    #
    # return _length
# TODO header instruction needed set cache to 0
@app.route("/", methods=["POST", "GET"])
# functions below are mapped to the URL ('/")
def environment_dashboard():


    # gather data file - from gather_data import current_time, current_date, uptime_time, uptime_date

    # a get is performed , retrieves last stored values. Once init file is ran (poll check) new values will be saved
    # refresh the page , and a get will be performed getting last stored value

    # init , shell script runs and gathers date/time last poll was taken and stored ( not current date/time )

    # ------------ For the date time input widget - use if selecting a date range ----------#
    # start_date_time = today.strftime("%Y-%m-%d")
    # # default dates for data shown to user when first visit the page
    # end_date_time = today.strftime("%Y-%m-%d")


    todays_date = datetime.datetime.now()
    # (day time object ) result 2021-06-09 14:50:54.967380 , used instead of gathered data date becasue easy to format w/python
    formatted_current_time = todays_date.strftime("%H:%M:%S")
    beginning_of_the_day_time = "00:00:00"
    formatted_date = todays_date.strftime("%Y-%m-%d")


    # current time formatted for input
    input_formatted_time = todays_date.strftime("%H:%M")

    start = formatted_date
    start_time = "00:00"
    end = formatted_date
    end_time = input_formatted_time

    start_date_time = formatted_date + ' ' + beginning_of_the_day_time
    end_date_time = formatted_date + ' ' + formatted_current_time
    # date shown date input value , (to)  (from) , data not from DB

    temp_image_data, load_data, load_image_data, kernel_cpu_time, system_memory_used, cpu_state = graph_images(start_date_time, end_date_time)
    # image information

    reboot_count = return_reboot_count()
    if request.method == 'POST':
        # change default dates to posted dates
        end = request.form.get('end_date')
        end_time = request.form.get('end_time')
        start = end
        # start = request.form.get('start_date')
        start_time = request.form.get('start_time')


        start_date_time = start + ' ' + start_time + ':00'
        end_date_time = end + ' ' + end_time + ':00'
        # defaultValue: "2021-04-22"
        # value: "16:42"
        # format needed '2010-05-12 23:59:59'

        temp_image_data, load_data, load_image_data, kernel_cpu_time, system_memory_used, cpu_state = graph_images(start_date_time, end_date_time)
        # get all images woul d like to add to homepage
        # print("beginning" + ":" + start_date_time + "end date/time selected" + ':' + end_date_time)

    config_file_location = '/Users/matthewchadwell/server_environment/project_files/config.json'
    reboot_poll_check = reboot_coutified
    with open(config_file_location) as f:
        y = json.load(f)
    poll = y["poll_check"]
    if y["reset_reboot_counter"] == "YES":
        reboot_poll_check = 0
    # check if reboot occured , adjust reboot poll


    return render_template('home_page.html', date=date_now,
                           image=temp_image_data,
                           image2=load_image_data,
                           image3=kernel_cpu_time,
                           image4=system_memory_used,
                           image5=cpu_state,
                           # images
                           time=time_now,
                           cpu_temp=cpu_temp,
                           gpu_temp=gpu_temp,
                           ambient_temp=ambient_temp,
                           one_min_load=one_min_load,
                           five_min_load=five_min_load,
                           fifteen_min_avg_load=fifteen_min_load,
                           # load=load
                           cpu_idle=cpu_idle,
                           cpu_wait=cpu_wait_time,
                           memory=memory_used_percent,
                           swap_memory=swap_used_percent,
                           reboot=reboot_poll_check,
                           # reboot=reboot_poll_check,
                           # this will only check database , will count reboots over time
                           # reboot=reboot_count_checkin,
                           # reboot checkin script w/ load checking will need to be ran separately
                           uptime=uptime_time,
                           uptime_date=uptime_date,
                           percent_swap_used=swap_used_percent,
                           user=cpu_user_time,
                           system=kernel_use_time,

                           time_start=start_time,
                           date_start=start,
                           time_end=end_time,
                           date_end=end,
                           # data given to route directly, not queried from db

                           last_poll=date_and_time,
                           poll_interval=poll
                           # poll_interval=poll_check,
                           # config file setting
                           )






@app.route('/settings', methods=('GET', 'POST'))
# performs the Post first and than Get , specified
def login_test():

    config_file_location = '/Users/matthewchadwell/server_environment/project_files/config.json'
    time_check = None
    form = AForm()
    # AFORM used with wtf validate data upon submitiion
    # if request.method == 'POST':     ( form.validate    handles the post/get method check , no need for if statement)
    with open(config_file_location) as f:
        y = json.load(f)
        # Open JSON setting file , load data and over

    if form.validate_on_submit():
        # AFORM used with wtf validate data upon submitiion , works if all values qualify
        # TODO - flash('Thank you for the info') refer to https://blog.teclado.com/flashing-messages-with-flask/ , flash meesages stored not shown
        dict = request.form.to_dict(flat=True)
        # flatten immutable dict created from submitted form so can access the content , form is of type ImmutableMultiDict
        # https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.to_dict.html

        # dict object contains all key/value pairs submiited from the form

        # create another instance of dict to append to final dict , key /(str values)
        # end result dictionary key intvalues and key strvalue pairs



        # Formatting string data from json object, all value sstring
        # add any non int value (key:value) example :  "YES" or bool
        search_dict_for_these_keys = ['reset_reboot_counter', 'reboot_warning']

        str_value_dict = {}
        # create empty dictionary to hold  search_dict_for_these_keys {key:value}

        # get the values for the keys w/ string values(search_dict_for_these_keys)
        for i in search_dict_for_these_keys:
            for key, value in dict.items():
                if key == i:
                    # y[key]
                    z = str(dict[key])
                    str_value_dict.update({key: z})
                    # turn booleans into string

                    # str_value_dict.update({key: dict[key]})


        # remove all key str values and 'csrf_token', 'submit'
        [dict.pop(key) for key in ['csrf_token', 'submit', 'reset_reboot_counter','reboot_warning']]

        # removed 'csrf_token', 'submit' ,not part of dict   ,removed 'key2','key3' , because already in correct type format - string
        for key, value in dict.items():
            # dict created from form values submitted
            y[key] = int(value)
        y.update(str_value_dict)


# -----------------------------------------------------------------
            # WT Form module to protected our Form with a unique csrf_token from the server
            # avoid an attack where attacker tricks a web browser into executing an unwanted action
            # cont .. in an application to which a user is logged in


            # add all int key (values) to this list
            # !! HTTP only deals with text (or binaries). ,need to convert values to int when saving to json!!
            # only one verification csrf for a single form submit , containing all inputs
            # csrf_token and submit automatically added to the dict , avoid submitting these with check if key not in the list

            # if key not in int_key_values:
            #     y[key] = int(value)
# -------------------------------------------------------------------

                # original json key = forms int entered
        with open(config_file_location, 'w') as g:
            # the key/value entered from the for overwrite existing key/values
            json.dump(y, g, indent=4, sort_keys=True)
        # from dcitionary return jsonify(y)

        return redirect("/", code=200)
    # Upon post

    with open(config_file_location) as f:
        get_config = json.load(f)
    # on page laod GET the existing data from json file

    set_poll = get_config["poll_check"]
    # sensor_id = get_config["ambient_sensor_id"]
    # not added to settings yet , determine criteria
    set_ambient_temp_warn = get_config["ambient_temp_warning"]
    set_cpu_temp_warn = get_config["cpu_temp_warning"]
    set_gpu_temp_warn = get_config["gpu_temp_warning"]
    set_load_threshold_level = get_config["load_average_threshold"]
    set_load_threshold_count = get_config["load_above_threshold_count"]
    set_memory_warn = get_config["percent_memory_warning"]
    set_swap_warn = get_config["percent_swap_warning"]
    set_reboot_warn = get_config["reboot_warning"]
    reset_reboot = get_config["reset_reboot_counter"]
    set_time = get_config["time_check"]
    cpu_idle_warn = get_config["cpu_idle"]
    cpu_wait_warn = get_config["cpu_wait"]

# add configs into form as default values

    form = AForm(poll_check=set_poll, reset_reboot_counter=reset_reboot,
                 reboot_warning=set_reboot_warn,
                 cpu_temp_warning=set_cpu_temp_warn,
                 gpu_temp_warning=set_gpu_temp_warn,
                 ambient_temp_warning=set_ambient_temp_warn,
                 percent_memory_warning=set_memory_warn,
                 percent_swap_warning=set_swap_warn,
                 time_check=set_time,
                 load_average_threshold=set_load_threshold_level,
                 load_above_threshold_count=set_load_threshold_count,
                 cpu_idle_warning=cpu_idle_warn,
                 wait_warning=cpu_wait_warn
                 )

    return render_template('settings.html', form=form)


@app.route('/form-example', methods=['GET', 'POST'])
def exam_graphing():
    if request.method == 'POST':
        first_number = request.form.get('first')
        second_number = request.form.get('second')
        # print(second_number)
        # third_number = int(first_number) + int(second_number)
        # return first_number, second_number
        data = ["cpu_temperature", "gpu_temperature", "ambient_temperature"]
        temp_image_data = db_frame_function(plot_title="temperature_reading", start_date=first_number,end_date=second_number,data_types=data)
        return render_template('examp_graphing.html', first=first_number, second=second_number, image=temp_image_data)
    return ''' <form method="POST">
               <div><label>Language: <input type="date" name="first"></label></div>
               <div><label>Framework: <input type="text" name="second"></label></div>
               <input type="submit" value="Submit">
           </form> '''


#         <form method="POST">
#             <div><label>Language: <input type="text" name="language"></label></div>
#             <div><label>Framework: <input type="text" name="framework"></label></div>
# # the keys in the applictaion dignated to the route will be  language and framework
#             <input type="submit" value="Submit">
#         </form> '''




    # entered_query = "select COUNT(reboot_counted) from environment where reboot_counted = 1"
    # reboot_count = query_function(entered_query)

# @app.route("/temp_image")
# def temp_image():
#     start = '2021-01-15'
#     end = '2021-01-25'
#     # if switching beteen 1, 5 15 mins access a gloabal variable specified in a an if statement
#     # could possibly make a subplot
#     load_data = ["one_min_avg_load"]
#     load_data = db_frame_function("system_load", start, end, load_data)
#     temp_data = ["cpu_temperature","gpu_temperature","ambient_temperature"]
#     image_data = db_frame_function("temperature_reading",start, end, temp_data)
#     return render_template("image.html", temp_image=image_data,load_image=load_data)
#
# # plot_title, start_date, end_date, data_types
#
#
# @app.route("/sys_load_image")
# def sys_load_image():
#     # if switching beteen 1, 5 15 mins access a gloabal variable specified in a an if statement
#     # could possibly make a subplot
#     start = '2021-01-15'
#     end = '2021-01-25'
#     load_data = ["one_min_avg_load","five_min_avg_load", "fifteen_min_avg_load"]
#     image_data = db_frame_function("system_load",start,end,load_data)
#     return render_template("image.html", image=image_data)


if __name__ == "__main__":
    app.run(debug=True)
    # port = config["port"],


