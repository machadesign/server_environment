#!/usr/bin/env python

import pandas as pd
import sqlite3
from sensor_info import todays_date
import matplotlib.pyplot as plt


# TODO - meant to connect to a live DB server , currently just creating a db file
class PandaTheInfo:
    file_location = '/Users/matthewchadwell/server_environment/flask_dir/static/images/todays_temp_chart.png'
    date = str(todays_date)

    def panda_db_info(self, db_file):
        conn = sqlite3.connect(db_file)
        df = pd.read_sql_query("select * from environment", conn)
        return df

    def todays_day_reporting(self, dataframe):
        x = dataframe.loc[lambda df: df['date'] == self.date]
        today_sorted = x.sort_values(by='time')
        return today_sorted

    def days_graphic(self, sorted_day):
        # Creates a scatter plot ,x axis ('time' column )  y axis ('temperature' column)
        sorted_day.plot(title=self.date, x='time', y='temperature', kind='scatter').get_figure()
        plt.gca().invert_yaxis()
        plt.savefig(self.file_location)
        # plt.show()   Note : Connection remains open, only show for testing purposes


database_file = 'DB_file.db'
c = PandaTheInfo()
p = c.panda_db_info(database_file)
d = c.todays_day_reporting(p)
c.days_graphic(d)
