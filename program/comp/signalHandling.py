import os
import time
import signal
import sys

def signalHandler(sig, frame):
    # print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")

    # exit
    sys.exit()
    
def infiniteLoop():
    signal.signal(signal.SIGINT, signalHandler)
    while True:
        print("loop")
        time.sleep(0.1)
    
if __name__ == "__main__":
    infiniteLoop()
