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

def server(data):
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        msg = dict()
        msg[1] = data["target"]
        msg[2] = data["pan"]
        msg[3] = data["tlt"]
        msg = pickle.dumps(msg)
        clientsocket, address = s.accept()
        print("Connection from {0} has been established!".format(address))
        clientsocket.send(msg)

def mainproc():
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        found = False
        ret, frame = cam.read()
        frame = cv2.flip(frame, -1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            bbox = (x, y, w, h)
            posX = int(bbox[0] + (bbox[2] / 2))
            posY = int(bbox[1] + (bbox[3] / 2))
            print("{0}, {1}, {2}\n".format(target, posX, posY))
            found = True
        if found:
            data.value = time.time()

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

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("192.168.0.120", 1234))
    s.listen(5)

    manager = Manager()
    data = manager.dict()

    target = input('Target: ')
    data["target"] = target
    pos = {"x":0, "y":0}
    angle = {"pan":0, "tlt":0}
    data["pan"] = angle["pan"]
    data["tlt"] = angle["tlt"]
    faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
                                        '/data/classifier/lbpcascades'
                                        '/lbpcascade_frontalface.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('/home/pi/skripsi/data/trainer/static/trainer.yml')
    subjects = ['Label start from 1', 'Danil', 'Yoga', 'Dede', 'Guntur', 'Rizal']
    cam = initCam()

    processServer = Process(target=server, args=(data, ))
    processMainproc = Process(target=mainproc)

    # start all processes
    processServer.start()
    processMainproc.start()

    # join all processes
    processServer.join()
    processMainproc.join()