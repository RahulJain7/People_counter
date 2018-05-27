import cv2
import numpy as np

hair_cascade = cv2.CascadeClassifier("/Users/rahuljain/Documents/FreelacerProf/HS.xml")
if hair_cascade:
	print 'empty'
cap = cv2.VideoCapture('videoplayback.mp4')
cap.set(cv2.CAP_PROP_FPS, 30)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)     # float
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (int(width), int(height)))

while True:
	ret, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	hair = hair_cascade.detectMultiScale(gray,1.1,4)
	for (x,y,w,h) in hair:
		print cv2.contourArea(hair)
		cv2.rectangle(img,(x+w/4,y+h/4), (x+3*w/4,y+3*h/4), (255,0,0), 2)

	cv2.imshow('img', img)
	out.write(img)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()