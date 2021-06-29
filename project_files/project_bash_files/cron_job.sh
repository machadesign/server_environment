#!/bin/bash

python3 gather_data.py
python3 server_info.py
python3 db_insert_data.py
python3 Load_and_reboot_check.py # ( runs - reboot_check.py, no need to run directly)
python3 run_warnings.py
python3 init.py