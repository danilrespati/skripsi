from time import sleep
import RPi.GPIO as GPIO
import numpy as np
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

tilt = 11
pan = 13

GPIO.setup(tilt, GPIO.OUT)  # white => TILT
GPIO.setup(pan, GPIO.OUT)  # gray ==> PAN

def setServoAngle(servo, dutyCycle):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.4)
    pwm.stop()

if __name__ == '__main__':
    for dc in np.arange(5, 11, 0.5):
        print(dc)
        setServoAngle(pan, dc)
        setServoAngle(tilt, dc)
        sleep(0.5)
    setServoAngle(pan, 8)
    setServoAngle(tilt, 7)
    GPIO.cleanup()
