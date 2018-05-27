
#Author Rahul Jain
import numpy as np
import cv2
import os
# import pexpect

cap = cv2.VideoCapture(0)


width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)     # float
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)   # float
print("Frame Width, Height = ", width, ",", height)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
out = cv2.VideoWriter('video.mp4', fourcc, 20.0, (int(width), int(height))) 

try:

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            frame = cv2.flip(frame,0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    
    cap.release()
    out.release()

except:
    print 'recording ended'


os.system("scp video.mp4 rahuljain@35.190.147.42:")
cv2.destroyAllWindows()

