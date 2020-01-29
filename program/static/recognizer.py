import cv2
import os
import numpy as np
import math

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
    frameWidth = 1280
    frameHeight = 720
    brightness = 0.6
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, brightness)
    return cap

def searchTarget():
    i = 0
    bbox = None
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, -1)
        rec.write(frame)
        cv2.imshow('frame', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            label, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if (subjects[label] == target):
                cv2.imshow('Target', frame[y:y+h, x:x+w])
                bbox = (x, y, w, h)
                x = int(bbox[0] + (bbox[2] / 2))
                y = int(bbox[1] + (bbox[3] / 2))
                break
        i += 1
        print("Cycle {0}, not detected\n".format(i))
        if(i == 10):
            print("Re-cycle\n")
            x = None
            y = None
            break
    return x, y

def sendAngle(stat, target, pos, angle):
    path = "/var/www/html/skripsi"
    os.chdir(path)
    message = """
		<?php
        $stat = {a};
        $target = '{b}';
        $x = {c};
        $y = {d};
        $pan = {e};
        $tilt = {f};""".format(a=stat, b=str(target), c=pos["x"], d=pos["y"], e=angle["pan"], f=angle["tilt"]) + """
		?>
		"""
    f = open('var.php', 'w')
    f.write(message)
    f.close()

def posToAngle(pos):
    pan = pos["x"]
    tilt = pos["y"]
    return pan, tilt

stat = 1
pos = {"x":0, "y":0}
angle = {"pan":0, "tilt":0}

faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
                                    '/data/classifier/lbpcascades'
                                    '/lbpcascade_frontalface.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/skripsi/data/trainer/static/trainer.yml')
subjects = ['Label start from 1', 'Danil', 'Ayu', 'Yoga', 'Toni']
cam = initCam()
rec = cv2.VideoWriter('/home/skripsi/data/video/static/video.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frameWidth, frameHeight))
target = input('Target: ')
print('(ESC) Exit\n(c) Change target')

while stat:
    pos["x"], pos["y"] = searchTarget()
    angle["pan"], angle["tilt"] = posToAngle(pos)
    sendAngle(stat, target, pos, angle)
    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == ord('c'):
        target = input('New target: ')
        print('\nTarget: {0}'.format(target))
        print('(ESC) Exit\n(c) Change target')
    if k == 27:
        sendAngle(stat, target, pos, angle)
        stat = 0

# Do a bit of cleanup
print("\n[INFO] Exiting Program and cleanup stuff")
cam.release()
rec.release()
cv2.destroyAllWindows()
