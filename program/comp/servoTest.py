from time import sleep
import RPi.GPIO as GPIO
import numpy as np


testPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(testPin, GPIO.OUT)  # white => TILT

def setServoAngle(servo, dutyCycle):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(0)
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.4)
    pwm.stop()

if __name__ == '__main__':
    for dc in np.arange(5, 11, 0.5):
        print(dc)
        setServoAngle(testPin, dc)
    setServoAngle(testPin, 7.5)
    GPIO.cleanup()
