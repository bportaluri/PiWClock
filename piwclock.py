import os
import time

from sense_hat_twim import SenseHatTwim

import piwclock_cfg as cfg


sense = SenseHatTwim()


def do_clock(force_redraw):
  if not hasattr(do_clock, "prev_hour"):
    do_clock.prev_hour = 0
    do_clock.prev_min = 0

  t = time.localtime()
  
  if do_clock.prev_hour!=t.tm_hour and do_clock.prev_hour!=0 and force_redraw==False:
    for x in range(100, 0, -1):
      sense.show_digits34(do_clock.prev_hour, 0, 0, sense.scale_rgb_color(cfg.HOURS_COLOR, x))
  if do_clock.prev_hour!=t.tm_hour or force_redraw==True:
    for x in range(0, 100):
      sense.show_digits34(t.tm_hour, 0, 0, sense.scale_rgb_color(cfg.HOURS_COLOR, x))
  do_clock.prev_hour=t.tm_hour

  if do_clock.prev_min!=t.tm_min and do_clock.prev_min!=0 and force_redraw==False:
    for x in range(100, 0, -1):
      sense.show_digits34(do_clock.prev_min, 0, 4, sense.scale_rgb_color(cfg.MINUTES_COLOR, x))
  if do_clock.prev_min!=t.tm_min or force_redraw==True:
    for x in range(0, 100):
      sense.show_digits34(t.tm_min, 0, 4, sense.scale_rgb_color(cfg.MINUTES_COLOR, x))
  do_clock.prev_min=t.tm_min


def do_clock2(force_redraw):
  if not hasattr(do_clock2, "prev_hour"):
    do_clock2.prev_hour = 0
    do_clock2.prev_min = 0

  t = time.localtime()
  if do_clock2.prev_hour!=t.tm_hour or force_redraw==True:
    sense.clear()
  
  sense.show_tiny_hour(t.tm_hour%12, 2, cfg.HOURS_COLOR)
  do_clock2.prev_hour = t.tm_hour

  px = round(t.tm_min*29/60)
  
  sense.draw_circ_bar(px, cfg.MINBAR_COLOR, cfg.BKG_COLOR)

  
def do_wforecast(force_redraw):

  sense.show_openweather_forecast(cfg.OW_AIPKEY, cfg.OW_LAT, cfg.OW_LON, cfg.OW_DAY)
  

def do_temp(force_redraw):

  t = round(sense.get_corrected_temperature())
  sense.show_digits35(t, 0, 2, cfg.TEMPERATURE_COLOR)


def do_humidity(force_redraw):

  h = round(sense.get_humidity())
  sense.show_digits35(h, 0, 2, cfg.HUMIDITY_COLOR)



#-------------------------------------------------------------------------------
#  M A I N
#-------------------------------------------------------------------------------

sense.clear()

prev_orientation = 99
force_redraw = False


while True:

  orientation = sense.get_orientation()
  mode = cfg.MODES[orientation]

  if orientation!=prev_orientation:
    print("Orientation: %d" % orientation)
    print("Mode       : %d" % mode)
    sense.clear()
    sense.set_rotation(orientation*90)
    force_redraw = True
    prev_orientation = orientation
  
  if mode==0:
    do_clock(force_redraw)
  if mode==1:
    do_clock2(force_redraw)
  if mode==2:
    do_wforecast(force_redraw)
  if mode==3:
    do_temp(force_redraw)
  if mode==4:
    do_humidity(force_redraw)
 
  force_redraw = False
  time.sleep(1)

