import socket
import time

for i in range(5):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.0.120", 1234))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
    time.sleep(1)