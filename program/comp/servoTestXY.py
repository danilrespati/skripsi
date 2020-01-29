from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

tilt = 17
pan = 27

GPIO.setup(tilt, GPIO.OUT)  # white => TILT
GPIO.setup(pan, GPIO.OUT)  # gray ==> PAN


def setServoAngle(servo, ds):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = ds
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.4)
    pwm.stop()


if __name__ == '__main__':
    for i in range(5, 12, 1):
        print(i)
        setServoAngle(pan, i)
        setServoAngle(tilt, i)
        sleep(0.5)

    setServoAngle(pan, 8)
    setServoAngle(tilt, 7)
    GPIO.cleanup()
