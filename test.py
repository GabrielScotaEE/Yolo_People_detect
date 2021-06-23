import torch
import cv2 as cv
import pandas as pd
# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5x, custom

img = cv.imread('./images/minafut.jpg')
results = model(img)
#results.show()
info_results = results.xyxy[0].numpy()
print(len(info_results))
print(info_results)
print(info_results[0][5])

if len(info_results) is not None:
    print("Detected something")
    #If was a person
    for i in range (len(info_results)):
        if info_results[i][5] == 0 and info_results[i][4]>0.5:
            x = int(info_results[i][0])
            y = int(info_results[i][1])
            x2 = int(info_results[i][2]) # altura
            y2 = int(info_results[i][3]) # largura
            cv.putText(img,'1',(10,70),cv.FONT_HERSHEY_COMPLEX,2,(0,255,0),3)
            cv.rectangle(img, (x, y),(x2, y2), (0, 255, 0), 2)
    cv.imshow('Frame', img)
    cv.waitKey(0)       
            
            