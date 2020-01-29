import numpy as np
import cv2
width = 1280
height = 720
cap = cv2.VideoCapture(0)
cap.set(3,width) # set Width
cap.set(4,height) # set Height
cap.set(10,0.6)    
ok, img = cap.read()
frame = cv2.flip(img, -1)
bbox = (112, 50, 88, 126)
tu = (bbox[0],bbox[1])
wa = ((bbox[0]+bbox[2]),bbox[1])
ga = (bbox[0],(bbox[1]+bbox[3]))
pa = ((bbox[0]+bbox[2]),(bbox[1]+bbox[3]))
ppm = ((bbox[2]/0.2)+(bbox[3]/0.3))/2 # actual box 20x30cm
# Uncomment to calibrate
# bbox = cv2.selectROI(frame, False)
print(bbox)
print(tu)
print(wa)
print(ga)
print(pa)
print(ppm)
while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1) # Flip camera vertically
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Middle line
    cv2.line(frame, (640,0), (640,height), (0,0,255), 4)
    # Indicator
    cv2.line(frame, (bbox[0],0), (bbox[0],height), (255,0,0), 2)
    cv2.line(frame, ((bbox[0]+bbox[2]),0), ((bbox[0]+bbox[2]),height), (0,255,0), 2)
    cv2.line(frame, (0,bbox[1]), (width,bbox[1]), (0,0,255), 2)
    cv2.line(frame, (0,(bbox[1]+bbox[3])), (width,(bbox[1]+bbox[3])), (0,0,0), 2)
    # Coordinate arrow
    cv2.line(frame, (0,0), (int(width/20),int(height/20)), (0,0,255), 2)
    cv2.line(frame, (int((width/20)-15),int(height/20)), (int(width/20),int(height/20)), (0,0,255), 2)
    cv2.line(frame, (int(width/20),int((height/20)-15)), (int(width/20),int(height/20)), (0,0,255), 2)
    cv2.imshow('frame', frame)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()
