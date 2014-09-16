#!/usr/bin/python
"""
    A simple test tool for PICamera testing
"""

import time
import picamera

camera = picamera.PiCamera()

try:
    camera.start_preview()
    time.sleep(20)
    camera.stop_preview()
finally:
    camera.close()
    
