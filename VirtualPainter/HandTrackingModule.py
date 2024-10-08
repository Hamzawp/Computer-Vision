import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self,mode=False,max_hands=2,model_complexity=1,detection_conf=0.5,track_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.track_conf = track_conf
        self.model_complex = model_complexity
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,
                                        self.max_hands,
                                        self.model_complex,
                                        self.detection_conf,
                                        self.track_conf)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4,8,12,16,20]
        
    def find_hands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        
        if self.results.multi_hand_landmarks:
            for hand_landmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,hand_landmark,self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self,img,hand_number=0,draw=True,):
        self.landmark_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_number]
            for id,lm in enumerate(my_hand.landmark):
                # print(id,lm)    
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                self.landmark_list.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED)
                
        return self.landmark_list  
    
    def fingersUp(self):
        fingers = []
        # Thumb
        if self.landmark_list[self.tipIds[0]][1] > self.landmark_list[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1,5):
            if self.landmark_list[self.tipIds[id]][2] < self.landmark_list[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers