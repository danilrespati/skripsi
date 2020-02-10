from time import sleep
import RPi.GPIO as GPIO
import numpy as np
from bs4 import BeautifulSoup
import urllib.request

def initUrl():
    url = 'http://192.168.100.13/skripsi/target.php'
    web = urllib.request.urlopen(url)
    html = web.read()
    soup = BeautifulSoup(html, 'lxml')
    stat = soup.find('em').text
    target = soup.find('td', {'id': 'target'}).text
    anglePan = soup.find('td', {'id': 'x'}).text
    angleTlt = soup.find('td', {'id': 'y'}).text
    return stat, target, int(anglePan), int(angleTlt)

def setServoAngle(servo, angle):
    if (angle >= -80 and dutyCycle <= 80):
        dutyCycle = round(((7*angle)+1350)/180, 1)
        pwm = GPIO.PWM(servo, 50)
        pwm.start(0)
        pwm.ChangeDutyCycle(dutyCycle)
        print("{0} -> {1}".format(angle, dutyCycle))
        sleep(0.5)
        pwm.stop()

testPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(testPin, GPIO.OUT)
stat, target, anglePan, angleTlt = initUrl()
if stat=="Running":
    setServoAngle(testPin, anglePan)
    setServoAngle(testPin, 0)
    GPIO.cleanup()
