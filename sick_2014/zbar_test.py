#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  The tool for barcode reading
"""
# zbar
#instaling: sudo apt-get install python-zbar
#http://zbar.sourceforge.net/
#https://github.com/ZBar/ZBar/tree/master/python/examples

import io
import time
import picamera
from PIL import Image
import zbar
import sys

def runBarcodeReader():
#   Create the in-memory stream
    stream = io.BytesIO()
    camera = picamera.PiCamera()
    camera.start_preview()
    time.sleep(2)
    camera.capture(stream, format='jpeg')
#   "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    pil = Image.open(stream)

#   create a reader
    scanner = zbar.ImageScanner()

#   configure the reader
    scanner.parse_config('enable')
    
    pil = pil.convert('L')
    width, height = pil.size
    raw = pil.tostring()
    
#   wrap image data
    image = zbar.Image(width, height, 'Y800', raw)
    
#   scan the image for barcodes
    scanner.scan(image)

#   extract results
    for symbol in image:
#   print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        print symbol.type, symbol.data
    
#   clean up
    del(image)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    runBarcodeReader()
