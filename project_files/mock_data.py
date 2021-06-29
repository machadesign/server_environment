# Raw mock data

#  gather_data.py

config_file_location = '/Users/matthewchadwell/server_environment/project_files/config.json'
temp_directory = '/Users/matthewchadwell/mock_temp/temp_id/'
# Test - Mock data locally stored in a .txt file
arm_cpu_reading = "/Users/matthewchadwell/server_environment/mock_cpu_arm_temp/temp"
get_load_avg = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/load_avg.sh"
get_system_memory_info = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/memory.sh"
get_current_time_andup = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/date_uptime_check.sh"
get_cpu_temperature = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/cpu_temperature.sh"
get_swap_total_used_free = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/used_swap.sh"
get_cpu_usage = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/cpu_usage.sh"
cpu_user_sys = "/Users/matthewchadwell/server_environment/project_files/project_bash_files/cpu_usage_user_kernel.sh"





# Mock data stored local files
# Mock data stored in varaibales
Mock_GPU_data = "temp=109.670'C"
Mock_cpu_data = 79670
Mock_sys_load = "2.94, 2.58, 1.50"
Mock_memory = "MiB Mem : 7759.2 total, 6718.3 free, 389.0 used, 652.0 buff/cache"
mock_string_date_flag_s_not_avail = '2021-06-08 19:49:56 2021-06-08 19:48:56'
# server_info.py
mock_gpu_temp = "temp=100.99'C"
gpu_temperature = mock_gpu_temp
mock_sys_load = "2.94, 2.58, 1.50"
system_load = mock_sys_load
mock_sys_memory = "MiB Mem : 7759.2 total, 6718.3 free, 389.0 used, 652.0 buff/cache"
system_memory = mock_sys_memory
arm_cpu_reading = "/Users/matthewchadwell/server_environment/mock_cpu_arm_temp/temp"
# data is found at this location linux  , format  56000
mock_swap_average_use = "Total swap: 0 Used swap: 1000 Free swap: 10000"
# mock_swap_page_in_out = "Total swap: 3000 Used swap: 0  Page swap ins: 0 Page swap outs: 0"
mock_cpu_usage = "Cpu idle: 100.92 Io wait: 0.02"
mock_sys_usage = "%user: 0.01 %system: 0.02"
# Time cpu running user code and kernel(system) code and