# SenseHatStation

A cool weather station for Raspberry PI with SenseHat


## Features

- Two nice digital clock display
- Temperature and humidity
- Weather forecast using OpenWeatherMap

The teperature display is not really accurate because the Sense Hat sensor is not reliable and heavily influenced by the Raspberry CPU heat.

## Requirements

Python 3


## Installation

Copy the all the PiWClock files in a directory named.
This script will do the job for you

```
wget  xxx
unzip
```


## Run

```
python3 piwclock.py
```

## Configuration

All configuration settings are stored in the pywclock.cfg script.

The SenseHatStation changes the display automatically by rotating the Raspberry PI. This means that there are 4 positions available but consider that one side has normally a Micro USB connector attached to power the board.
What is displayed in the 4 positions is set in the pywclock.cfg script.

To be able to retrieve the weather forecast you must create a free account on OpenWeatherMap and generate an API code.
Latitude/longitude

## Autorun

After having configured your preferred displays and maybe tweaked the colors, you should now configure your PI to automatically start the PiWClock at boot.

Ensure the start.sh script is executable, typing this command:
```
chmod 755 start.sh
```

Type in:
```
sudo crontab -e
```
This will brings up a crontab window.
Now, enter the line:
```
@reboot sh /home/pi/piwclock/start.sh
```
This will execute the script once at startup.


To test if this is workin reboot your Pi using:
```
sudo reboot
```
	