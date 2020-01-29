from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def setServoAngle(servoPin, angle):
	pwm = GPIO.PWM(servoPin, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	print(dutyCycle)
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()

if __name__ == '__main__':
	import sys
	servoPin = int(sys.argv[1])
	GPIO.setup(servoPin, GPIO.OUT)
	setServoAngle(servoPin, int(sys.argv[2]))
	GPIO.cleanup()