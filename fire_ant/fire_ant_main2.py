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
from multiprocessing import Process, Queue
import numpy as np
import cv2

from img_processing import *

sys.path.append( "/home/pi/git/fireant/serial_servo" )
sys.path.append( "/home/pi/git/fireant/ver1")
sys.path.append( "/home/pi/git/fireant/ver0")
from serial_servo import LogIt, ReplayLog, ReplyLogInputsOnly, LogEnd
from fireant import *
from triangle import pos2angles10thDeg, angles10thDeg2pos


SERIAL_BAUD =  9600 #38400 #62500 #38400

g_index = 0
g_queueOut = None
g_processor = None
g_queueResults = None


def timeName( prefix, ext, index ):
  dt = datetime.datetime.now()
  index = "_" + index
  filename = prefix + dt.strftime("%y%m%d_%H%M%S") + index + ext
  return filename


#def imageSave( workingTime = 300.0, test = 0 ):
def processMain( queueIn, queueOut ):
    stream = io.BytesIO()
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(2)
    
    timeStart = time.time()
    actulalTime = time.time()
    ii = 0
    #while timeStart > actulalTime - workingTime:
    while True:
        shouldWork = queueIn.get()
        if shouldWork is None:
            print "close camera" 
            camera.close()
            break
        
        camera.capture(stream, format='jpeg')
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(data, 1)
        actulalTime = time.time()
        index = str(ii)
        filename = timeName( "/home/pi/git/RasPI_and_robots/fire_ant/logs/image_", ".jpg", index )
        cv2.imwrite( filename, img )
        stream.seek(0)
        stream.truncate()
        
        imgResult = imgProcessingMain( img, filename, directory = "" )
        ii = ii + 1
        queueOut.put( ( [ filename, imgResult ] ) )
        
#        time.sleep(0.5)

def getNewPicture( firstInit ):
    global g_queueOut, g_processor, g_queueResults
    if g_queueOut is None:
        g_queueOut = Queue()
        g_queueResults = Queue()
        g_processor = Process( target=processMain, args=(g_queueOut,g_queueResults,) )
        g_processor.daemon = True
        g_processor.start()
    if firstInit:
        g_queueOut.put_nowait( 1 )
        return None

    elif firstInit is None:
        g_queueOut.put_nowait( None )
        time.sleep(1)
        g_queueOut = None

    else:
        if g_queueResults.empty():
            return None
        ret = g_queueResults.get()
        g_queueOut.put_nowait( 1 )
        return ret        


def robotGo():
    logsRpiName = timeName( "/home/pi/git/RasPI_and_robots/fire_ant/logs/logsRpi_", ".txt", "" )
    rpiLogs  = open( logsRpiName, "w")
    com = LogIt( serial.Serial( '/dev/ttyAMA0', SERIAL_BAUD ) )
    robot = FireAnt( "Due", com )
    
    getNewPicture( firstInit=True )
    robot.standUp()
    ii = 0
    while True:
        redButton = GPIO.input(22)
        if redButton == True:
            break
        
        a = 0
        picResult = getNewPicture( firstInit=False )
        if picResult is not None:
            print picResult
            contoursXYC = picResult[1]
            bigL = 0
            bigR = 0
            smL = 0
            smR = 0
            vBigL = 0
            vBigR = 0
            
            for item in contoursXYC:
                if item[0] < 500:
                    if item[1] < 320:
                        smL += 1
                    else:
                        smR += 1
                elif item[0] < 5000:
                    if item[1] < 280:
                        bigL += 1
                    elif item[1] > 360:
                        bigR += 1
                else:
                    if item[1] < 280:
                        vBigL += 1
                    elif item[1] > 360:
                        vBigR += 1
            
            print "sm l r:", smL, smR
            print "big l r: ", bigL, bigR
            print "vBig l r: ", vBigL, vBigR
            
            direction = None
            if ( vBigL == 0 ) and ( vBigR == 0 ):
                if bigL > bigR *2.0:
                    direction = "R"
                elif bigR > bigL *2.0:
                    direction = "L"
                
            elif vBigL == 0:
                direction = "L"
               
            elif vBigR == 0:
                direction = "R"
            
            else:
                direction = None
            
            ###
            #direction = "L"            
            ###
            if direction == "L":
                a = math.radians(5)
                
            elif direction == "R":
                a = math.radians(-5)
                
            rpiLogs.write( str(ii)+"\r\n")
            rpiLogs.write( str( picResult[0] )+"\r\n")
            rpiLogs.write( str( contoursXYC )+"\r\n")
            rpiLogs.write( "sm l r:"+str(smL)+", "+str(smR)+"\r\n")
            rpiLogs.write( "big l r:"+str(bigL)+", "+str(bigR)+"\r\n")
            rpiLogs.write( "vBig l r:"+str(vBigL)+", "+str(vBigR)+"\r\n")
            rpiLogs.write( str(direction)+"\r\n")
            
        robot.walk( step=(0.02, 0.0, a), numSteps=1)
        #robot.walk( step=(0.0, -0.02, 0.0), numSteps=1) 
        #robot.walk( step=(0.0, 0.0, math.radians(5)), numSteps=2)
        ii += 1
        
    robot.sitDown()
    robot.stopServos()
    getNewPicture(None)
    rpiLogs.close()


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
#    start_new_thread( imageSave, (300.0, 0) )
    fireAntMain()

# vim: expandtab sw=4 ts=4 

