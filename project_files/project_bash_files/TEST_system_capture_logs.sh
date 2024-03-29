#!/usr/local/bin/bash
# -- TODO Regex error

# --Note: ambient temp called from python script , sensor id configurable
#cpu_temp_reading
#gpu_temp_reading
#system_load
# - one_min_avg_load
# - five_min_avg_load
# - fifteen_min_avg_load
#system_memory
#percent_of_swap_used
#cpu_usage
#cpu_user_sys

#from reboot_check import reboot_counted
#
#from server_info import *cpu_temp_reading, *gpu_temp_reading, system_load \
#
#
#    percent_memory_used, *cpu_usage(cpu_idle/cpu_wait)  *swap_average_use, *sys_usage(kernel_time/cpu_user_time)

declare -A def_dict

# tips :
# declare the dictionary you want
# test - def_dict[keyA]=valueA
# test - echo ${def_dict}
# (alternative) way to add values to dictionary in bash
#def_dict+=( [free_swap]=$free_swap [total_swap]=$total_swap [used_swap]=$used_swap )


# ---------------- ( current time and uptime ) ---------------- #



current_date=$(date '+%F %H:%M:%S')
uptime_check=$(uptime -s)

current_and_uptime="$current_date $uptime_check"


#current_and_uptime="2021-06-08 01:30:00 2021-06-08 00:55:00"
# check
# echo $current_an_uptime
def_dict[current_and_uptime]=$current_and_uptime



# ---------------- (memory_used ) ---------------- #



memory=$(top -n 1 | grep "MiB Mem :")
regex='MiB Mem : ([0-9]+.[0-9]+) total, ([0-9]+.[0-9]+) free, [0-9]+.[0-9]+ used, [0-9]+.[0-9]+ buff\/cache'



if [[ "$memory" =~ $regex ]]; then
  system_memory="${BASH_REMATCH[0]}"
  def_dict[system_memory]=$system_memory
  # check
  # echo system_memory
else
    def_dict[system_memory]="NULL"
fi

#system_memory="MiB Mem : 1000.0 total, 5.0 free, 0.01 used, 5.0 buff/cache"


# --------------- (cpu_temp_reading) cpu_temperature.sh ---------------#

cpu_temp_reading=$(</sys/class/thermal/thermal_zone0/temp)
echo $cpu_temp_reading

#cpu_temp_reading=10000
#cpu_temp_reading=''
# echo "cpu temp: $cpu"

# check
# echo $cpu_temp_reading

#cpu_temp_reading=53000
def_dict[cpu_temp_reading]=$cpu_temp_reading



# --------------- (gpu_temp_reading) gpu_temperature.sh ---------------#

# need to setup config for username??

    # format temp=69.0'C
    # sudo usermod -aG video <username>   , add user name permission to run   vcgencmd

gpu_temp_reading=os.system('vcgencmd measure_temp')


# check --
#echo $gpu_temp_reading

# gpu_temp_reading="temp=100.000'C"
def_dict[gpu_temp_reading]=$gpu_temp_reading

#----------------- (return swap used) used_swap.sh  -------------------#




# check_pwap_in_out.sh    ---   check if swap has been allocated for machine
free_swap=$(free -t | awk 'FNR == 3 {print $4}')
used_swap=$(free -t | awk 'FNR == 3 {print $3}')
total_swap=$(free -t | awk 'FNR == 3 {print $2}')

swap_average_use=$("total swap: $total_swap used swap: $used_swap free_swap: $free_swap")

# check --
#echo "total swap: $total_swap used swap: $used_swap free_swap: $free_swap"


#test echo $swap_average_use
# need to create this string shown above --
#swap_average_use="Total swap: 1000 Used swap: 10 Free swap: 990"
def_dict[swap_average_use]=$swap_average_use



#---------------- ( return one,five,fifteen min load) -----------------#

#mock data
#system_load='load average: 0.17, 0.28, 0.26'
system_load='load average: 2.00, 1.00, 5.00'

# load is split function server_info.py - return_system_performance()

v=$(top | head -1)

regex='load average: ([0-9].[0-9]{2}, [0-9].[0-9]{2}, [0-9].[0-9]{2})'

if [[ "$v" =~ $regex ]]; then
  system_load=${BASH_REMATCH[1]}
# check
#  echo $(system_load)
else
   system_load="NULL"
# check
#  echo $(system_load)
fi


# system_load=$(system_load)
def_dict[system_load]=$system_load


#-------------- ( cpu_idle ) ------------------#

cpu_idle=$(iostat -c | awk 'FNR == 4 {print $6}')
io_wait=$(iostat -c | awk 'FNR == 4 {print $4}')



cpu_usage=$("Cpu idle: $cpu_idle Io wait: $io_wait")

# check
#echo "Cpu idle: $cpu_idle Io wait: $io_wait"

#cpu_usage='Cpu idle: 1.00 Io wait: 1.00'
def_dict[cpu_usage]=$cpu_usage

# ------------------- ( kernel_time, cpu_user_time ) ---------------#


user_title=$(iostat -c | awk 'FNR == 3 {print $2}')
# %user
user_time_non_kernel_code_running=$(iostat -c | awk 'FNR == 4 {print $2}')
# 0.01
system_title=$(iostat -c | awk 'FNR == 3 {print $4}')
# %system
system_time_code_running=$(iostat -c | awk 'FNR == 4 {print $4}')
# 0.02


cpu_user_sys=$("$user_title: $user_time_non_kernel_code_running $system_title: $system_time_code_running")

# check --
#echo $cpu_user_sys
cpu_user_sys="%user: 1.00 %system: 1.00"
def_dict[cpu_user_sys]=$cpu_user_sys



# -------------------- ( return dictionary ) -------------#

for i in ${!def_dict[@]};
 do
   echo "\""$i"\"":"\""${def_dict[$i]}"\""
  #  echo $i: ${def_dict[$i]}
#    arrVar+=$i ,${def_dict[$i]}
done