"""
Start recording v
Parsing v
Initial position
Finding v
Tracking v
Following
End recording v
"""

from bs4 import BeautifulSoup
import urllib.request
import cv2
import os
import numpy as np
import RPi.GPIO as GPIO

def initUrl():
    url = 'http://192.168.100.13/skripsi/target.php'
    web = urllib.request.urlopen(url)
    html = web.read()
    soup = BeautifulSoup(html, 'lxml')
    return soup
    
def initCam():
    cap = cv2.VideoCapture(0)
    frameWidth = 640
    frameHeight = 480
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, 0.6)
    return cap
    
def positionServo (servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

def mapServoPosition (x, y):
	global panAngle
	global tiltAngle
	if (x < 150):
		if panAngle >= 150:
			panAngle = 150
		else :
			panAngle += 5
			positionServo (panServo, panAngle)
	if (x > 250):
		if panAngle <= 30:
			panAngle = 30
		else :
			panAngle -= 5
			positionServo (panServo, panAngle)
	if (y < 100):
		if tiltAngle >= 140:
			tiltAngle = 140
		else :
			tiltAngle -= 10
			positionServo (tiltServo, tiltAngle)
	if (y > 150):
		if tiltAngle <= 40:
			tiltAngle = 40
		else :
			tiltAngle += 10
			positionServo (tiltServo, tiltAngle)


faceCascade = cv2.CascadeClassifier('/home/pi/Skripsi/repository'
                                    '/data/classifier/haarcascades'
                                    '/haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/Skripsi/repository/data/trainer/trainer.yml')

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
panServo = 13
tiltServo = 11
panAngle = 90
tiltAngle = 70
positionServo (panServo, panAngle)
positionServo (tiltServo, tiltAngle)
id = 0
names = ['None', 'Danil', 'Ayu', 'Yoga', 'Toni',
         'Azi', 'Joko', 'Tingkir', 'Bawa', 'Taufiq']
	 
cam = initCam()
soup = initUrl()
stat = 1  # kalo udah fix bisa diganti pake stat hasil parser

#vid = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(
#    'M', 'J', 'P', 'G'), 10, (frameWidth, frameHeight))
frameCount = 0
while stat:
    soup = initUrl()
    stat = 1  # kalo udah fix bisa diganti pake stat hasil parser
    target = soup.find('td', {'id': 'target'}).text
    posX = soup.find('td', {'id': 'x'}).text
    posY = soup.find('td', {'id': 'y'}).text
    sX = soup.find('td', {'id': 'sx'}).text
    print(stat, target, posX, posY, sX, ' Parsed')
    finding = 1
    tracking = 0
    while finding:
        tracker = cv2.TrackerKCF_create()
        ret, frame = cam.read()
        frameCount = frameCount + 1
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5)

        for(x, y, w, h) in faces:
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if (confidence < 100 and names[id] == target):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                found = frame[y:y+h, x:x+w]
                bbox = (x, y, w, h)
                tracked = tracker.init(frame, bbox)
                # print(tracked)
                finding = 0
                tracking = 1
                cv2.imshow('face', found)

        cv2.imshow('frame', frame)
        #vid.write(frame)
        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            stat = 0
            finding = 0
            tracking = 0
            cv2.destroyAllWindows()
        elif k == ord('x'):
            finding = 0
            tracking = 1
        elif (frameCount % 10) == 0:
            finding = 0

    while tracking:
        ret, frame = cam.read()
        frameCount = frameCount + 1
        frame = cv2.flip(frame, -1)
        tracked, bbox = tracker.update(frame)
        # print(tracked)
        if tracked:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            cx = int(bbox[0] + (bbox[2] / 2))
            cy = int(bbox[1] + (bbox[3] / 2))
            mapServoPosition(cx, cy)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            finding = 1
            tracking = 0
        cv2.imshow('frame', frame)
        #vid.write(frame)
        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            stat = 0
            finding = 0
            tracking = 0
            cv2.destroyAllWindows()
        elif k == ord('x'):
            finding = 1
            tracking = 0

# Do a bit of cleanup
print("Total frame count: {0}".format(frameCount))
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
#vid.release()
