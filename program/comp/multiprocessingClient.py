import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.120", 1234))

for i in range(5):
    msg = s.recv(1024)
    print(msg.decode("utf-8"))