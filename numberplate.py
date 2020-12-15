import cv2
import numpy as np
webcame=cv2.VideoCapture(0)
# ------- setting width and height of the screen--------------
webcame.set(3,640)
webcame.set(4,480)
numberPlateCascade = cv2.CascadeClassifier("Resources/haarcascades/haarcascade_russian_plate_number.xml")
# ------------------------- set brightness -------------------
webcame.set(10,100)
marea =400
count=0
while True:
    success, webcamimage=webcame.read()
    imagegray=cv2.cvtColor(webcamimage,cv2.COLOR_BGR2GRAY)

    numberplate = numberPlateCascade.detectMultiScale(imagegray,1.1,4)
    for (x,y,width,height) in numberplate:
        area=width*height
        if area>marea:
            cv2.rectangle(webcamimage,(x,y),(x+width,y+height),(0,255,255),2)
            cv2.putText(webcamimage,"Number Plate",(x,y-4),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,255),2)
            imageRegionofInterest = webcamimage[y:y+height,x:x+width]
            cv2.imshow("Number Plate",imageRegionofInterest)
    cv2.imshow("Webcam",webcamimage)
    if cv2.waitKey(1) & 0xff==ord('s'):
        count+=1
        cv2.imwrite('Resources'+str(count)+'.jpg',imageRegionofInterest)
        cv2.rectangle(webcamimage,(0,200),(640,300),(0,255,255),cv2.FILLED)
        cv2.putText(webcamimage,"Saved",(150,265),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),1)
        cv2.imshow("Result",webcamimage)
        cv2.waitKey(100)

        