import cv2
import os
import numpy as np

def initCam():
    global frameSize
    frameSize = [640, 360]
    brightness = 0.6
    cap = cv2.VideoCapture(0)
    cap.set(3, frameSize[0])
    cap.set(4, frameSize[1])
    cap.set(10, brightness)
    return cap

cam = initCam()
flag = 0

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, -1)
    if(flag==0):
        roi = cv2.selectROI(frame)
        flag = 1
        cv2.imwrite("/home/pi/skripsi/data/calibration.jpg", frame[roi[1]:roi[1]+roi[3],roi[0]:roi[0]+roi[2]])
    cv2.imshow('Preview',frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        flag = 0
    if key == 27:
        break

cv2.destroyAllWindows()
cam.release()
