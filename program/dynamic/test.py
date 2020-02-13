from bs4 import BeautifulSoup
import urllib.request
import cv2
import os
import numpy as np
import time

def drawRectangle(frame, bbox):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

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
    stat = soup.find('em').text
    target = soup.find('td', {'id': 'target'}).text
    pan = soup.find('td', {'id': 'pan'}).text
    tlt = soup.find('td', {'id': 'tlt'}).text
    return stat, target, int(pan), int(tlt)

def moveServo(servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

def searchTarget():
    i = 0
    bbox = None
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, -1)
        cv2.imshow('frame', frame)
        rec.write(frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            label, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if(subjects[label] == target):
                cv2.imshow('Target', frame[y:y+h, x:x+w])
                bbox = (x, y, w, h)
                break
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                stat = 0
                break
        if(bbox != None):
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
            drawRectangle(frame, bbox)
            rec.write(frame)
            cv2.imshow('frame', frame)
            offsetCheck(bbox)
            tracked, bbox = tracker.update(frame)
            k = cv2.waitKey(10) & 0xff
            if k == 27:
                stat = 0
                break

def offsetCheck(bbox):
    global angle
    x = int(bbox[0] + (bbox[2] / 2))
    y = int(bbox[1] + (bbox[3] / 2))
    centerBox = {
        "xMin":250,
        "xMax":390,
        "yMin":100,
        "yMax":380
        }
    servoRange = {
        "panMin":-90,
        "panMax":90,
        "tltMin":-30,
        "tltMax":30
        }
    inc = {
        "pan":2,
        "tlt":2
        }
    if (x > centerBox["xMax"]):
        if angle["pan"] <= servoRange["panMin"]:
            angle["pan"] = servoRange["panMin"]
        else :
            angle["pan"] += inc["pan"]
            moveServo(servo["pan"], angle["pan"])
    if (y > centerBox["yMax"]):
        if angle["tlt"] <= servoRange["tltMin"]:
            angle["tlt"] = servoRange["tltMin"]
        else :
            angle["tlt"] += inc["tlt"]
            moveServo(servo["tlt"], angle["tlt"])
    if (x < centerBox["xMin"]):
        if angle["pan"] >= servoRange["panMax"]:
            angle["pan"] = servoRange["panMax"]
        else :
            angle["pan"] -= inc["pan"]
            moveServo(servo["pan"], angle["pan"])
    if (y < centerBox["yMin"]):
        if angle["tlt"] >= servoRange["tltMax"]:
            angle["tlt"] = servoRange["tltMax"]
        else :
            angle["tlt"] -= inc["tlt"]
            moveServo(servo["tlt"], angle["tlt"])

servo = {"pan":13, "tlt":11}
angle = {"pan":0, "tlt":0}
moveServo(servo["pan"], angle["pan"])
moveServo(servo["tlt"], angle["tlt"])

faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
                                    '/data/classifier/lbpcascades'
                                    '/lbpcascade_frontalface.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/skripsi/data/trainer/dynamic/trainer.yml')
subjects = ['Label start from 1', 'Danil', 'Ayu', 'Yoga', 'Toni']
cam = initCam()
rec = cv2.VideoWriter('/home/pi/skripsi/data/video/dynamic/movingTracker.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frameWidth, frameHeight))
ret, frame = cam.read()
frame = cv2.flip(frame, -1)
cv2.imshow('frame', frame)
stat, target, angle["pan"], angle["tlt"] = initUrl()
print(angle)
moveServo(servo["pan"], angle["pan"])
moveServo(servo["tlt"], angle["tlt"])
while stat == "Running":
    tracker = cv2.TrackerKCF_create()
    bbox = searchTarget()
    trackTarget(bbox)
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        stat = 0
        break

moveServo(servo["pan"], 0)
moveServo(servo["tlt"], 0)
cv2.destroyAllWindows()
rec.release()
cam.release()
