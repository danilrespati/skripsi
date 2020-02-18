from bs4 import BeautifulSoup
import urllib.request
import cv2
import os
import numpy as np
import time

def initCam():
    global frameSize
    frameSize = [640, 480]
    brightness = 0.6
    cap = cv2.VideoCapture(0)
    cap.set(3, frameSize[0])
    cap.set(4, frameSize[1])
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
    return stat, target, float(pan), float(tlt)

def moveServo(servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

servo = {"pan":13, "tlt":11}
angle = {"pan":0, "tlt":0}
currAngle = {"pan":0, "tlt":0}
moveServo(servo["pan"], angle["pan"])
moveServo(servo["tlt"], angle["tlt"])

cam = initCam()
if os.path.exists("/home/pi/skripsi/data/video/dynamic/angleParser.avi"):
    os.remove("/home/pi/skripsi/data/video/dynamic/angleParser.avi")
rec = cv2.VideoWriter('/home/pi/skripsi/data/video/dynamic/angleParser.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (frameSize[0], frameSize[1]))
ret, frame = cam.read()
frame = cv2.flip(frame, -1)
cv2.imshow('frame', frame)
stat, target, angle["pan"], angle["tlt"] = initUrl()
print(stat)
while stat == "Running":
    ret, frame = cam.read()
    frame = cv2.flip(frame, -1)
    cv2.imshow('frame', frame)
    rec.write(frame)
    stat, target, angle["pan"], angle["tlt"] = initUrl()
    if (abs(currAngle["pan"]-angle["pan"]) >= 0.3):
        moveServo(servo["pan"], angle["pan"])
        currAngle["pan"] = angle["pan"]
    if (abs(currAngle["tlt"]-angle["tlt"]) >= 0.3):
        moveServo(servo["tlt"], angle["tlt"])
        currAngle["tlt"] = angle["tlt"]
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        stat = 0
        break

moveServo(servo["pan"], 0)
moveServo(servo["tlt"], 0)
cv2.destroyAllWindows()
rec.release()
cam.release()
