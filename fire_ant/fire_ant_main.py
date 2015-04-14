#!/usr/bin/python
"""
  The main program for Fire Ant.
"""

import RPi.GPIO as GPIO
import picamera
import time
import sys


def fireAntMain():
    pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    print "STARTED"
    fireAntMain()
