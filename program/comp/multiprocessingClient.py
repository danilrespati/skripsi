from multiprocessing import Process, Manager, Value
import socket
import time
import signal
import sys
import cv2
import os
import numpy as np
import math
import pickle

def initCam():
    global frameSize
    frameSize = [640, 360]
    brightness = 0.6
    cap = cv2.VideoCapture(0)
    cap.set(3, frameSize[0])
    cap.set(4, frameSize[1])
    cap.set(10, brightness)
    return cap

def signal_handler(sig, frame):
    # print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")

    # exit
    cam.release()
    cv2.destroyAllWindows()
    sys.exit()

def client():
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.0.120", 1234))
        msg = s.recv(512)
        msg = pickle.loads(msg)
        data["target"] = msg["target"]
        data["pan"] = msg["pan"]
        data["tlt"] = msg["tlt"]
        time.sleep(0.2)

def moveServo(servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

def setServos(data):
    signal.signal(signal.SIGINT, signal_handler)
    servo = {"pan":13, "tlt":11}
    while True:
        print(data)
        moveServo(servo["pan"], data["pan"])
        moveServo(servo["tlt"], data["tlt"])
        time.sleep(0.2)

if __name__ == "__main__":
    manager = Manager()
    data = manager.dict()

    data["target"] = "null"
    data["pan"] = 0
    data["tlt"] = 0

    cam = initCam()

    processClient = Process(target=client)
    processSetServos = Process(target=setServos, args=(data, ))

    # start all processes
    processClient.start()
    processSetServos.start()

    # join all processes
    processClient.join()
    processSetServos.join()