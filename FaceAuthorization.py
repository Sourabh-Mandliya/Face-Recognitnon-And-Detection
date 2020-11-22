# CAPTURE IMAGE AND STORE IN FOLDER

import cv2
import numpy as np
import sqlite3
faceDetect=cv2.CascadeClassifier("G:\\project\\ANACONDA\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
cam=cv2.VideoCapture(0);
####################################DATABASE_CONNECTIVITY_PART##################################
def insertOrUpdate(ID,Name):
    #conn=sqlite3.connect("FaceBase.db")
    conn=sqlite3.connect("G:\\project\\DATABASE.db")
    query="SELECT * FROM People WHERE ID = "+str(ID)
    cursor=conn.execute(query)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        query="UPDATE People SET Name="+str(Name)+"WHERE ID="+str(ID)
    else:
        query="INSERT INTO People(ID, Name) VALUES("+str(ID)+","+str(Name)+")"
    conn.execute(query)
    conn.commit()
    conn.close()    
#####################################################################################

ID=input("Enter User ID = ")
Name=input("ENTER NAME = ")
insertOrUpdate(ID,Name)
img2=0
while(True):
     
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray,1.3,5)
   
    for(x,y,w,h) in faces:
         cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
         
         if cv2.waitKey(1):#& 0xff==ord("s"):
            img2=img2+1
            cv2.imwrite('G:\\project\\photo\\User.'+ID+'.'+str(img2)+'.jpg',gray[y:y+h,x:x+w])
        
    cv2.imshow('face',img)
    cv2.waitKey(1)
    if(img2>200):               ######  20-500
        break
cam.release()
cv2.destroyAllWindows()
