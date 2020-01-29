import cv2
import os
import numpy as np
import math

def sendCoordinate(stat, target, x, y, sx):
    """
    Send Coordinates
    """
    path = "/var/www/html/skripsi"
    os.chdir(path)
    message = """
		<?php
        $stat = {a};
        $target = '{b}';
        $x = {c};
        $y = {d};
        $sx = {e}""".format(a=stat, b=str(target), c=x, d=y, e=sx) + """
		?>
		"""
    f = open('var.php', 'w')
    f.write(message)
    f.close()
    # print("Sending {0}'s position: {1}, {2} \n".format(target, x, y))

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/skripsi/data/trainer/static/trainer.yml')
faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
                                    '/data/classifier/lbpcascades'
                                    '/lbpcascade_frontalface.xml')

stat = 1
font = cv2.FONT_HERSHEY_SIMPLEX

# iniciate id counter
id = 0
target = input('Target: ')
print('(ESC) Exit\n(c) Change target')
# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Danil', 'Ayu', 'Yoga', 'Toni',
         'Azi', 'Joko', 'Tingkir', 'Bawa', 'Taufiq']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
frameWidth = 1280
frameHeight = 720
cam.set(3, frameWidth)  # set video width
cam.set(4, frameHeight)  # set video height
cam.set(10, 0.6)

# Define min window size to be recognized as a face (for optimizing)
minW = 0
minH = 0
ppm = 430
vid = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frameWidth, frameHeight))
while (stat == 1):
    ret, frame = cam.read()
    frame = cv2.flip(frame, -1)
    cv2.line(frame, (int(frameWidth/2),0), (int(frameWidth/2),int(frameHeight)), (0,255,0), 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    i = 0
    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        cv2.putText(frame, str(id), (x, y-5), font, 1, (0, 0, 0), 2)
        cv2.putText(frame, str(confidence), (x, y+h-5), font, 1, (0, 0, 0), 1)
        # print additional info
        cv2.putText(frame, 'Name     : {}'.format(id), (10, ((i*20)+20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        cv2.putText(frame, 'Location : {0},{1}'.format(x, y), (200, ((i*20)+20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        if (target == id):
            cv2.line(frame, (int(x+(w/2)),int(y+(h/2))), (int(frameWidth/2),int(y+(h/2))), (0,255,0), 2)
            # Print distance from middle line in cm
            jarak = round(((x+(w/2)-(frameWidth/2)))/ppm*100)
            cv2.putText(frame, str(abs(jarak)), (int(((x+(w/2))+(frameWidth/2))/2), int(y+(h/2)-15)), font, 1, (0, 0, 0), 1)
            sx = round(math.degrees(math.atan(jarak/240)))
            cv2.putText(frame, str(sx), (int(((x+(w/2))+(frameWidth/2))/2), int(y+(h/2)+15)), font, 1, (0, 0, 0), 1)
            sendCoordinate(stat, target, x, y, sx)
        # else:
            # print('No match! ({0})\n'.format(target))
    vid.write(frame)
    cv2.imshow('camera', frame)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == ord('c'):
        target = input('New target: ')
        print('\nTarget: {0}'.format(target))
        print('(ESC) Exit\n(c) Change target')
    if k == 27:
        sendCoordinate(0, target, x, y, sx)
        stat = 0

# Do a bit of cleanup
print("\n[INFO] Exiting Program and cleanup stuff")
cam.release()
vid.release()
cv2.destroyAllWindows()
