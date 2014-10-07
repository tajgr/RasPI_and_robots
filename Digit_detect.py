# -*- coding: utf-8 -*-
import sys
import numpy as np
import cv2

class Digit_detect:
    def __init__(self, path, roi_size):
        self.path = path
        self.roisize = roi_size
        self.max_h=0
        self.min_h=0
        self.min_w=0
        self.keys=[ i for i in range(48,58)]
        self.keys.append(32)
        self.keys.append(97)
        self.samples =  np.empty((0,self.roisize*self.roisize))
        self.responses = []
        self.model = cv2.KNearest()

    def im_preprocess(self,image):
        size=image.shape
        self.max_h=size[0]/2.5
        self.min_h=size[0]/20
        self.min_w=size[1]/30
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(3,3),0)
        thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
        return thresh

    def process_learning(self,image,binary):
        contours,hierarchy = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt)>30:
                [x,y,w,h] = cv2.boundingRect(cnt)
                if (w>self.min_w) and (h>self.min_h) and (w<h) and (h<self.max_h):
                    if y<300:
                        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
                        roi = binary[y:y+h,x:x+w]
                        roismall = cv2.resize(roi,(self.roisize,self.roisize))
                        cv2.imshow('norm',image)
                        cv2.imshow('small',image[y:y+h,x:x+w])
                        key = cv2.waitKey(0)
                        if key == 27:  # (escape to skip rest of image)
                            break
                        elif key in self.keys:
                            if key == 32:
                                self.responses.append(20)
                            elif key == 97:
                                self.responses.append(10)
                            else:
                                self.responses.append(int(chr(key)))
                            sample = roismall.reshape((1,self.roisize*self.roisize))
                            self.samples = np.append(self.samples,sample,0)
    
    def learn_from_pic(self, path_to_files, clear_all, to_save, to_train):
        # do you want to start from zero?
            # True: clear all
            # False -> just continue
        if(clear_all):
            self.samples =  np.empty((0,self.roisize*self.roisize))
            self.responses = []
            self.model = 0
            self.model = cv2.KNearest()
        # make samples and responses
        cv2.namedWindow('norm',cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow('small',cv2.WINDOW_AUTOSIZE)
        for img_path in path_to_files:
            imag = cv2.imread(img_path)
            binary = self.im_preprocess(imag)
            self.process_learning(imag,binary)
        cv2.destroyWindow('norm')
        cv2.destroyWindow('small')
        # ask for saving data
            # True -> save data
            # False -> nothing happens
        if(to_save):
            path_1 = self.path + 'samples.data'
            path_2 = self.path + 'responses.data'
            self.save_learned(path_1,path_2)
        # ask to train model on current datas
            # Y -> self.model.train(self.samples,self.responses)
            # N -> program ends
        if(to_train):
            responses = np.array(self.responses,np.float32)
            responses = responses.reshape((responses.size,1))
            samples = np.array(self.samples,np.float32)
            self.model.train(samples,responses)


    def save_learned(self,path_samples,path_responses):
        responses = np.array(self.responses,np.float32)
        responses = responses.reshape((responses.size,1))
        np.savetxt(path_samples,self.samples)
        np.savetxt(path_responses,responses)
        
            
    def learn_from_file(self,path_to_samples,path_to_responses):
        samples = np.loadtxt(path_to_samples,np.float32)
        responses = np.loadtxt(path_to_responses,np.float32)
        responses = responses.reshape((responses.size,1))
        self.model.train(samples,responses)

    def selection(self,points):
        points = sorted(points)
        detected = []
        ret = []
        for num in points:
            if num[0] not in detected:
                detected.append(num[0])
                ret.append(num)
        return ret

    def detect(self,binary):
        contours,hierarchy = cv2.findContours(binary,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        point=[]
        size = binary.shape
        for cnt in contours:
            if cv2.contourArea(cnt)>50:
                [x,y,w,h] = cv2.boundingRect(cnt)
        
                if (w>self.min_w) and (h>self.min_h) and (w<h) and (h<self.max_h):
                    if y<300:
                        roi = binary[y:y+h,x:x+w]
                        roismall = cv2.resize(roi,(self.roisize,self.roisize))
                        roismall = roismall.reshape((1,self.roisize*self.roisize))                                            
                        roismall = np.float32(roismall)
                        retval, results, neigh_resp, dists = self.model.find_nearest(roismall, k=1)
                        if int((results[0][0]))<11:# and dists<200000
                            point.append([int(retval),int((dists)),(x+w/2)/float(size[0]),(y+h/2)/float(size[1])])
        best = self.selection(point)
        return best
        
    def detect_digits_from_file(self,path_to_image):
        digits = []
        image = cv2.imread(path_to_image)
        binary = self.im_preprocess(image)
        digits = self.detect(binary)
        return digits


    def detect_digits(self,cv_image):
        digits = []
        binary = self.im_preprocess(cv_image)
        digits = self.detect(binary)
        return digits
        
    
if __name__ == "__main__": 
    A=Digit_detect('',20)
    A.learn_from_file('samples.data','responses.data')
    print A.detect_digits_from_file('SICK_ROBOT/004.jpg')