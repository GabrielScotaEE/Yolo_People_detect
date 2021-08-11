import torch
import cv2 as cv
import time
from tracker import *
# Tracker obj
tracker = EuclideanDistTracker()

class getAndDrawBB:

    def __init__(self) :

        self.sucess = False
        

    def get_bbox(self,results):
        self.count = 0  
        self.detections_bb = []
        
        # Converting tensor to array
        info_results = results.xyxy[0].numpy()

        if len(info_results) is not None:
            # print("Detected something")
            # If was a gun
            for i in range (len(info_results)):
                if info_results[i][5] == 0 and info_results[i][4]>0.55:
                    x = int(info_results[i][0])
                    y = int(info_results[i][1])
                    x2 = int(info_results[i][2]) # altura
                    y2 = int(info_results[i][3]) # largura

                    self.detections_bb.append([x,y,x2,y2])

                    self.count = self.count +1
                

        return self.detections_bb, self.count

       
    def drawBBoxes(self, choose,frame, video, bb, tracker=False):
        self.choose = choose
        self.frame = frame
        self.bb_id = None
        if tracker is False:
            for rect in bb:
                x, y, w, h = rect
                cv.rectangle(self.frame, (x, y),(w, h), (0, 255, 5), 1)
                self.showNumbers()
        else:
            raise Exception("This function don't have tracker, use drawBBoxes_with_ID() instead.")

        
 
        video.write(frame)    
        return frame
        
    def drawBBoxes_with_ID(self, choose, frame, video, bb_id, tracker=True):
        self.frame = frame
        self.bb_id = bb_id
        self.choose = choose

        if tracker is False:
            raise Exception("This function have tracker, use drawBBoxes() instead.")
        
        else:
            self.showNumbers()
 
        video.write(frame)
        return frame
    

    def showNumbers(self):
        if self.bb_id is not None:
            for box_id in self.bb_id:
                    x, y, w, h,id = box_id
                    if self.choose ==1:
                        cv.putText(self.frame,str(id), (x-2,y-10),cv.FONT_HERSHEY_COMPLEX,0.4,(0,255,0),1)
                        cv.rectangle(self.frame, (x, y),(w, h), (0, 255, 0), 1)
                    else:
                        cv.putText(self.frame,str(id), (x-2,y-10),cv.FONT_HERSHEY_COMPLEX,0.4,(0,0,255),1)
                        cv.rectangle(self.frame, (x, y),(w, h), (0, 0, 255), 1)

        if self.count > 9:
            if self.choose ==1:
                cv.rectangle(self.frame, (1268, 1),(1295, 22), (0, 0, 0), -1) 
                cv.putText(self.frame,str(self.count), (1268,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)
            else:
                cv.rectangle(self.frame, (1176, 1),(1295, 22), (0, 0, 0), -1) 
                cv.putText(self.frame,'Guns', (1088,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),1)
                cv.putText(self.frame,str(self.count), (1172,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),1)
        else:
            if self.choose == 1:
                cv.rectangle(self.frame, (1269, 1),(1295, 22), (0, 0, 0), -1) 
                cv.putText(self.frame,str(self.count), (1275,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)
            else:
                cv.rectangle(self.frame, (1080, 1),(1199, 22), (0, 0, 0), -1) 
                cv.putText(self.frame,'Guns', (1113,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),1)  
                cv.putText(self.frame,str(self.count), (1180,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),1)  
        return
        



    










