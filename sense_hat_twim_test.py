import time

from sense_hat_twim import SenseHatTwim

import piwclock_cfg as cfg

COL_RED = [200,0,0]
COL_GREEN = [0,200,0]
COL_BLUE = [0,0,200]
COL_OFF = [0,0,0]


sense = SenseHatTwim()
sense.clear()

print("Orientation is %d " % sense.get_orientation())

print("Test auto_rotate_display")
sense.auto_rotate_display()


print("Test draw_circ_bar")
for x in range(0, 29):
    sense.draw_circ_bar(x, COL_RED, COL_OFF)
    time.sleep(.1)


print("Test show_openweather_forecast")
sense.show_openweather_forecast(cfg.OW_AIPKEY, cfg.OW_LAT, cfg.OW_LON, cfg.OW_DAY)
time.sleep(4)


#quit()


print("Test show_icon")
sense.show_icon('SUN')
time.sleep(1)
sense.show_icon('CLOUD')
time.sleep(1)
sense.show_icon('SHOWERS')
time.sleep(1)
sense.show_icon('RAIN')
time.sleep(1)
sense.show_icon('STORM')
time.sleep(1)
sense.show_icon('SNOW')
time.sleep(1)


time.sleep(1)
sense.clear()
print("Test show_digit34")
for x in range(0, 10):
    sense.show_digit34(x, 0, 0, COL_RED)
    time.sleep(.4)

time.sleep(1)
sense.clear()
print("Test show_digit35")
for x in range(0, 10):
    sense.show_digit35(x, 3, 3, COL_BLUE)
    time.sleep(.4)

time.sleep(1)
sense.clear()
print("Test show_digits34")
for x in range(0, 100):
    sense.show_digits34(x, 1, 1, COL_GREEN)
    time.sleep(.1)

time.sleep(1)
sense.clear()
print("Test show_digits35")
for x in range(0, 100):
    sense.show_digits35(x, 0, 0, COL_RED)
    time.sleep(.1)

time.sleep(1)
sense.clear()
print("Test show_tiny_hour")
for x in range(0, 13):
    sense.show_tiny_hour(x, 2, COL_GREEN)
    time.sleep(.2)

time.sleep(1)
sense.clear()
