import torch
import cv2 as cv
import time
from tracker import *

# set var choose = 1 to people and 0 to guns]
choose = 1

if choose == 1:  
# Model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5x, custom
# Custom Model
else: 
    model = torch.hub.load('ultralytics/yolov5', 'custom','./yolo_people_detect/models/yolov5x99.pt')

# Tracker obj
tracker = EuclideanDistTracker()

inicio = time.time()

cap = cv.VideoCapture('./yolo_people_detect/videos/{}'.format('wpeople.mp4'))
# Calculating how many frames the video has
totalFrames = cap.get(cv.CAP_PROP_FRAME_COUNT)
print(totalFrames)

# Seting parameter pro create a mp4 file
h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
w= int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
parameter = cv.VideoWriter_fourcc(*'MP4V')
video = cv.VideoWriter('test-people_walking-yolov5s.mp4', parameter,30,(416,416), isColor =True)

if (cap.isOpened()== False):
    print("Error opening video file")

# Creating a loop just to 30s of video. obs: the fps was choose by 30, so 30*30 =900
for i in range(int(900)):

    count = 0   
    # Creating an array
    detections_bb = []
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    #cv.imshow('frame',frame)
    (width, height) = int(416), int(416)
    dimensions = (width,height)
    frame_resized = cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    #Using yolo to detect
    results = model(frame_resized)
    #cv.imshow('framerez',frame_resized)
          
    if ret == True:

        #converting tensor to array
        info_results = results.xyxy[0].numpy()

        if len(info_results) is not None:
            # print("Detected something")
            # If was a gun
            for i in range (len(info_results)):
                if info_results[i][5] == 0 and info_results[i][4]>0.2:
                    x = int(info_results[i][0])
                    y = int(info_results[i][1])
                    x2 = int(info_results[i][2]) # altura
                    y2 = int(info_results[i][3]) # largura

                    detections_bb.append([x,y,x2,y2])

                    count = count +1
            
            # Obj tracking
            bb_id = tracker.update(detections_bb)
            
            for box_id in bb_id:
                x, y, w, h,id = box_id
                if choose ==1:
                    cv.putText(frame_resized,str(id), (x-2,y-10),cv.FONT_HERSHEY_COMPLEX,0.4,(0,255,0),1)
                    cv.rectangle(frame_resized, (x, y),(w, h), (0, 255, 0), 1)
                else:
                    cv.putText(frame_resized,str(id), (x-2,y-10),cv.FONT_HERSHEY_COMPLEX,0.4,(0,0,255),1)
                    cv.rectangle(frame_resized, (x, y),(w, h), (0, 0, 255), 1)

            # Showing the number os guns or people in each frame
            if count > 9:
                if choose ==1:
                    cv.rectangle(frame_resized, (385, 1),(411, 22), (0, 0, 0), -1) 
                    cv.putText(frame_resized,str(count), (384,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)
                else:
                    cv.rectangle(frame_resized, (292, 1),(411, 22), (0, 0, 0), -1) 
                    cv.putText(frame_resized,'Guns', (300,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),1)
                    cv.putText(frame_resized,str(count), (384,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),1)
            else:
                if choose == 1:
                    cv.rectangle(frame_resized, (385, 1),(411, 22), (0, 0, 0), -1) 
                    cv.putText(frame_resized,str(count), (392,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)
                else:
                    cv.rectangle(frame_resized, (292, 1),(411, 22), (0, 0, 0), -1) 
                    cv.putText(frame_resized,'Guns', (325,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),1)  
                    cv.putText(frame_resized,str(count), (392,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),1)  
            cv.imshow('framerez',frame_resized)
            

            
            video.write(frame_resized)
        else:
            video.write(frame_resized)

        
        

    if(cv.waitKey(10) == ord("q")):
            break
     
        
    if ret == False:
        break
fim = time.time()
print('O codigo demorou: {} segundos'.format(fim-inicio))
cap.release()
cv.destroyAllWindows()
    










