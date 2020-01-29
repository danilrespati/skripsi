'''
Face detection and tracking with OpenCV
    ==> Real Time tracking with Pan-Tilt servos 
    Based on original tracking object code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2016/05/09/opencv-rpi-gpio-and-gpio-zero-on-the-raspberry-pi/
Developed by Marcelo Rovai - MJRoBot.org @ 9Feb2018 
'''

# import the necessary packages
import picamera
import picamera.array
import time
import cv2
import os
import RPi.GPIO as GPIO

# define Servos GPIOs
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
tiltServo = 11
panServo = 13

def init_cam():
	"""
	Function for setting up the camera
	"""
	camera = picamera.PiCamera()
	camera.resolution = (400, 304)
	camera.framerate = 30
	camera.vflip = True
	camera.hflip = True
	return camera
	
def detect_face(image):
	"""
	Face detection
	"""
	# grayscale the image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
	# detecting face(s)
	faces = faceCascade.detectMultiScale(gray, 1.3, 3, 0)
	return faces
		
def positionServo (servo, angle):
	"""
	Servo positioning
	"""
	os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
	print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

def mapServoPosition (x, y):
	"""
	Servo angle centering
	"""
	global panAngle
	global tiltAngle
	if (x < 150):
		if panAngle >= 150:
			panAngle = 150
		else :
			panAngle += 5
			positionServo (panServo, panAngle)
	if (x > 250):
		if panAngle <= 30:
			panAngle = 30
		else :
			panAngle -= 5
			positionServo (panServo, panAngle)
	if (y < 100):
		if tiltAngle >= 140:
			tiltAngle = 140
		else :
			tiltAngle -= 10
			positionServo (tiltServo, tiltAngle)
	if (y > 150):
		if tiltAngle <= 40:
			tiltAngle = 40
		else :
			tiltAngle += 10
			positionServo (tiltServo, tiltAngle)

faceCascade = cv2.CascadeClassifier('/home/pi/Skripsi/repository'
		'/data/classifier/haarcascades'
		'/haarcascade_frontalface_default.xml')

# initialize the camera
camera = init_cam()

# grab a reference for the raw camera capture
rawCapture = picamera.array.PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.25)

# initialize angle servos at 90-90 (middle) position
global panAngle
global tiltAngle
panAngle = 90
tiltAngle =90

# positioning Pan/Tilt servos at initial position
positionServo (panServo, panAngle)
positionServo (tiltServo, tiltAngle)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", 
		use_video_port=True):
	# initialize face index and location list		
	i = 0
	loc = [ ]		
	
	# grab the raw array representing the image
	image = rawCapture.array
	
	faces = detect_face(image)
	
	# edit frame image this 'for' will loop for each face found in frame 		
	for (x,y,w,h) in faces:
		# print rectangle around face
		cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
		# centering face location
		x = x+(w/2)
		y = y+(h/2)
		# print additional info 
		cv2.putText(image, 'Faces   : {}'.format(len(faces)), (10,20), 
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
		cv2.putText(image, 'Location : {0},{1}'.format(x,y), (10,((i*20)+40)), 
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)	
		loc.insert(i,[i+1,x,y])
		i += 1
		if i == 1:
			mapServoPosition(int(x), int(y))

					
	# show to screen	
	cv2.imshow('Preview',image)
	
	# if the `ESC` key is pressed, break from the loop
	key = cv2.waitKey(1) & 0xFF
	if key == 27:
		break
	
	rawCapture.truncate(0)

# do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff \n")
# repositioning servo (centering)
positionServo (panServo, 90)
positionServo (tiltServo, 90)
GPIO.cleanup()
cv2.destroyAllWindows()
