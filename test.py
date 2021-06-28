import torch
import cv2 as cv
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
from collections import OrderedDict


# Model
model = torch.hub.load('ultralytics/yolov5', 'custom','./yolo_people_detect/models/yolov5s84newdataset.pt')  # or yolov5m, yolov5x, custom


img = cv.imread('./yolo_people_detect/images/squad2.jpg')
results = model(img)
#results.show()
info_results = results.xyxy[0].numpy()
print(len(info_results))
print(info_results)
# print(info_results[0][5])vvbbcx     
inputCentroids = OrderedDict()
#results.show()

if len(info_results) is not None:
    print("Detected something")
    #If was a person
    for i in range (len(info_results)):
        if info_results[i][5] >= 0 and info_results[i][4]>0.30:
            x1 = int(info_results[i][0])
            y1 = int(info_results[i][1])
            x2 = int(info_results[i][2]) # altura
            y2 = int(info_results[i][3]) # largura

            cX = int((x1 + x2) / 2.0)
            cY = int((y1 + y2) / 2.0)
            inputCentroids[i] = (cX, cY)

            cv.putText(img,'1',(10,70),cv.FONT_HERSHEY_COMPLEX,2,(50,100,200),3)
            cv.rectangle(img, (x1, y1),(x2, y2), (230, 0, 150), 2)
    cv.imshow('Frame', img)
    cv.waitKey(0)       

print(inputCentroids)    

print(inputCentroids.keys())    

print(inputCentroids.values())  

objects = inputCentroids

objectIDs = list(objects.keys())
objectIDs = list(objects.keys())
objectCentroids = list(objects.values())

D = dist.cdist(list(inputCentroids.values()), list(inputCentroids.values()))
print('print distances:\n{}'.format(D))
print('print shapes of D:\n {} {}'.format(D.shape[0],D.shape[1]))
rows = D.min(axis=1).argsort()
cols = D.argmin(axis=1)[rows]
print(rows,cols)
usedRows = set()
usedCols = set()  

for (row, col) in zip(rows, cols):
        # if we have already examined either the row or
        # column value before, ignore it
        # val
        if row in usedRows or col in usedCols:
            continue
        # otherwise, grab the object ID for the current row,
        # set its new centroid, and reset the disappeared
        # counter
        objectID = objectIDs[row]
        objects[objectID] = inputCentroids[col]
        #disappeared[objectID] = 0
        # indicate that we have examined each of the row and
        # column indexes, respectively
        usedRows.add(row)
        usedCols.add(col)
print('objectid --- usedrows and usedcols')
print (objectID)
print(usedRows,usedCols)
unusedRows = set(range(0, D.shape[0])).difference(usedRows)
unusedCols = set(range(0, D.shape[1])).difference(usedCols)
print('unused \n {} {}'.format(usedRows,unusedCols))
