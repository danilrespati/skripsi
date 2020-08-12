import cv2
import numpy as np

def initCam():  #initialize pi camera configuration
    cap = cv2.VideoCapture(0) # Create a VideoCapture object
    frameWidth = 640
    frameHeight = 480
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, 0.6)
    return cap

def drawRectangle(frame, bbox):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

cap = initCam()
# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
 
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
 
while(True):
  ret, frame = cap.read()
  frame = cv2.flip(frame, -1)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  faces = faceCascade.detectMultiScale(gray, 1.3, 5)
  for(x, y, w, h) in faces:
    drawRectangle(frame, bbox=(x,y,w,h))
    
  if ret == True: 
    # Write the frame into the file 'output.avi'
    out.write(frame)
 
    # Display the resulting frame    
    cv2.imshow('frame',frame)
 
    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else:
    break 
 
# When everything done, release the video capture and video write objects
cap.release()
out.release()
 
# Closes all the frames
cv2.destroyAllWindows()
