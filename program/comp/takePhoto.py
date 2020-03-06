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

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, -1)
    if(flag==0):
        roi = cv2.selectROI(frame)
        flag = 1
        cv2.imwrite("/home/pi/skripsi/data/user/static/User." + str(label) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
    cv2.imshow('Preview',frame)
    if key == ord('q'):
        flag = 0
    if key == 27:
        print(distance)
        print(ppm)
        break

cv2.destroyAllWindows()
cap.release()
