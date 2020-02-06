"""
Program flow:
START
Move servo(initial position)
Face detection
Face recognition
Setup tracker
Check offset
Move servo(offset based)
If tracker lost: move to line 4
If ESC pressed: break
STOP
"""

from bs4 import BeautifulSoup
import urllib.request
import cv2
import os
import numpy as np
import time

def drawRectangle(frame, bbox):
    (x, y, w, h) = bbox
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

def drawText(frame, text, x, y):
    cv2.putText(frame, text, (x, y), 
                cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def timer(*con):
    global startTime
    if(con[0] == "start"):
        startTime = time.time()
    if(con[0] =="stop"):
        print("--- {0} executed in {1} seconds ---\n".format(con[1], (time.time() - startTime)))

def initCam():
    global frameWidth
    global frameHeight
    frameWidth = 640
    frameHeight = 480
    brightness = 0.6
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, brightness)
    return cap

def initUrl():
    url = 'http://192.168.100.13/skripsi/target.php'
    web = urllib.request.urlopen(url)
    html = web.read()
    soup = BeautifulSoup(html, 'lxml')
    target = soup.find('td', {'id': 'target'}).text
    anglePan = soup.find('td', {'id': 'x'}).text
    angleTilt = soup.find('td', {'id': 'y'}).text
    return target, anglePan, angleTilt

def moveServo(servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

def searchTarget():
    i = 0
    bbox = None
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, -1)
        vid.write(frame)
        cv2.imshow('frame', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            label, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if (subjects[label] == target):
                cv2.imshow('Target', frame[y:y+h, x:x+w])
                bbox = (x, y, w, h)
                break
        i += 1
        print("Cycle {0}, not detected\n".format(i))
        if(i == 10):
            print("Re-cycle\n")
            break
    return bbox

def trackTarget(bbox):
    if(bbox != None):
        ret, frame = cam.read()
        frame = cv2.flip(frame, -1)
        tracked = tracker.init(frame, bbox)
        while tracked:
            ret, frame = cam.read()
            frame = cv2.flip(frame, -1)
            tracked, bbox = tracker.update(frame)
            vid.write(frame)
            cv2.imshow('frame', frame)
            offsetCheck(bbox, angle, servo)

def offsetCheck(bbox, ang, servo):
    global angle
    x = int(bbox[0] + (bbox[2] / 2))
    y = int(bbox[1] + (bbox[3] / 2))
    centerBox = {
    "xMax":250,
    "yMax":150,
    "xMin":150,
    "yMin":100
    }
    servoRange = {
    "panMax":150,
    "tiltMax":140,
    "panMin":30,
    "tiltMin":40
    }
    inc = {
    "pan":5,
    "tilt":10
    }
    if (x > centerBox["xMax"]):
        if int(angle["pan"]) <= servoRange["panMin"]:
            int(angle["pan"]) = servoRange["panMin"]
        else :
            int(angle["pan"]) -= inc["pan"]
            moveServo(servo["pan"], int(angle["pan"]))
    if (y > centerBox["yMax"]):
        if int(angle["tilt"]) <= servoRange["tiltMin"]:
            int(angle["tilt"]) = servoRange["tiltMin"]
        else :
            int(angle["tilt"]) -= inc["tilt"]
            moveServo(servo["tilt"], int(angle["tilt"]))
    if (x < centerBox["xMin"]):
        if int(angle["pan"]) >= servoRange["panMax"]:
            int(angle["pan"]) = servoRange["panMax"]
        else :
            int(angle["pan"]) += inc["pan"]
            moveServo(servo["pan"], int(angle["pan"]))
    if (y < centerBox["yMin"]):
        if int(angle["tilt"]) >= servoRange["tiltMax"]:
            int(angle["tilt"]) = servoRange["tiltMax"]
        else :
            int(angle["tilt"]) += inc["tilt"]
            moveServo(servo["tilt"], int(angle["tilt"]))

servo = {"pan":13, "tilt":11}
angle = {"pan":90, "tilt":90}

faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
                                    '/data/classifier/lbpcascades'
                                    '/lbpcascade_frontalface.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/skripsi/data/trainer/dynamic/trainer.yml')
subjects = ['Label start from 1', 'Danil', 'Ayu', 'Yoga', 'Toni']
cam = initCam()
rec = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frameWidth, frameHeight))
while True:
    tracker = cv2.TrackerKCF_create()
    target, angle["pan"], angle["tilt"] = initUrl()
    moveServo(servo["pan"], angle["pan"])
    moveServo(servo["tilt"], angle["tilt"])
    bbox = searchTarget()
    trackTarget(bbox)

cv2.destroyAllWindows()
vid.release()
cam.release()
