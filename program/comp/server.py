import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("192.168.0.120", 1234))
s.listen(5)

while True:
    data = {"trg": "Danil", "pan": 10.5, "tme": time.time()}
    msg = pickle.dumps(data)
    clientsocket, address = s.accept()
    print("Connection from {0} has been established!".format(address))
    clientsocket.send(msg)