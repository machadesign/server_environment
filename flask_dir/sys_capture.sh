#!/usr/local/bin/bash

declare -A def_dict



# ---------------- ( current time and uptime ) ---------------- #

# current_and_uptime="2021-06-08 19:54:56 2021-06-08 19:48:56"

# diff name for incoming value

# current_and_uptime="2021-06-08 19:50:56 2021-06-08 19:40:56"
# echo "$current_and_uptime2"

# https://www.cyberciti.biz/faq/bash-shell-find-out-if-a-variable-has-null-value-or-not/

if [[ $mock_current_and_uptime ]]   # defined then
        then
        	def_dict[current_and_uptime]=$mock_current_and_uptime
        else
        	current_and_uptime="2021-08-04 10:25:00 2021-08-04 10:00:00"
        	def_dict[current_and_uptime]=$current_and_uptime
        fi


# ---------------- (memory_used ) ---------------- #

# system_memory="MiB Mem : 7759.2 total, 6718.3 free, 389.0 used, 652.0 buff/cache"
if [[ $mock_system_memory ]]   # defined then
        then
        	def_dict[system_memory]=$mock_system_memory
        else
        	system_memory="MiB Mem : 7759.2 total, 6718.3 free, 389.0 used, 652.0 buff/cache"
        	def_dict[system_memory]=$system_memory
        fi


# --------------- (cpu_temp_reading) cpu_temperature.sh ---------------#


# cpu_temp_reading=59000

if [[ $mock_cpu_temp_reading ]]   # defined then
        then
        	def_dict[cpu_temp_reading]=$mock_cpu_temp_reading
        else
        	cpu_temp_reading=29000
        	def_dict[cpu_temp_reading]=$cpu_temp_reading
        fi





# def_dict[cpu_temp_reading]=$cpu_temp_reading




# --------------- (gpu_temp_reading) gpu_temperature.sh ---------------#


if [[ $mock_gpu_temp_reading ]]   # defined then
        then
        	def_dict[gpu_temp_reading]=$mock_gpu_temp_reading
        else
        	gpu_temp_reading="temp=29.000'C"
        	def_dict[gpu_temp_reading]=$gpu_temp_reading
        fi





# gpu_temp_reading="temp=110.000'C"
# def_dict[gpu_temp_reading]=$gpu_temp_reading

#----------------- (return swap used) used_swap.sh  -------------------#

if [[ $mock_swap_average_use ]]   # defined then
        then
        	def_dict[swap_average_use]=$mock_swap_average_use
        else
        	swap_average_use="Total swap: 1000 Used swap: 290 Free swap: 210"
        	def_dict[swap_average_use]=$swap_average_use
        fi








#swap_average_use="Total swap: 1000 Used swap: 200 Free swap: 300"
# def_dict[swap_average_use]=$swap_average_use



#---------------- ( return one,five,fifteen min load) -----------------#


if [[ $mock_sys_load ]]   # defined then
        then
        	def_dict[system_load]=$mock_sys_load
        else
        	system_load="load average: 2.97, 2.98, 2.96"
        	def_dict[system_load]=$system_load
        fi



#mock data


# load is split function server_info.py - return_system_performance()

#v=$(top | head -1)
#
#regex='load average: ([0-9].[0-9]{2}, [0-9].[0-9]{2}, [0-9].[0-9]{2})'
#
#if [[ "$v" =~ $regex ]]; then
#  system_load=${BASH_REMATCH[1]}
#else
#   system_load="NULL"
#fi


# system_load=$(system_load)

# system_load="load average: 1.17, 1.28, 1.26"
# def_dict[system_load]=$system_load


#-------------- ( cpu_idle ) ------------------#


if [[ $mock_cpu_usage ]]   # defined then
        then
        	def_dict[cpu_usage]=$mock_cpu_usage
        else
        	cpu_usage="Cpu idle: 20.00 Io wait: 90.00"
        	def_dict[cpu_usage]=$cpu_usage
        fi



# mock data


#cpu_idle=$(iostat -c | awk 'FNR == 4 {print $6}')
#io_wait=$(iostat -c | awk 'FNR == 4 {print $4}')
#
#echo "Cpu idle: $cpu_idle Io wait: $io_wait"

# cpu_usage=$("Cpu idle: $cpu_idle Io wait: $io_wait")


# cpu_usage="Cpu idle: 100.00 Io wait: 0.10"
# def_dict[cpu_usage]=$cpu_usage

# ------------------- ( kernel_time, cpu_user_time ) ---------------#



if [[ $mock_cpu_user_sys ]]   # defined then
        then
        	def_dict[cpu_user_sys]=$mock_cpu_user_sys
        else
        	cpu_user_sys="%user: 0.29 %system: 0.29"
        	def_dict[cpu_user_sys]=$cpu_user_sys
        fi

#user_title=$(iostat -c | awk 'FNR == 3 {print $2}')
## %user
#user_time_non_kernel_code_running=$(iostat -c | awk 'FNR == 4 {print $2}')
## 0.01
#system_title=$(iostat -c | awk 'FNR == 3 {print $4}')
## %system
#system_time_code_running=$(iostat -c | awk 'FNR == 4 {print $4}')
## 0.02
#echo "$user_title: $user_time_non_kernel_code_running $system_title: $system_time_code_running"

# cpu_user_sys=$("$user_title: $user_time_non_kernel_code_running $system_title: $system_time_code_running")


# cpu_user_sys="%user: 0.10 %system: 0.10"
# def_dict[cpu_user_sys]=$cpu_user_sys

# --------------------- ( ambient sensor data ) -----------------#

# check if temp data crc check and data is exported correctly , but do not add to the dictionary
# mock data in the data check file is redirected to the mock sensor data location
# checked successfully mock data exported (not used in this dict) changes mock check to true to indicate use of mock sensor data file

#mock_ambient_sensor_CRC="${BASH_REMATCH[9]}"
#mock_ambient_temp="${BASH_REMATCH[11]}"
if [[ $mock_ambient_sensor_CRC ]] && [[ $mock_ambient_temp ]]   # defined then
        then
            mock_ambient_sensor_on="true"
        	def_dict[mock_ambient_sensor_on]=$mock_ambient_sensor_on
        else
        	mock_ambient_sensor_on="false"
            def_dict[mock_ambient_sensor_on]=$mock_ambient_sensor_on
        fi

# -------------------- ( return dictionary ) -------------#

for i in ${!def_dict[@]};
 do
   echo "\""$i"\"":"\""${def_dict[$i]}"\""
  #  echo $i: ${def_dict[$i]}
#    arrVar+=$i ,${def_dict[$i]}
done