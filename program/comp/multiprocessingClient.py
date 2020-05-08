from multiprocessing import Process, Manager, Value
import RPi.GPIO as GPIO
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
    moveServo(13, 0)
    moveServo(11, 0)
    rec.release()
    cam.release()
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
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(servo, GPIO.OUT)
    if (-90 <= angle <= 90):
        pwm = GPIO.PWM(servo, 50)
        pwm.start(8)
        #dutyCycle = ((7*angle)+1350)/180
        #dutyCycle = angle / 18. + 3.
        #dutyCycle = angle / 10
        dutyCycle = ((angle*-1)+126) / 18
        pwm.ChangeDutyCycle(dutyCycle)
        time.sleep(2)
        pwm.stop()
    else:
        print("Limit: -90 <= angle <= 90")
    GPIO.cleanup()

def setServos(data):
    signal.signal(signal.SIGINT, signal_handler)
    servo = {"pan":13, "tlt":11}
    lastPan = 0
    lastTlt = 0
    moveServo(servo["pan"], 0)
    moveServo(servo["tlt"], 0)
    while True:
        if(abs(data["pan"] - lastPan) >= 0.5):
            moveServo(servo["pan"], data["pan"])
            lastPan = data["pan"]
        if(abs(data["tlt"] - lastTlt) >= 0.5):
            moveServo(servo["tlt"], data["tlt"])
            lastTlt = data["tlt"]

def mainproc():
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, -1)
        cv2.putText(frame, data["target"], (100, 100), 
            cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
        rec.write(frame)
        time.sleep(0.1)

if __name__ == "__main__":
    manager = Manager()
    data = manager.dict()

    data["target"] = "null"
    data["pan"] = 0
    data["tlt"] = 0

    cam = initCam()
    if os.path.exists("/home/pi/skripsi/data/video/dynamic/angleParser.avi"):
        os.remove("/home/pi/skripsi/data/video/dynamic/angleParser.avi")
    rec = cv2.VideoWriter('/home/pi/skripsi/data/video/dynamic/angleParser.avi', cv2.VideoWriter_fourcc(
        'M', 'J', 'P', 'G'), 30, (frameSize[0], frameSize[1]))

    processClient = Process(target=client)
    processSetServos = Process(target=setServos, args=(data, ))
    processMainproc = Process(target=mainproc)

    # start all processes
    processClient.start()
    processSetServos.start()
    processMainproc.start()

    # join all processes
    processClient.join()
    processSetServos.join()
    processMainproc.join()