import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.120", 1234))

msg = s.recv(256)
print(pickle.loads(msg))