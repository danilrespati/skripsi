import cv2
import os

def initCam():
    global frameWidth
    global frameHeight
    frameWidth = 640
    frameHeight = 480
    brightness = 0.6
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, brightness)
    return cap

cam = initCam()
faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
		'/data/classifier/lbpcascades'
		'/lbpcascade_frontalface.xml')
label = input('\n enter user label and press <return> ==>  ')
print("\n [INFO] Initializing face capture. Look the camera and wait ...")
count = 0
while(True):
    ret, frame = cam.read()
    frame = cv2.flip(frame, -1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        count += 1
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)     
        cv2.imwrite("/home/pi/skripsi/data/user/dynamic/User." + str(label) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', frame)
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 100:
         break
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
