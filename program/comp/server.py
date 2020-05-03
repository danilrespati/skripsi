import socket

s = socket.socket(socket.AF_INET, socket)
s.bind("192.168.0.120", 1234)
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsocket.send(bytes("Welcome to the server!", "utf-8"))