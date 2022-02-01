"""

This script updates any attached Luminous Rex clock to
the current system time.  

https://www.luminousrex.com/clocks

"""

import sys 
import datetime, time
import struct

# Determine which FTDI library to use.
# Set True to use FTD2XX (Windows).  
# Set False to use pylibftdi (Linux)
FTD2XX = False 
# FTD2XX timeout in msec
FTDI_TIMEOUT = 1000

if FTD2XX:
	import ftd2xx as ftd
else:
	import pylibftdi as ftdi

"""
// eeprom c configuration struct
// 128 bytes in length
struct configuration_data_t
{
	uint32_t version;
	uint32_t timestamp_initialized;
	uint32_t timestamp;

	uint8_t  brightness_hours;
	uint8_t  brightness_minutes;
	uint8_t  brightness_seconds;
	uint8_t  is_24_hour;

	int16_t calibration_value;

	// pad out to 128 bytes
	uint8_t padding[110];
};
"""

CMD_PING = 0
CMD_SET_UNIX_TIMESTAMP = 1
CMD_GET_UNIX_TIMESTAMP = 2
CMD_WRITE_EEPROM_STRUCT = 3
CMD_READ_EEPROM_STRUCT = 4

CMD_RESPONSE_OK = 0
CMD_RESPONSE_ERROR = 1 

# open the first ftdi device found.
if FTD2XX:
	dev = ftd.open(0)
	dev.setTimeouts(FTDI_TIMEOUT, FTDI_TIMEOUT)
	dev.setBaudRate(1000000)
	dev.setDataCharacteristics(ftd.defines.BITS_8, ftd.defines.STOP_BITS_1, ftd.defines.PARITY_NONE)
	dev.setFlowControl(ftd.defines.FLOW_NONE)
else:
	ftdi.USB_PID_LIST.append(0x6015)
	dev = ftdi.Device()
	dev.baudrate = 1000000
	dev.ftdi_fn.ftdi_set_line_property(8, 1, 0)
	dev.ftdi_fn.ftdi_setflowctrl(0)
	dev.ftdi_fn.ftdi_set_latency_timer(500)

# generate read eeprom struct command
cmd = []
for i in range(16):
	cmd.append(0)
cmd[0] = CMD_READ_EEPROM_STRUCT

# send command
dev.write(bytes(cmd))

# wait for response
response = dev.read(128)

version, timestamp_initialized, timestamp, brightness_hours, brightness_minutes, brightness_seconds, is_24_hour, calibration_value, padding = struct.unpack('LLLBBBBh110s', response)

# get current system time.
pc_epoch = int(time.time())
# if local time is within daylight savings and a
# dst offset is defined, use the dst altzone for UTC offset
if time.localtime().tm_isdst and time.daylight:
	pc_offset = time.altzone
else:
	pc_offset = time.timezone

error_seconds = timestamp - (pc_epoch - pc_offset)

print("clock epoch: " + str(timestamp))
print("pc epoch: " + str(pc_epoch - pc_offset))
print("Lrex clock is " + str(error_seconds) + " seconds ahead of the system clock\n")

# set the current time and leave all other configuration values unchanged.
timestamp = pc_epoch - pc_offset

# send write eeprom struct command
cmd[0] = CMD_WRITE_EEPROM_STRUCT
dev.write(bytes(cmd))

# wait for response
response = dev.read(1)
if CMD_RESPONSE_OK != response[0]:
	print("Error in response from lrex clock.")
	exit()

cmd_data = struct.pack('LLLBBBBh110s', version, timestamp_initialized, timestamp, brightness_hours, brightness_minutes, brightness_seconds, is_24_hour, calibration_value, padding)
dev.write(bytes(cmd_data))

# wait for response
response = dev.read(1)
if CMD_RESPONSE_OK != response[0]:
	print("Error in response from lrex clock.")
	exit()
else:
	print("Clock time has been updated.")
