from multiprocessing import Process, Manager, Value
import socket
import time
import pickle
import sys

start = time.time()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.120", 1234))

msg = s.recv(512)
print(sys.getsizeof(pickle.loads(msg)))
print(pickle.loads(msg))
print(msg)
finish = time.time()
print(finish-start)