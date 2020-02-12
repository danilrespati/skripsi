import cv2
import os
import numpy as np
import time

def moveServo(servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

moveServo(13, 50)