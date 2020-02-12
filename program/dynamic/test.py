import subprocess
servo = str(13)
angle = str(50)
subprocess.call(['/home/pi/skripsi/program/dynamic/angleServoCtrl.py', servo, angle])