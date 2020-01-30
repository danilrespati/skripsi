import cv2
import numpy as np
from PIL import Image
import os

path = '/home/pi/skripsi/data/user/static'
recognizer = cv2.face.LBPHFaceRecognizer_create()
faceCascade = cv2.CascadeClassifier('/home/pi/skripsi'
        '/data/classifier/lbpcascades'
        '/lbpcascade_frontalface.xml')

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    labels = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')
        label = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = faceCascade.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            labels.append(label)
    return faceSamples,labels

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,labels = getImagesAndLabels(path)
recognizer.train(faces, np.array(labels))
recognizer.write('/home/pi/skripsi/data/trainer/static/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(labels))))
