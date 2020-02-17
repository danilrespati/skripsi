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

def initCam():
    global frameSize
    frameSize = [1280, 720]
    brightness = 0.6
    cap = cv2.VideoCapture(0)
    cap.set(3, frameSize[0])
    cap.set(4, frameSize[1])
    cap.set(10, brightness)
    return cap

def searchTarget():
    while True:
        found = False
        ret, frame = cam.read()
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            label, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if (subjects[label] == target):
                cv2.imshow('Target', frame[y:y+h, x:x+w])
                bbox = (x, y, w, h)
                drawRectangle(frame, bbox)
                drawText(frame, subjects[label], x, y-5)
                posX = int(bbox[0] + (bbox[2] / 2))
                posY = int(bbox[1] + (bbox[3] / 2))
                found = True
                break
        cv2.imshow('frame', frame)
        rec.write(frame)
        if found:
            break

        k = cv2.waitKey(10) & 0xff 
        if k == 27:
            stat = 0
            posX = pos["x"]
            posY = pos["y"]
            break
    return posX, posY

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
        $tlt = {f};""".format(a=stat, b=str(target), c=pos["x"], d=pos["y"], e=angle["pan"], f=angle["tlt"]) + """
        ?>
        """
    f = open('var.php', 'w')
    f.write(message)
    f.close()

def posToDist(pos):
    ppm = 402 #Calibrate from calPos.py static
    ppc = ppm/100
    centerX = frameSize[0]//2
    centerY = frameSize[1]//2
    deltaX = (centerX - pos["x"])*(-1)
    deltaY = (centerY - pos["y"])*(1)
    dist = [deltaX//ppc, deltaY//ppc]
    return dist

def distToAngle(dist):
    camDist = 200 #Calibrate from calPos.py dynamic
    pan = math.degrees(math.atan(dist[0]/camDist))
    tlt = math.degrees(math.atan(dist[1]/camDist))
    return pan, tlt

def posToAngle(pos):
    dist = posToDist(pos)
    angle = distToAngle(dist)
    return angle[0], angle[1]

stat = 1
target = input('Target: ')
pos = {"x":0, "y":0}
angle = {"pan":0, "tlt":0}

faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
                                    '/data/classifier/lbpcascades'
                                    '/lbpcascade_frontalface.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/skripsi/data/trainer/static/trainer.yml')
subjects = ['Label start from 1', 'Danil', 'Yoga', 'kosong', 'kosong']

cam = initCam()
if os.path.exists("/home/pi/skripsi/data/video/static/recognizer.avi"):
    os.remove("/home/pi/skripsi/data/video/static/recognizer.avi")
rec = cv2.VideoWriter('/home/pi/skripsi/data/video/static/recognizer.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frameSize[0], frameSize[1]))

while stat:
    pos["x"], pos["y"] = searchTarget()
    angle["pan"], angle["tlt"] = posToAngle(pos)
    sendAngle(stat, target, pos, angle)
    
    k = cv2.waitKey(10) & 0xff  
    if k == 27:
        stat = 0
        sendAngle(stat, target, pos, angle)

print("\n[INFO] Exiting Program and cleanup stuff")
cam.release()
rec.release()
cv2.destroyAllWindows()
