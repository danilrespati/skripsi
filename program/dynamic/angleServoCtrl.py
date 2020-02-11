from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def setServoAngle(servo, angle):
	if (-90 <= angle <= 90):
		pwm = GPIO.PWM(servo, 50)
		pwm.start(8)
		#dutyCycle = ((7*angle)+1350)/180
		#dutyCycle = angle / 18. + 3.
		#dutyCycle = angle / 10
		dutyCycle = ((angle*-1)+126) / 18
		pwm.ChangeDutyCycle(dutyCycle)
		sleep(0.3)
		pwm.stop()

if __name__ == '__main__':
	import sys
	servo = int(sys.argv[1])
	angle = int(sys.argv[2])
	GPIO.setup(servo, GPIO.OUT)
	setServoAngle(servo, angle)
	GPIO.cleanup()