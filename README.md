# Raspberry Pi TCP2Serial

## What is this?

The goal of this project is to rediect all Serial interface comunication to/from a TCP session.
That way, it will be possible to have remote access to any serial console.
On top of that, it also provides the ability to store all serial printable and timestamped output into log file.
By using a raspberry Pi, it is possible to keep logging all data, 24/7 (kind of "black box"), and still be able to interact with the serial interface.  

The base of the code is the example [TCP to Serial Redirect](https://github.com/pyserial/pyserial/blob/master/examples/tcp_serial_redirect.py) existing in project [pySerial](https://github.com/pyserial/pyserial).
It takes cares of all Serial and TCP (telnet) data redirection.
On top of that excelent example, I'm just adding the timestamp on every text line and saving all output to log files.

## Instalation on Raspberry Pi

### 1- Hardware Wiring

![pinout](https://raw.githubusercontent.com/albkirk/TCP2Serial/main/images/GPIO-Pinout-Diagram-2.png)
On the raspberry pi
Use the following pins:

- 6 -> Ground

- 8 -> TX

- 10 -> RX

On your device use the correspondent  **TX + RX + Ground**  pins.

The other device could any device, such as ESP8266, ES32, nrf51822 ... or other MCU.

In my example, I'm connecting to a prototype device  
![tchpinout](https://raw.githubusercontent.com/albkirk/TCP2Serial/main/images/tchpinout.jpg)

### 2- OS

The tested and recomended OS is the [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/).
Burn the image on the SD-Card using the Balena Etcher and enable [SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/README.md) (see chapter 3).

If you are using the RPi3 or newer, you also need to disable BT by adding the following line at the end of file **/boot/config.txt**.
```
dtoverlay=pi3-disable-bt
``` 

### 3- Network Connection

Connect the raspberry pi to your home LAN network using an Ethernet cable.
[Check the Raspberry Pi IP on you HomeGateway](https://www.raspberrypi.org/documentation/remote-access/ip-address.md)

### 4- Serial Setup

To enable the serial interface on the Raspberry pi side start the [raspi-config](https://www.raspberrypi.org/documentation/configuration/raspi-config.md)

```bash
sudo raspi-config
```

![raspi](https://raw.githubusercontent.com/albkirk/TCP2Serial/main/images/raspi-config.png)
Go to **"3 Interface Options"**  and enable **"P6 Serial Port"**.

Anwser "NO" to this
![raspi](https://raw.githubusercontent.com/albkirk/TCP2Serial/main/images/serial_login.jpg)

and "YES" to this
![raspi](https://raw.githubusercontent.com/albkirk/TCP2Serial/main/images/hw_enabled.jpg)


### 5- Python

The code is writen for python3. So, make sure you have this version installed.

### 6- Python Module

The code need to have installed a the python module [pySerial](https://github.com/pyserial/pyserial).

On the SSH console execute the commands:

```bash
sudo apt install python3-pip
python3 -m pip install pyserial
```

### 7- Identify the Serial interface

```bash
dmesg | grep tty
```

```bash
...
[    0.001357] printk: console [tty1] enabled
[    2.968291] 20201000.serial: ttyAMA0 at MMIO 0x20201000 (irq = 81, base_baud = 0) is a PL011 rev2
[    7.657641] systemd[1]: Created slice system-getty.slice.
...
```

in this case it shall use **/dev/ttyAMA0**

### 8- The TCP2Serial Code

get a copy of both files from **/code** to yout raspberry pi **/home/pi/** folder (or subfolder)

- **tcp2serial.py**

- **t2saux.py**

create the folder **/home/pi/logs/**

```bash
mkdir logs
```

### 9 - Run the tool

to run the code enter the following command

```bash
python3 tcp2serial.py -P 3000 /dev/ttyAMA0 115200
```

to run the code on the RPi3 the command will be following

```bash
python3 tcp2serial.py -P 3000 /dev/serial0 115200
```


### 10- Start it at boot

It is suggested to start the tool at boot by using  crontab, by appending the last line below:

```bash
$ crontab -e
# Edit this file to introduce tasks to be run by cron.
#

...

#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
@reboot /usr/bin/python3 /home/pi/tcp2serial.py -P 3000 /dev/ttyAMA0 115200 2>&1 >> /home/pi/logs/debug.log

```

## -.-

## .-.

## How to use the tool

### 1- Get access to Serial Comunication from your PC
On the PC open a telnet session on port 3000.
Here's an example using [putty](https://www.putty.org/).
![putty](https://raw.githubusercontent.com/albkirk/TCP2Serial/main/images/putty.jpg)

### 2- The LOG Files
Log Files are stored on (configurable) folder directory **/home/pi/logs**. Files are automatically organized into subfolders Year and Month.
```
pi@raspberry:~ $ ls  -R  /home/pi/logs/
/home/pi/logs/:
2021  debug.log

/home/pi/logs/2021:
03

/home/pi/logs/2021/03:
2021-03-25_17H_serial.log  2021-03-26_11H_serial.log  2021-03-27_05H_serial.log  2021-03-27_23H_serial.log
...
```

New log files is created every new hour.

**IMPORTANT** The raspberry pi **MUST** be able to sincronize the date/time using NTP. 
