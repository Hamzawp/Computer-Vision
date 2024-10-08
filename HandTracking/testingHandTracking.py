import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.find_hands(img=img)
    landmark_list = detector.find_position(img,draw=False)
    if len(landmark_list) != 0:
        print(landmark_list[4])
    # Setting up FPS     
    cTime = time.time()   
    fps = 1/(cTime-pTime)
    pTime = cTime
        
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)