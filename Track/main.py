import cv2
import sys
 
minor_ver = 3
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
    hair_cascade = cv2.CascadeClassifier("/Users/rahuljain/Documents/FreelacerProf/cascadeH5.xml")
    if hair_cascade:
        print 'empty'
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[1]
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
 
    # Read video
    cap = cv2.VideoCapture("video2.mp4")
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)     # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(width), int(height)))
    wf = cap.get(3)
    hf = cap.get(4)
    frameArea = hf*wf
    areaTH = frameArea/270
 
    # Exit if video not opened.
    if not cap.isOpened():
        print "Could not open video"
        sys.exit()
 
    # Read first frame.
    ok, frame = cap.read()
    if not ok:
        print 'Cannot read video file'
        sys.exit()
     
    # Define an initial bounding box
    # tdbox = (287, 23, 86, 320)
 
    # # Uncomment the line below to select a different bounding box
    # tdbox = cv2.selectROI(frame, False)
 
    # # Initialize tracker with first frame and bounding box
    # ok = tracker.init(frame, tdbox)
    trackedpersons = [[0,0,2,3,1,1]]
    tracked = []

 
    while True:
        # Read a new frame
        ok, frame = cap.read()
        if not ok:
            break
         
        # Start timer
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hair = hair_cascade.detectMultiScale(gray,1.1,4)
        
        
        currentpersons = [[0,0,2,3,1,1]]
        
        i = 0
        for track in tracked:
            td, tdbox = track.update(frame)
            if td:
                p1 = (int(tdbox[0]), int(tdbox[1]))
                p2 = (int(tdbox[0] + tdbox[2]), int(tdbox[1] + tdbox[3]))
                wtd = abs(p2[0]-p1[0])
                htd = abs(p2[1]-p1[1])
                cx = int((tdbox[0] + tdbox[2])/2)
                cy = int((tdbox[1]+tdbox[3])/2)
                trackedpersons.append([p1[0],p1[1],wtd,htd,cx,cy])
                cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            i = i + 1
        
        for (x,y,w,h) in hair:
            print hair
            area = w*h
            cx = x + w/2
            cy =y + h/2
            new = False
            if area > areaTH:
                for person in currentpersons:
                    if abs(cx - person[0]) >= person[2] or abs(cy - person[1]) >= person[3]:
                        
                        for tperson in trackedpersons:
                            if abs(cx - tperson[0]) >= tperson[2] or abs(cy - tperson[1]) >= tperson[3]:
                                print 'yee'
                                new = True
                if new:
                    print 'yes'
                    cv2.rectangle(frame,(x+w/4,y+h/4), (x+3*w/4,y+3*h/4), (255,0,0), 2)
                    k = x + w
                    n = y + h
                    tcbox = (x, y, x+w/2, y+h/2)
                    print tcbox
                    currentpersons.append([x,y,w,h,cx,cy])
                    t =  cv2.TrackerMIL_create()
                    print t
                    t.init(frame,tcbox)
                    tracked.append(t)
                           
    
        

        

        # timer = cv2.getTickCount()
 
        # # Update tracker
        # ok, tdbox = tracker.update(frame)
 
        # # Calculate Frames per second (FPS)
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # # Draw bounding box
        # if ok:
        #     # Tracking success
        #     p1 = (int(tdbox[0]), int(tdbox[1]))
        #     p2 = (int(tdbox[0] + tdbox[2]), int(tdbox[1] + tdbox[3]))
        #     cx = int((tdbox[0] + tdbox[2])/2)
        #     cy = int((tdbox[1]+tdbox[3])/2)
        #     cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        # else :
        #     # Tracking failure
        #     cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # # Display tracker type on frame
        # cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # # Display FPS on frame
        # cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
