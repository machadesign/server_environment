#!/usr/bin/env python


from sqlalchemy import *
# from sqlalchemy import MetaData , MetaData use w/ multiple tables
from db_engine import engine


meta = MetaData()

environment = Table('environment', meta,
                    # the collection of tables are defined in the MetaData cataloge
                    Column('id', Integer, primary_key=True),
                    Column('date_and_time', String(25)),
                    Column('date', String(20)),
                    Column('time', String(20)),
                    Column('uptime_date', String(20)),
                    Column('uptime_time', String(20)),
                    Column('reboot_check', BOOLEAN),
                    Column('ambient_temperature', Float(20)),
                    Column('cpu_temperature', Float(20)),
                    Column('gpu_temperature', Float(20)),
                    Column('one_min_avg_load', Float(20)),
                    Column('five_min_avg_load', Float(20)),
                    Column('fifteen_min_avg_load', Float(20)),
                    Column('percent_memory_used', Integer),
                    Column('cpu_wait', Float(20)),
                    Column('cpu_idle', Float(20)),
                    Column('percent_of_swap_used', Float(20)),
                    Column('cpu_user_time', Float(20)),
                    Column('kernel_time', Float(20))
                    )

meta.create_all(engine)




