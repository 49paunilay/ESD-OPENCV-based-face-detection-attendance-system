import cv2
import face_recognition as f
import numpy as np
import os
from datetime import datetime
from pygame import mixer
# ---------------------------------------- Initialisation ------------------------------------
print('Starting process')
mixer.init()
mixer.music.load('r.mp3')

mixer.music.play()
print('Fetching dataset  ------------------------------ ')
path = 'dataset'
images=[]
classnames=[]

myList=os.listdir(path)


for element in myList:
    currentimage=cv2.imread(f'{path}/{element}')
    images.append(currentimage)
    classnames.append(os.path.splitext(element)[0])
print('Starting encoding  ------------------------------ ')
# --------------------------------- Functions ---------------------------------------
def FindEncoding(images):
    encodeList=[]
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # we need to convert BGR format into RGB format as it is compatible with opencv
        encodeimg=f.face_encodings(img)[0] #finding the encodings of image for future processing of data
        encodeList.append(encodeimg)
    return encodeList



encodeListOfDataset = FindEncoding(images)

def markAttendance(name):
    with open('attendance.csv','r+') as fhand:
        attendancelist=fhand.readlines()
        print(attendancelist)
        nameList=[]

        for line in attendancelist:
            entry=line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            currentTime=datetime.now()
            DateTime = currentTime.strftime('%H:%M:%S')
            fhand.writelines(f'\n{name},{DateTime}')
            





print('-------------------------------- Encoding Colpleted ------------------------------ ')
# -------------------------------- Webcam integration ---------------------------------
print('Starting webcam')
mixer.music.stop()
cap=cv2.VideoCapture(0)
while True:
    success, imageWbcam=cap.read()
    imageWbcamSmall=cv2.resize(imageWbcam,(0,0),None,0.25,0.25) # Compressing webcam image to process data faster
    imageWbcamSmall = cv2.cvtColor(imageWbcamSmall,cv2.COLOR_BGR2RGB) # converting image solour scheme

    facesinframe=f.face_locations(imageWbcamSmall)
    faceinFrameEncodings = f.face_encodings(imageWbcamSmall,facesinframe)
    for encodeface,facelocation in zip(faceinFrameEncodings,facesinframe):
        matches=f.compare_faces(encodeListOfDataset,encodeface)
        facedistance=f.face_distance(encodeListOfDataset,encodeface)
        #print(facedistance)
        matchindex=np.argmin(facedistance)
        if matches[matchindex]:
            name=classnames[matchindex].upper()
            #print(name)
            y1,x2,y2,x1=facelocation
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4

            cv2.rectangle(imageWbcam,(x1,y1),(x2,y2),(0,255,255),2)
            cv2.rectangle(imageWbcam,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(imageWbcam,name,(x1+6,y2-6),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
            markAttendance(name)
    cv2.imshow('webcam',imageWbcam)        
    cv2.waitKey(1)

