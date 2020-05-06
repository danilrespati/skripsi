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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.120", 1234))

msg = s.recv(512)
print(msg)