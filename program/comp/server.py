import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.0.120", 1234))
s.listen(5)

while True:
    msg = "The time is {0}".format(time.time())
    clientsocket, address = s.accept()
    print("Connection from {0} has been established!".format(address))
    clientsocket.send(bytes(msg, "utf-8"))