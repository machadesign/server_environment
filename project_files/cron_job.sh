#!/bin/bash

python3 db_init.py
python3 sensor_info.py
python3 db_insert_data.py
python3 db_data_to_pandas.py
