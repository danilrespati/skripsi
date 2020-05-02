from bs4 import BeautifulSoup
import urllib.request
import cv2
import os
import numpy as np
import time

def initUrl():
    url = 'http://192.168.0.120/skripsi/target.php'
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

stat, target, angle["pan"], angle["tlt"] = initUrl()
print(stat)
while stat == "Running":
    stat, target, angle["pan"], angle["tlt"] = initUrl()
    if (abs(currAngle["pan"]-angle["pan"]) >= 0.3):
        moveServo(servo["pan"], angle["pan"])
        currAngle["pan"] = angle["pan"]
    if (abs(currAngle["tlt"]-angle["tlt"]) >= 0.3):
        moveServo(servo["tlt"], angle["tlt"])
        currAngle["tlt"] = angle["tlt"]

moveServo(servo["pan"], 0)
moveServo(servo["tlt"], 0)