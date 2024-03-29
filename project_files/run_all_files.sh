#!/usr/local/bin/bash


# clear DB , insert seed data
# values taken from system capture bash file

# all modules need to installed package manager -  /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/
# https://realpython.com/run-python-scripts/#how-to-run-python-scripts-interactively
# https://realpython.com/python-modules-packages/#the-module-search-path

#source './venv/bin/activate'
# instead of having the files saved directly into package management

# cron job schedule running this script


#for value in {1..5}
## implement for loop for quick testing
#do
    python3 /Users/matthewchadwell/server_environment/flask_dir/server_data.py;
    # server_data runs the mock_data_check and system_capture , stores system values in variables
    python3 /Users/matthewchadwell/server_environment/project_files/server_info.py;
    python3 /Users/matthewchadwell/server_environment/project_files/reboot_check.py;
    python3 /Users/matthewchadwell/server_environment/project_files/db_insert_data.py;
    python3 /Users/matthewchadwell/server_environment/project_files/Load_and_reboot_check.py;
    python3 /Users/matthewchadwell/server_environment/project_files/run_warnings.py;
    python3 /Users/matthewchadwell/server_environment/flask_dir/send_email.py;
#done



# run separately, server continues after initial run
# python3 /Users/matthewchadwell/server_environment/flask_dir/__init__.py;