#!/usr/bin/python
"""
  Image processing for FRE 2015
"""

import sys
import os
import cv2
import numpy as np
#from matplotlib import pyplot as plt


def getFilesN( directory ):
    fileList = os.listdir( directory )
    #print fileList
    
    cleanFileL = []
    for fileN in fileList:
        if fileN.split(".")[-1] == "jpg":
            cleanFileL.append( fileN )
    
    print len(cleanFileL)
    return cleanFileL


#def getHist( grayImg ):
#    showImg( grayImg )
#    plt.hist( grayImg.ravel(), 256,[0,256])
#    plt.show()


def cutImage(img, xi, yi, xe, ye ):
    img = img[yi:ye, xi:xe]
    if imShow == True:
        showImg( img )
    return img


def getThreshold( gray, thrValue ):
    ret, binaryImg = cv2.threshold( gray, thrValue, 255,cv2.THRESH_BINARY_INV)
    return binaryImg
    

def openingClosing( binaryImg, ker1 = 5, ker2 = 2 ):
    newBinaryImg = None
    kernel = np.ones( ( ker1, ker1 ), np.uint8 )
    newBinaryImg = cv2.morphologyEx( binaryImg, cv2.MORPH_OPEN, kernel)
    
    if ker2 != None:
        kernel = np.ones( ( ker2, ker2 ), np.uint8 )
        newBinaryImg = cv2.morphologyEx( newBinaryImg, cv2.MORPH_CLOSE, kernel)
        
    return newBinaryImg


def dataFromDirectory( directory ):
    fileNames = getFilesN( directory )
    for fileN in fileNames:
        print fileN
        imgProcessingMain( fileN, directory )


def imgProcessingMain( img, imgFileName, directory = "" ):
    if img:
        cv2.imwrite(directory + imgFileName, img )
    if img == None:
        img = cv2.imread( directory + imgFileName )
    try:
        img2 = img[240:480, :]
        
        laplacian = cv2.Laplacian(img2,cv2.CV_32F)
        #cv2.imwrite(directory + imgFileName.split(".")[0]+"_lap.png", laplacian )
        gray = cv2.cvtColor( laplacian, cv2.COLOR_BGR2GRAY )
        #cv2.imwrite( directory + imgFileName.split(".")[0]+"_gray.png", gray )
        
        #getHist( gray )
        binaryImg = getThreshold( gray, 12 )
        #cv2.imwrite( directory + imgFileName.split(".")[0]+"_bi0.png", binaryImg )
        binaryImg = openingClosing( binaryImg, ker1 = 4, ker2 = 2 )
        #cv2.imwrite( directory + imgFileName.split(".")[0]+"_bi1.png", binaryImg )
        
        #print type(binaryImg)
        print binaryImg.dtype
        binaryImg = cv2.convertScaleAbs( binaryImg )
        contours, hierarchy= cv2.findContours( binaryImg, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        contours2 = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            #print area
            if area > 100:
                contours2.append(cnt)
                
        cv2.drawContours(img2, contours2, -1, (0,255,0), 2)
        cv2.imwrite( directory + imgFileName.split(".")[0]+"_cnt.png", img2 )
        
    except:
        print "--------------Error!!!------------------"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    
    if len(sys.argv) > 2:
        dataFromDirectory( sys.argv[1] )
    
    else:
        imgFileName = sys.argv[1]
        imgProcessingMain( imgFileName )
