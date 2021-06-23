import cv2 as cv


cap = cv.VideoCapture('people.mp4')
totalFrames = cap.get(cv.CAP_PROP_FRAME_COUNT)
if (cap.isOpened()== False):
    print("Error opening video file")
for i in range(int(totalFrames)):
        # get the frame image
        sucess, frame = cap.read()
        # Resizing frame shape by 0.6
      
        if sucess == True:
            
            #Resizing frame by 0.6
             #(width, height) = (1280, 760) #(1366, 768) (1920, 1080) (3840, 2160)
           
            

            cv.imshow('Barcode/QR code reader',frame)
            if(cv.waitKey(10) == ord("q")):
                    break