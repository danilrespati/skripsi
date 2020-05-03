from multiprocessing import Process, Manager, Value
import socket
import time
import signal
import sys
import cv2
import os
import numpy as np
import math

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
        msg = "The time is {0}".format(time.time())
        clientsocket, address = s.accept()
        print("Connection from {0} has been established!".format(address))
        clientsocket.send(bytes(msg, "utf-8"))

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



if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("192.168.0.120", 1234))
    s.listen(5)

    target = 'Danil'
    pos = {"x":0, "y":0}
    angle = {"pan":0, "tlt":0}
    faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
                                        '/data/classifier/lbpcascades'
                                        '/lbpcascade_frontalface.xml')
    cam = initCam()

    manager = Manager()
    data = manager.Value('i', 0)

    processServer = Process(target=server, args=(data, ))
    processMainproc = Process(target=mainproc)

    # start all processes
    processServer.start()
    processMainproc.start()

    # join all processes
    processServer.join()
    processMainproc.join()