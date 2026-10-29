import os, sys, io
import M5
from M5 import *
import time






def setup():

  M5.begin()
  Widgets.setRotation(1)
  Widgets.fillScreen(0x222222)

  M5.Display.drawImage("/flash/res/img/bg.jpg", 0, 0, 320, 240, 0, 0, 0.92, 0.92)
  M5.Display.setCursor(103, 100)
  M5.Display.setFont(Widgets.FONTS.Montserrat40)
  M5.Display.print('Hello', 0xcc0000)
  time.sleep(3)
  M5.Display.clear(0xc0c0c0)


def loop():
  M5.update()


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
