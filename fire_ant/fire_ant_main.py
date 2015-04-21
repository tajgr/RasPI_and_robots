#!/usr/bin/python
"""
  The main program for Fire Ant.
"""

import RPi.GPIO as GPIO
import picamera
import time
import sys


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

def imageSave( workingTime = 10.0 ):
    camera = picamera.PiCamera()
    camera.start_preview()
    time.sleep(2)
    timeStart = time.time()
    actulalTime = time.time()
    ii = 0
    while timeStart > actulalTime - workingTime:
        actulalTime = time.time()
        index = str(ii)
        filename = timeName( "/home/pi/git/RasPI_and_robots/fire_ant/logs/image_", ".jpg", index )
        camera.capture( filename )
        ii = ii + 1


def fireAntMain():
    imageSave()
    #picameraToCv2()
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    print "STARTED"
    fireAntMain()
