from time import sleep
import RPi.GPIO as GPIO
import numpy as np

def initUrl():
    url = 'http://192.168.100.13/skripsi/target.php'
    web = urllib.request.urlopen(url)
    html = web.read()
    soup = BeautifulSoup(html, 'lxml')
    target = soup.find('td', {'id': 'target'}).text
    anglePan = soup.find('td', {'id': 'x'}).text
    angleTlt = soup.find('td', {'id': 'y'}).text
    return target, anglePan, angleTlt

def setServoAngle(servo, angle):
    dutyCycle = round(((7*angle)+1350)/180, 1)
    if (dutyCycle >= 4.5 and dutyCycle <= 10.5):
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

if __name__ == '__main__':
    for angle in np.arange(-90, 190, 10):
        setServoAngle(testPin, angle)
    setServoAngle(testPin, 0)
    GPIO.cleanup()
