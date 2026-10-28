import os, sys, io
import M5
from M5 import *
from hardware import RGB



rgb15 = None


toggleRGB = None


def setup():
  global rgb15, toggleRGB

  M5.begin()
  Widgets.setRotation(1)
  Widgets.fillScreen(0x222222)

  toggleRGB = False
  rgb15 = RGB(io=15, n=10, type="SK6812")


def loop():
  global rgb15, toggleRGB
  M5.update()
  if toggleRGB == True:
    rgb15.fill_color(0x003300)
    rgb15.set_brightness(10)
  else:
    rgb15.set_brightness(0)
  if BtnA.wasDoubleClicked():
    toggleRGB = not toggleRGB


if __name__ == '__main__':
  try:
    setup()
    while True:
      loop()
  except (Exception, KeyboardInterrupt) as e:
    try:
      from utility import print_error_msg
      print_error_msg(e)
    except ImportError:
      print("please update to latest firmware")
