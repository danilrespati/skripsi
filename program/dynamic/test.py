import subprocess
import os
servo = str(13)
angle = str(50)
subprocess.call(['./angleServoCtrl.py', servo, angle])
