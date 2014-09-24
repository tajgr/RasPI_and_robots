#!/usr/bin/python
"""
  The main program of the comteticion Sick Robot Day 2014
"""

import RPi.GPIO as GPIO
import time
import sys

# test function
def sickMain():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11, True)
    time.sleep(5)
    GPIO.output(11, False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    sickMain()