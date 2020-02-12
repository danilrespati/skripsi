import subprocess
servo = str(13)
angle = str(50)
subprocess.run(['angleServoCtrl.py', servo, angle])
# /home/pi/skripsi/program/dynamic/