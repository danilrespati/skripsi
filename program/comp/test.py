import os
import time
import signal
import sys

def signal_handler(sig, frame):
    # print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")

    # exit
    sys.exit()
    
def infiniteLoop():
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        print("loop")
        time.sleep(0.1)
    
if __name__ == "__main__":
    infiniteLoop()
