import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for i in range(5):
    s.connect(("192.168.0.120", 1234))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
    time.sleep(1)