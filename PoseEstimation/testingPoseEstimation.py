import cv2
import time
import PoseEstimationModule as pem

cap = cv2.VideoCapture(0)
pTime = 0
detector = pem.Pose_Detector()

while True:
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    while True:
        success,img = cap.read()
        img = detector.find_pose(img)
        lm_list = detector.find_position(img,draw=False)
        cv2.circle(img,(lm_list[14][1],lm_list[14][2]),5,(255,0,0),cv2.FILLED)
        # print(lm_list)

        cTime = time.time()   
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)
    
        cv2.imshow("Image",img)
        cv2.waitKey(1)