import cv2
import time
import FaceDetectionModule as fd

cap = cv2.VideoCapture(0)
pTime = 0
detector = fd.FaceDetection()
while True:
    success,img = cap.read()
    img,bbox = detector.find_faces(img)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS : {int(fps)}',(20,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    # result = 
    cv2.imshow('image',img)
    cv2.waitKey(1)