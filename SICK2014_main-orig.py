#!/usr/bin/python
"""
  The main program of the comteticion Sick Robot Day 2014
"""

import RPi.GPIO as GPIO
import picamera
import time
import sys

from picamera_tool import *
from Digit_detect import *

def ledLight():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11, True)
    time.sleep(5)
    GPIO.output(11, False)

def sickMain( workingTime = 60, saving = True ):
    detected = []
    logs = open("/home/pi/git/RasPI_and_robots/logs/detection.txt", "a")
    stream = io.BytesIO()
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
#    camera.start_preview()
    time.sleep(2)
    A=Digit_detect('',20)
    A.learn_from_file('/home/pi/git/RasPI_and_robots/samples.data','/home/pi/git/RasPI_and_robots/responses.data')
    index = 0
    timeStart = time.time()
    actulalTime = time.time()
    while timeStart > actulalTime - workingTime:
        actulalTime = time.time()
        
        camera.capture(stream, format='jpeg')
        #    Construct a numpy array from the stream
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        #    "Decode" the image from the array, preserving colour
        image = cv2.imdecode(data, 1)
        stream.seek(0)
        stream.truncate()
        
        if saving:
#            actualTime = time.time()
            filename = timeName( "/home/pi/git/RasPI_and_robots/logs/image_", ".jpg", "%03d"%index )
#            camera.capture( filename )
            cv2.imwrite( filename, image )
            index = index + 1
#        print A.detect_digits_from_file('SICK_ROBOT/001.jpg')
        print filename
#        detected = A.detect_digits_from_file(filename)
        detected = A.detect_digits(image)
        print detected
        logs.write(filename.split("/")[-1] + str(detected ) + "\r\n")
        logs.flush()
    
    logs.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    sickMain( workingTime = 20 )