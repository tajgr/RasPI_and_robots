#!/usr/bin/python
"""
  The main program for Fire Ant.
"""

import RPi.GPIO as GPIO
import picamera
import time
import sys
import datetime
import serial
import math
import io
from thread import start_new_thread

sys.path.append( "/home/pi/git/fireant/serial_servo" )
sys.path.append( "/home/pi/git/fireant/ver1")
sys.path.append( "/home/pi/git/fireant/ver0")
from serial_servo import LogIt, ReplayLog, ReplyLogInputsOnly, LogEnd
from fireant import *
from triangle import pos2angles10thDeg, angles10thDeg2pos


SERIAL_BAUD =  9600 #38400 #62500 #38400


def timeName( prefix, ext, index ):
  dt = datetime.datetime.now()
  index = "_" + index
  filename = prefix + dt.strftime("%y%m%d_%H%M%S") + index + ext
  return filename

def picameraToCv2( saving = True ):
#    Create the in-memory stream
    stream = io.BytesIO()
    camera = picamera.PiCamera()
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')
#    Construct a numpy array from the stream
    data = np.fromstring(stream.getvalue(), dtype=np.uint8)
#    "Decode" the image from the array, preserving colour
    image = cv2.imdecode(data, 1)
    ii = 0
    if saving:
        actulalTime = time.time()
        index = str(ii)
        filename = timeName( "/home/pi/git/RasPI_and_robots/fire_ant/logs/image_", ".jpg", index )
        cv2.imwrite( filename, image )
        ii = ii + 1
    return image

def imageSave( workingTime = 300.0, test = 0 ):
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(2)
    timeStart = time.time()
    actulalTime = time.time()
    ii = 0
    #while timeStart > actulalTime - workingTime:
    while True:
        actulalTime = time.time()
        index = str(ii)
        filename = timeName( "/home/pi/git/RasPI_and_robots/fire_ant/logs/image_", ".jpg", index )
        camera.capture( filename )
        ii = ii + 1
        time.sleep(0.5)

def robotGo():
    com = LogIt( serial.Serial( '/dev/ttyAMA0', SERIAL_BAUD ) )
    robot = FireAnt( "Due", com )
    
    robot.standUp()
    ii = 0
    while True:
        redButton = GPIO.input(22)
        if redButton == True:
            break
        
        if ii == 3:
            a = math.radians(0)
            ii = 0
        else:
            a = 0
            
        robot.walk( step=(0.02, 0.0, a), numSteps=1)
        #robot.walk( step=(0.0, -0.02, 0.0), numSteps=1) 
        #robot.walk( step=(0.0, 0.0, math.radians(5)), numSteps=2)
        ii += 1
        
    robot.sitDown()
    robot.stopServos()


def fireAntMain():
    #imageSave()
    #picameraToCv2()
    #sys.exit(1)
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(22, GPIO.IN)
    redButton = GPIO.input(22)
    while True:
        time.sleep(1)
        redButton = GPIO.input(22)
        if redButton == False:
            robotGo()
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    print "STARTED"
    start_new_thread( imageSave, (300.0, 0) )
    fireAntMain()
