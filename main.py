import torch
import cv2 as cv
import time
from tracker import *
from getAndDraw import *

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

# Get and Draw obj
GaD = getAndDrawBB()

cap = cv.VideoCapture('./yolo_people_detect/videos/{}'.format('peoples.mp4'))
# Calculating how many frames the video has
totalFrames = cap.get(cv.CAP_PROP_FRAME_COUNT)

# Seting parameters to create a mp4 file
h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
w= int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
parameter = cv.VideoWriter_fourcc(*'MP4V')
video = cv.VideoWriter('test2_fullres-peoples-yolov5s.mp4', parameter,30,(1300,700), isColor =True)

if (cap.isOpened()== False):
    print("Error opening video file")


for i in range(int(totalFrames)):
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret is False:
        raise Exception('No frame detected')
        
    # Selecting width and height to the frame.
    (width, height) = int(1300), int(700)
    dimensions = (width,height)
    frame_resized = cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

    #Using yolo to detect
    results = model(frame_resized)

    # Call GaD class, get_bbox function, to get bounding boxes
    bb, count = GaD.get_bbox(results)

    # Call Obj tracking (optional)
    bb_id = tracker.update(bb)

    # Call GaD class, drawBBoxes function to draw the bb around the objects
    # You must call drawBBoxes_with_ID if u wanna track objects
    # Otherwise just call drawBBoxes.
    frame_resized = GaD.drawBBoxes_with_ID(choose, frame_resized,count,video,bb_id,tracker=True)

    cv.imshow('framerez',frame_resized)

    if(cv.waitKey(1) == ord("q")):
            break
     
        

cap.release()
cv.destroyAllWindows()