from multiprocessing import Process, Manager, Value
import socket
import time

def server(msg):
    while True:
        msg = "The time is {0}".format(time.time())
        clientsocket, address = s.accept()
        print("Connection from {0} has been established!".format(address))
        clientsocket.send(bytes(msg, "utf-8"))

def mainproc():
    waktu.value = time.time()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("192.168.0.120", 1234))
    s.listen(5)

    waktu = manager.value('i', 0)

    processServer = Process(target=server,
        args=(waktu))
    processMainproc = Process(target=mainproc)

    # start all processes
    processServer.start()
    processMainproc.start()

    # join all processes
    processServer.join()
    processMainproc.join()