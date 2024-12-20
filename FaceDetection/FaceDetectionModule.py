import cv2
import mediapipe as mp
import time

class FaceDetection():
    
    def __init__(self):
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.face_detection = self.mpFaceDetection.FaceDetection()
        
    def find_faces(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.face_detection.process(imgRGB)
        bboxs = []
        if self.results.detections:
            for id,detection in enumerate(self.results.detections):
            # mpDraw.draw_detection(img,detection)
            ## manual draw
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih),\
                    int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id,bbox,detection.score])
                img = self.fancy_draw(img,bbox)                
                cv2.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),1)
                
                return img,bbox
            
    def fancy_draw(self,img,bbox, l=30,t=5,rt=1):
        x,y,w,h = bbox
        x1,y1 = x+w,y+h
        
        cv2.rectangle(img,bbox,(255,0,255),rt)
        #top left x,y
        cv2.line(img,(x,y),(x+l,y),(255,0,255),t)
        cv2.line(img,(x,y),(x,y+l),(255,0,255),t)
        #top right  x1,y
        cv2.line(img,(x1,y),(x1 - l,y), (255,0,255),t)
        cv2.line(img,(x1,y),(x1,y+l), (255,0,255),t)
        #Bottom left
        cv2.line(img,(x,y1),(x+l,y1),(255,0,255),t)
        cv2.line(img,(x,y1),(x,y1 - l),(255,0,255),t)
        #Bottom right
        cv2.line(img,(x1,y1),(x1-l,y1), (255,0,255),t)
        cv2.line(img,(x1,y1),(x1,y1-l), (255,0,255),t)
        
        return img
        
    
# def main():
#     cap = cv2.VideoCapture(0)
#     pTime = 0
#     detector = FaceDetection()
#     while True:
#         success,img = cap.read()
#         img,bbox = detector.find_faces(img)
#         cTime = time.time()
#         fps = 1/(cTime-pTime)
#         pTime = cTime
#         cv2.putText(img,f'FPS : {int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
#         # result = 
#         cv2.imshow('image',img)
#         cv2.waitKey(1)
    
# if __name__ == '__main__':
#     main()