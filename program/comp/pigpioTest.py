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
import pigpio

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
    pi.set_servo_pulsewidth(27, 1500)
    time.sleep(0.2)
    pi.set_servo_pulsewidth(17, 1500)
    time.sleep(0.2)
    pi.stop()
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

def setServos(data):
    signal.signal(signal.SIGINT, signal_handler)
    servo = {"pan":27, "tlt":17}
    angle = [data["pan"], data["tlt"]]
    pulse = [element * (100/9) + 1500 for element in angle]
    pi.set_servo_pulsewidth(servo["pan"], 1500)
    time.sleep(0.2)
    pi.set_servo_pulsewidth(servo["tlt"], 1500)
    time.sleep(1)
    while True:
        angle = [data["pan"], data["tlt"]]
        pulse = [element * (100/9) + 1500 for element in angle]
        pi.set_servo_pulsewidth(servo["pan"], pulse[0])
        time.sleep(0.2)
        pi.set_servo_pulsewidth(servo["tlt"], pulse[1])
        time.sleep(0.2)

def mainproc():
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, -1)
        cv2.putText(frame, data["target"], (100, 100), 
            cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
        time.sleep(0.02)
        rec.write(frame)

if __name__ == "__main__":
    manager = Manager()
    data = manager.dict()

    data["target"] = "null"
    data["pan"] = 0
    data["tlt"] = 0

    pi = pigpio.pi()
    cam = initCam()
    if os.path.exists("/home/pi/skripsi/data/video/dynamic/angleParser.avi"):
        os.remove("/home/pi/skripsi/data/video/dynamic/angleParser.avi")
    rec = cv2.VideoWriter('/home/pi/skripsi/data/video/dynamic/angleParser.avi', cv2.VideoWriter_fourcc(
        'M', 'J', 'P', 'G'), 20, (frameSize[0], frameSize[1]))

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