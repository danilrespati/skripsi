import subprocess
import os
servo = str(13)
angle = str(50)
subprocess.run(['/home/pi/skripsi/program/dynamic/angleServoCtrl.py', servo, angle])
