#!/bin/bash

date_time=`date "+%Y-%m-%d %H:%M:%S"`
used_swap=$(free -t | awk 'FNR == 3 {print $3}')
#total_swap=$(free -t | awk 'FNR == 3 {print $2}')

total_swap=3000
# mock data for testing a system with swap allocated to storage

echo $total_swap

if [[ $total_swap -gt 0 ]]
# if equals zero swap has not been allocated for the machine
then
    echo "None"
else
    cd /proc
    page_swap_in=$(cat vmstat | awk '$0 ~ /pswpin/ {print $2}')
    page_swap_out=$(cat vmstat | awk '$0 ~ /pswpout/ {print $2}')
    echo "$date_time Total swap: $total_swap Used swap: $used_swap  Page swap ins: $page_swap_in Page swap outs: $page_swap_out"
fi