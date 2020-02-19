import signal

def signal_handler(sig, frame):
    # print a status message
    print("[INFO] You pressed `ctrl + c`! Exiting...")

    # disable the servos
    print("bisa")

    # exit
    sys.exit()
    
def infiniteLoop():
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        print("loop")
    
if __name__ == "__main__":
    infiniteLoop()