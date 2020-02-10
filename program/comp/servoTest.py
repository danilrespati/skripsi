from time import sleep
import RPi.GPIO as GPIO
import numpy as np

testPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(testPin, GPIO.OUT)

def setServoAngle(servo, angle):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(0)
    dutyCycle = round(((7*angle)+1350)/180, 1)
    pwm.ChangeDutyCycle(dutyCycle)
    print("{0} -> {1}".format(angle, dutyCycle))
    sleep(0.5)
    pwm.stop()

if __name__ == '__main__':
    for angle in np.arange(-90, 190, 10):
        setServoAngle(testPin, angle)
    setServoAngle(testPin, 0)
    GPIO.cleanup()
