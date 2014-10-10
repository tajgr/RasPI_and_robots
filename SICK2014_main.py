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

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("192.168.1.1", 8000),
                            requestHandler=RequestHandler)
server.register_introspection_functions()


class MyFuncs:
    def init( self ):
        self.logs = open("/home/pi/git/RasPI_and_robots/logs/detection.txt", "a")
        self.stream = io.BytesIO()
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        time.sleep(2)
        self.A = Digit_detect('',24)
        self.A.learn_from_file('/home/pi/git/RasPI_and_robots/new_samples','/home/pi/git/RasPI_and_robots/new_responses')
        self.index = 0
        return 1

    def step( self ):
        print "STEP"
        self.camera.capture(self.stream, format='jpeg')
        #    Construct a numpy array from the stream
        data = np.fromstring(self.stream.getvalue(), dtype=np.uint8)
        #    "Decode" the image from the array, preserving colour
        image = cv2.imdecode(data, 1)
        self.stream.seek(0)
        self.stream.truncate()
        filename = timeName( "/home/pi/git/RasPI_and_robots/logs/image_", ".jpg", "%03d" % self.index )
        cv2.imwrite( filename, image )
        self.index += 1
        print filename
        try:
           detected = self.A.detect_digits(image)
        except:
           print "EXCEPTION"
           detected = []
        print detected
        self.logs.write(filename.split("/")[-1] +'\t'+ str(detected ) + "\r\n")
        self.logs.flush()
        return [filename.split("/")[-1]] + detected

    def term( self ):
        self.logs.close()
        self.camera.close()
        self.logs = None
        self.camera = None
        self.stream = None
        return 1

server.register_instance(MyFuncs())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    print "STARTED"
    server.serve_forever()

#-------------------------------------------------------------------
# vim: expandtab sw=4 ts=4 

