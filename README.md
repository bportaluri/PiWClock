# SenseHatStation

A cool weather station for Raspberry PI with SenseHat.


## Features

- Two nice digital clock display modes
- Temperature and humidity (not accurate)
- Weather forecast using OpenWeatherMap



## Requirements

- Raspberry Pi 2 or 3
- Sense HAT


## Installation

Copy the all the PiWClock files in a directory named *piwclock* under your home dir.
This script will do the job for you:

```
cd ~
wget https://github.com/bportaluri/PiWClock/archive/master.zip
unzip -j -d piwclock master.zip
```


## Run

```
python3 piwclock.py
```

## Configuration

All configuration settings are stored in the *pywclock.cfg* script.

The SenseHatStation changes the display automatically by rotating the Raspberry PI. This means that there are 4 positions available but consider that one side has normally a micro-USB connector attached to power the board.
What is displayed in the 4 positions is defined in the *pywclock.cfg* script.

To be able to retrieve the weather forecast you must create a free account on [OpenWeatherMap](https://openweathermap.org/) and generate an API Key.
Find out your location latitude and longitude and update your coordinates in the configuration file.

## Autorun

After having configured your preferred displays and maybe tweaked the colors, you should now configure your PI to automatically start the PiWClock at boot.

Type in:
```
sudo crontab -e
```
This will brings up the editor.
Enter the following line at the end:
```
@reboot python3 /home/pi/piwclock/piwclock.py
```
This will execute the *piwclock.py* script at startup.

To test if this is working reboot your Pi and verify the program is started automatically.
```
sudo reboot
```


## Troubleshooting


### Configuration file not found
You get the following error:
```
ImportError: No module named 'piwclock_cfg'
```
Rename *piwclock_cfg.py.example* to *piwclock_cfg.py*.


### Python 3
You get the following error:
```
ImportError: No module named http.client
```
The PiWClock runs on Python 3 ensure to launch it with the correct command:
```
python3 piwclock.py
```

### Wrong temperature

The temperature display is not really accurate because the Sense Hat sensor is not reliable and heavily influenced by the Raspberry CPU heat.
There is not much we can do for this. Sorry.
