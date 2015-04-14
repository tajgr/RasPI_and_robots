#!/usr/bin/python
"""
Tools for PiCamera
"""

import io
import time
import datetime
import picamera
import cv2
import sys
import numpy as np

# Martin's function from heidi/airrace_drone.py
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
        filename = timeName( "/home/pi/git/RasPI_and_robots/logs/image_", ".jpg", index )
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
        filename = timeName( "/home/pi/git/RasPI_and_robots/logs/image_", ".jpg", index )
        camera.capture( filename )
        ii = ii + 1

if __name__ == "__main__":
    print __doc__
#    sys.exit()
    picameraToCv2( )
#    imageSave()