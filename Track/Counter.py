import numpy as np
import cv2
import Person
import time



# create object to manage trace messages


# Contadores de entrada y salida
cnt_up = 0
cnt_down = 0

# Fuente de video
# cap = cv2.VideoCapture(0)
hair_cascade = cv2.CascadeClassifier("/Users/rahuljain/Documents/FreelacerProf/cascadeH5.xml")
if hair_cascade:
    print 'empty'
cap = cv2.VideoCapture('videoplayback.mp4')
cap.set(cv2.CAP_PROP_FPS, 100)

# Check if camera opened successfully
if (cap.isOpened() is False):
    print("Error opening video stream or file")

# Get current width and height of frame
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)     # float
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)   # float
print("Frame Width, Height = ", width, ",", height)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(width), int(height)))                     #noqa

# Propiedades del video
# cap.set(3, 160) # Width
# cap.set(4, 120) # Height

# Imprime las propiedades de captura a consola
for i in range(19):
    print(i, cap.get(i))

wf = cap.get(3)
hf = cap.get(4)
frameArea = hf*wf
areaTH = frameArea/300
print('Area Threshold', areaTH)

# Lineas de entrada/salida
line_up = int(0.3*hf)
line_down1 = int(0.58*hf)
line_down = int(0.6*(hf))
line_down2 = int(0.62*hf)

up_limit = int(0.56*hf)
down_limit = int(0.64*hf)

right_limit = int(4.2*(wf/5))

print("Red line y:", str(line_down))
print("Blue line y:", str(line_up))
line_down_color = (255, 0, 0)
line_up_color = (0, 0, 255)
pt1 = [0,line_down]
pt2 = [wf,line_down]
pts_L1 = np.array([pt1, pt2], np.int32)
pts_L1 = pts_L1.reshape((-1, 1, 2))
pt3 = [0, line_up]
pt4 = [wf, line_up]
pts_L2 = np.array([pt3, pt4], np.int32)
pts_L2 = pts_L2.reshape((-1, 1, 2))

pt5 = [0, up_limit]
pt6 = [wf, up_limit]
pts_L3 = np.array([pt5, pt6], np.int32)
pts_L3 = pts_L3.reshape((-1, 1, 2))
pt7 = [0, down_limit]
pt8 = [wf, down_limit]
pts_L4 = np.array([pt7, pt8], np.int32)
pts_L4 = pts_L4.reshape((-1, 1, 2))


font = cv2.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 3
pid = 1

while(cap.isOpened()):

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hair = hair_cascade.detectMultiScale(gray,1.1,4)

    for i in persons:
        i.age_one()  

    for (x,y,w,h) in hair:
        area = w*h
        if area > areaTH:
            
            cx = int(x+w/2)
            cy = int(y+h/2)
            

            new = True
            if cy in range(up_limit, down_limit):
                if cx in range(0,right_limit):
                    for i in persons:
                        if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
                            # el objeto esta cerca de uno que ya se detecto antes
                            new = False
                            passed = False
                            back = False
                            
                            i.updateCoords(cx, cy)   # actualiza coordenadas en el objeto and resets age     #noqa
                            
                            if i.going_UP(line_down1, line_up) is True:
                                cnt_up += 1
                                print("ID:", i.getId(), 'crossed going up at', time.strftime("%c"))          #noqa
                            
                            elif i.going_DOWN(line_down1, line_up, h/2) is True:
                                passed = True
                                index = persons.index(i)
                                persons.pop(index)
                                print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))        #noqa

                            
                            elif i.going_REV(line_down1, line_up, h/2) is True:
                                back= True
                                index = persons.index(i)
                                persons.pop(index)
                                print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))


                            elif i.going_DOWN(line_down, line_up, h/2) is True:
                        
                                passed = True
                                # cnt_down += 1
                                index = persons.index(i)
                                persons.pop(index)
                                print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))

                            
                            elif i.going_REV(line_down, line_up, h/2) is True:
                                back= True
                                index = persons.index(i)
                                persons.pop(index)
                                print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))

                            elif i.going_DOWN(line_down2, line_up, h/2) is True:
                                passed = True
                                # cnt_down += 1
                                index = persons.index(i)
                                persons.pop(index)
                                print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))

                            elif i.going_REV(line_down2, line_up, h/2) is True:
                                back= True
                                index = persons.index(i)
                                persons.pop(index)
                                print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))
                            
                            # elif i.going_REV(line_down, line_up, h/2) is True:
                            #     back= True
                            #     index = persons.index(i)
                            #     persons.pop(index)
                            #     print("ID:", i.getId(), 'crossed going down at', time.strftime("%c"))

                            if passed:
                                cnt_down += 1
                            # if back:
                            #     cnt_down -= 1

                            break
                        if i.getState() == '1':
                            if i.getDir() == 'down' and i.getY() > down_limit:
                                i.setDone()
                            # elif i.getDir() == 'up' and i.getY() < up_limit:
                            #     i.setDone()
                        if i.timedOut():
                            # sacar i de la lista persons
                            index = persons.index(i)
                            persons.pop(index)
                            del i     # liberar la memoria de i
                    if new is True:
                        p = Person.MyPerson(pid, cx, cy, max_p_age)
                        persons.append(p)
                        pid += 1
            #################
            #   DIBUJOS     #
            #################
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.rectangle(frame,(x+w/4,y+h/4), (x+3*w/4,y+3*h/4), (255,0,0), 2)
            # cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3)

    # END for cnt in contours0

    #########################
    # DIBUJAR TRAYECTORIAS  #
    #########################
    for i in persons:
        # if len(i.getTracks()) >= 2:
            # pts = np.array(i.getTracks(), np.int32)
            # pts = pts.reshape((-1, 1, 2))
            # frame = cv2.polylines(frame, [pts], False, i.getRGB())
        # if i.getId() == 9:
            # print(str(i.getX()), ', ', str(i.getY()))
        cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv2.LINE_AA)  #noqa

    #################
    #   IMAGANES    #
    #################
    str_up = 'UP: ' + str(cnt_up)
    str_down = 'DOWN: ' + str(cnt_down)
    print str_down
    print str_up
    frame = cv2.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
    frame = cv2.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
    frame = cv2.polylines(frame, [pts_L3], False, (255, 255, 255), thickness=1)
    frame = cv2.polylines(frame, [pts_L4], False, (255, 255, 255), thickness=1)
    cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)  #noqa
    cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)  #noqa
    cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)  #noqa
    cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)  #noqa

    cv2.imshow('Frame', frame)
    # cv2.imshow('Mask', mask)

    # write the flipped frame
    out.write(frame)

    # preisonar ESC para salir
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
# END while(cap.isOpened())

    #################
    #   LIMPIEZA    #
    #################
print int(cnt_down/3)
cap.release()
out.release()
cv2.destroyAllWindows()
