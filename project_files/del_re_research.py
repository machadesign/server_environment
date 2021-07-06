import re

temp_crc = "71 01 4b 46 7f ff 0f 10 56 : crc=56 YES"
temp_crc_check = re.match(r'YES$', temp_crc)

print(temp_crc_check)