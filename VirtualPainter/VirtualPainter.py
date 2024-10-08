import cv2
import numpy as np
import os
import HandTrackingModule as htm

folderPath = "Header"
myList = os.listdir(folderPath)

overlaylist = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlaylist.append(image)

header = overlaylist[0]
drawColor = (0,0,255)

cap = cv2.VideoCapture(0)

detector = htm.handDetector(detection_conf=0.85)
xp, yp = 0, 0
eraserThickness = 80
brushThickness = 15

imgCanvas = np.zeros((480, 640, 3), np.uint8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False) 

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            if y1<79:
                if 115<x1<215:
                    header=overlaylist[0]
                    drawColor=(0,0,255)
                elif 215<x1<315:
                    header=overlaylist[1]
                    drawColor=(0,255,0)
                elif 315<x1<415:
                    header=overlaylist[2]
                    drawColor=(255,0,0)
                elif 415<x1<545:
                    header=overlaylist[3]
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

            xp,yp=x1,y1

    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    img[0:79, 0:1280] = header
    cv2.imshow("Image", img)
    cv2.waitKey(1)
