import multiprocessing
import socket
import time
import signal
import sys

def signal_handler(sig, frame):
    # print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")

    # exit
    sys.exit()

def server(waktu):
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        msg = "The time is {0}".format(time.time())
        clientsocket, address = s.accept()
        print("Connection from {0} has been established!".format(address))
        clientsocket.send(bytes(msg, "utf-8"))

def mainproc():
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        waktu.value = time.time()



if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("192.168.0.120", 1234))
    s.listen(5)

    manager = Manager()
    waktu = manager.Value('i', 0)

    processServer = Process(target=server, args=(waktu,))
    processMainproc = Process(target=mainproc)

    # start all processes
    processServer.start()
    processMainproc.start()

    # join all processes
    processServer.join()
    processMainproc.join()