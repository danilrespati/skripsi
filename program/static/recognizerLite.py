import cv2
import os
import numpy as np
import math

def initCam():
    global frameSize
    frameSize = [640, 360]
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
                bbox = (x, y, w, h)
                posX = int(bbox[0] + (bbox[2] / 2))
                posY = int(bbox[1] + (bbox[3] / 2))
                print("{0}, {1}, {2}\n".format(target, posX, posY))
                found = True
                break
        if found:
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
    ppm = 168 #Calibrate from calPos.py static
    ppc = ppm/100
    centerX = frameSize[0]//2
    centerY = frameSize[1]//2
    deltaX = (centerX - pos["x"])*(-1)
    deltaY = (centerY - pos["y"])*(1)
    dist = [deltaX//ppc, deltaY//ppc]
    dist[1] = dist[1] + 23 #camStatic and camDynamic diff height
    return dist

def distToAngle(dist):
    camDist = 200 #Calibrate from calPos.py dynamic
    pan = math.degrees(math.atan(dist[0]/camDist))
    tlt = math.degrees(math.atan(dist[1]/camDist))
    return round(pan,1), round(tlt,1)

def posToAngle(pos):
    dist = posToDist(pos)
    angle = distToAngle(dist)
    return angle[0], angle[1]

stat = 1
target = input('Target: ')
pos = {"x":0, "y":0}
angle = {"pan":0, "tlt":0}
sendAngle(stat, target, pos, angle)
faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
                                    '/data/classifier/lbpcascades'
                                    '/lbpcascade_frontalface.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/skripsi/data/trainer/static/trainer.yml')
#based from dataset taken
subjects = ['Label start from 1', 'Danil', 'Yoga', 'Dede', 'Guntur', 'Rizal']

cam = initCam()

while stat:
    pos["x"], pos["y"] = searchTarget()
    angle["pan"], angle["tlt"] = posToAngle(pos)
    sendAngle(stat, target, pos, angle)

print("\n[INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
