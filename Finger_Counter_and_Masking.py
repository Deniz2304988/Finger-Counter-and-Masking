#opencv trials

import cv2
import numpy as np
from finger_counter import count_fing


Frame_Width=640
Frame_Heigth=480

cap=cv2.VideoCapture(0)

cap.set(3,Frame_Width)
cap.set(4,Frame_Heigth)
cap.set(10,150)

mycolour=([103,124,143,255,110,255])
def no_change(a):
    pass

cv2.namedWindow("Track_Bars")
cv2.resizeWindow("Track_Bars",640,240)
cv2.createTrackbar("H Min","Track_Bars",103,179,no_change)
cv2.createTrackbar("H Max","Track_Bars",124,179,no_change)
cv2.createTrackbar("Sat Min","Track_Bars",143,255,no_change)
cv2.createTrackbar("Sat Max","Track_Bars",255,255,no_change)
cv2.createTrackbar("V Min","Track_Bars",110,255,no_change)
cv2.createTrackbar("V Max","Track_Bars",255,255,no_change)

def find_counter(img):
    counter,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x=0
    y=0
    w=0
    h=0
    for cnt in counter:
        area=cv2.contourArea(cnt)
        if area>0.5:
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y , w , h = cv2.boundingRect(approx)

    return x+w//2,y

drawn_points=[]
while True:
    success, img = cap.read()
    img_last=img.copy()
    img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min=cv2.getTrackbarPos("H Min","Track_Bars")
    h_max = cv2.getTrackbarPos("H Max", "Track_Bars")
    s_min = cv2.getTrackbarPos("Sat Min", "Track_Bars")
    s_max = cv2.getTrackbarPos("Sat Max", "Track_Bars")
    v_min = cv2.getTrackbarPos("V Min", "Track_Bars")
    v_max = cv2.getTrackbarPos("V Max", "Track_Bars")

    mask=cv2.inRange(img_hsv,np.array([h_min,s_min,v_min]),np.array([h_max,s_max,v_max]))
    x,y=find_counter(mask)
    if (x != 0   and   y!=0) :
        drawn_points.append([x,y])
    for points in drawn_points:
        cv2.circle(img_last,(points[0],points[1]),10,(255,0,0),cv2.FILLED)
    image_result=cv2.bitwise_and(img,img,mask=mask)
    if cv2.waitKey(1) & 0xFF == ord("d") or count_fing(img)==10 :
        drawn_points=[]
    cv2.imshow("hh",img_last)

