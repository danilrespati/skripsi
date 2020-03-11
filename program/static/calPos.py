from imutils import paths
import imutils
import cv2
import os
import numpy as np

def initCam():
	global frameWidth
	global frameHeight
	frameWidth = 640
	frameHeight = 360
	brightness = 0.6
	cam = cv2.VideoCapture(0)
	cam.set(3, frameWidth)
	cam.set(4, frameHeight)
	cam.set(10, brightness)
	return cam

def findMarker(frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(blur, 35, 125)
	cnts = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key = cv2.contourArea)
	return cv2.minAreaRect(c)
	
def distanceToCamera(knownHeight, focalLength, perHeight):
	return (knownHeight * focalLength) / perHeight
	
def pixelPerMetric(height, perKnownHeight):
	return (height / perKnownHeight)

cam = initCam()
flag = 0
line = 0

image = cv2.imread("/home/pi/skripsi/data/cal2mstatic640x360.jpg")
cv2.imshow('Preview',image)
knownDistance = 200
knownHeight = 0.5
marker = findMarker(image)
focalLength = (marker[1][1] * knownDistance) / knownHeight

while True:
	ret, frame = cam.read()
	frame = cv2.flip(frame, -1)
	if line:
		cv2.line(frame, (int(frameWidth/2),0), (int(frameWidth/2),frameHeight), (0,0,255), 4)
	while(flag==0):
		roi = cv2.selectROI(frame)
		flag = 1
	frame = frame[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
	marker = findMarker(frame)
	distance = distanceToCamera(knownHeight, focalLength, marker[1][1])
	ppm = pixelPerMetric(marker[1][1], knownHeight)
	box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
	box = np.int0(box)
	cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
	cv2.putText(frame, "{0} {1}".format(round(distance,2), round(ppm,2)),
		(0,10), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 0, 0), 1)
	cv2.imshow('Preview',frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		flag = 0
	if key == ord('l'):
		line = 1 if line == 0 else 0
	if key == 27:
		print(distance)
		print(ppm)
		break
		
print("\n [INFO] Exiting Program and cleanup stuff")
cv2.destroyAllWindows()
cam.release()
