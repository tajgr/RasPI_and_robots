#!/usr/bin/python
"""
   The script can shutdown the RasPi if the button is pressed down for 5 s.
"""

import RPi.GPIO as GPIO
import time
import subprocess

def ledLight( number = 3, lightTime = 0.3 ):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    for ii in range(number):
        GPIO.output( 11, True )
        time.sleep( lightTime )
        GPIO.output( 11, False )
        time.sleep( lightTime )

ledLight()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)
bdt = 0 #time when the button is pressed down. 
while True:
    buttonUp = GPIO.input(16)
    if buttonUp == False:
        bdt = bdt + 1
        print "button down"
    else:
        bdt = 0
    if bdt == 4:
        print "shutdown"
        ledLight()
        subprocess.call("halt")
        break
    time.sleep(1)