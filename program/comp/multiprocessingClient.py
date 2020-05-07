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
        time.sleep(0.3)
        pwm.stop()
    else:
        print("Limit: -90 <= angle <= 90")
    GPIO.cleanup()

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