'''
Face detection and tracking with OpenCV
    ==> Real Time tracking with Pan-Tilt servos 
    Based on original tracking object code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2016/05/09/opencv-rpi-gpio-and-gpio-zero-on-the-raspberry-pi/
Developed by Marcelo Rovai - MJRoBot.org @ 9Feb2018 
'''

# import the necessary packages
from bs4 import BeautifulSoup
import urllib.request
import cv2
import os
import numpy as np
import RPi.GPIO as GPIO

# define Servos GPIOs
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
tiltServo = 11
panServo = 13

def drawRectangle(frame, bbox):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

def drawText(frame, text, x, y):
    cv2.putText(frame, text, (x, y), 
                cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def initCam():
	frameWidth = 640
	frameHeight = 480
	brightness = 0.6
	cam = cv2.VideoCapture(0)
	cam.set(3, frameWidth)
	cam.set(4, frameHeight)
	cam.set(10, brightness)
	return cam
	
def detectFace(frame):
	"""
	Face detection
	"""
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, 1.3, 3, 0)
	return faces

# faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
# 		'/data/classifier/lbpcascades'
# 		'/lbpcascade_frontalface.xml')

# faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
# 		'/data/classifier/lbpcascades'
# 		'/lbpcascade_frontalface_improved.xml')

faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
		'/data/classifier/haarcascades'
		'/haarcascade_frontalface_default.xml')

cam = initCam()
if os.path.exists("/home/pi/skripsi/data/video/static/detector.avi"):
    os.remove("/home/pi/skripsi/data/video/static/detector.avi")
rec = cv2.VideoWriter('/home/pi/skripsi/data/video/static/detector.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frameWidth, frameHeight))
stat = 1

while stat:
	ret, frame = cam.read()
	frame = cv2.flip(frame, -1)
	faces = detectFace(frame)
	for (x,y,w,h) in faces:
		drawRectangle(frame, bbox=(x,y,w,h))
		drawText(frame, "Position: {0}, {1}".format(x,y), 10, 10)
		x = x+(w/2)
		y = y+(h/2)
	cv2.imshow('Preview',frame)
	key = cv2.waitKey(1) & 0xFF
	if key == 27:
		stat = 0
    rec.write(frame)
		
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
rec.release()
cv2.destroyAllWindows()
