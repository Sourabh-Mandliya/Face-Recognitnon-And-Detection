import numpy as np
import os
import cv2
from PIL import Image
import pickle, sqlite3

face_cascade = cv2.CascadeClassifier('G:\\project\\ANACONDA\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')

recognizer =cv2.face.LBPHFaceRecognizer_create();
recognizer.read("G:\\project\\recognizer\\trainningData.yml")
######################################################################################################
def getProfile(ID):
    conn=sqlite3.connect("G:\\project\\DATABASE.db")
    query="SELECT * FROM People WHERE ID="+str(ID)
    cursor=conn.execute(query)
    
    profile=None
    #print(cursor)##############################
    for row in cursor.fetchall():
        print(row)
        profile=row
    conn.close()
    return profile
#########################################################################################################
#to train using frames from video
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
while True:
    #comment the next line and make sure the image being read is names img when using imread
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        ID, conf = recognizer.predict(gray[y:y+h, x:x+w])
        #if conf < 70:
        print(ID)
        profile=getProfile(ID)
        if profile != None:
            cv2.putText(img, "ID: "+str(profile[0]), (x, y+h+30), font, 0.4, (0, 255, 255), 1);#BGR
            cv2.putText(img, "NAME: "+str(profile[1]), (x, y + h + 50), font, 0.4, (0, 255, 255), 1);
                
        else:
            cv2.putText(img, "ID: Unknown", (x, y + h + 30), font, 0.4, (0, 255, 255), 1);#BGR
            cv2.putText(img, "NAME: Unknown", (x, y + h + 50), font, 0.4, (0, 255, 255), 1);
            
    cv2.imshow('img', img)
    if(cv2.waitKey(1) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()

