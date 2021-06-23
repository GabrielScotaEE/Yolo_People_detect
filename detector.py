import torch
import cv2 as cv
import time
# Model

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5x, custom

inicio = time.time()
cap = cv.VideoCapture('./videos/{}'.format('wpeople.mp4'))
totalFrames = cap.get(cv.CAP_PROP_FRAME_COUNT)
print(totalFrames)

h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
w= int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

parameter = cv.VideoWriter_fourcc(*'MJPG')
video = cv.VideoWriter('detectpeople.avi', parameter,30,(416,416), isColor =True)

if (cap.isOpened()== False):
    print("Error opening video file")

for i in range(int(totalFrames)):
#for i in range(15):
    count = 0   
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
            #print("Detected something")
            #If was a person
            for i in range (len(info_results)):
                if info_results[i][5] == 0 and info_results[i][4]>0.5:
                    x = int(info_results[i][0])
                    y = int(info_results[i][1])
                    x2 = int(info_results[i][2]) # altura
                    y2 = int(info_results[i][3]) # largura
                    cv.rectangle(frame_resized, (x, y),(x2, y2), (0, 255, 0), 2)
                    
                    count = count +1
                    
            cv.putText(frame_resized,str(count), (400,20),cv.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)         
            #cv.imshow('framerez',frame_resized)

            
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
    










