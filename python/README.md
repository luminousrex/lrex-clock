# Luminous Rex Clock Update Tool

This Python script updates your  [Luminous Rex clock](https://www.luminousrex.com/clocks) time via USB.  The script has been tested on a few different Linux distributions, and works well on a Raspberry Pi.

## Requirements

1. Python >=3
2. [libftdi](https://www.intra2net.com/en/developer/libftdi/)
3. [pylibftdi](https://github.com/codedstructure/pylibftdi) 

## Installation

First, install the the required libraries: 

```
pip install pylibftdi
sudo apt-get install libftdi-dev
```

In order to access the usb serial device from a user account, add a udev rule for libftdi:

```
sudo vi /etc/udev/rules.d/99-libftdi.rules
```

Add the following lines to the rules file: 

```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", GROUP="dialout", MODE="0660"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6010", GROUP="dialout", MODE="0660"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6011", GROUP="dialout", MODE="0660"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6014", GROUP="dialout", MODE="0660"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6015", GROUP="dialout", MODE="0660"
```

Connect the Luminous Rex clock to a USB port.  Wait 5-10 seconds for it to connect.  Run the script to update the clock's time:

```
python lrexclock.py
```
