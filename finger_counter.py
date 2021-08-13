import mediapipe as mp

import cv2
import numpy as np

Frame_Width=640
Frame_Heigth=480

cap=cv2.VideoCapture(0)

cap.set(3,Frame_Width)
cap.set(4,Frame_Heigth)
cap.set(10,150)

def count_fing(img):


    mpHands= mp.solutions.hands
    mpDraw = mp.solutions.drawing_utils
    hands=mpHands.Hands()

    finger = 0

    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_RGB)

    if result.multi_hand_landmarks != None:
        for hlms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hlms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(hlms.landmark):
                cv2.circle(img, (int(lm.x * Frame_Width), int(lm.y * Frame_Heigth)), 10, (255, 0, 0), cv2.FILLED)
                if id >= 2 and id <= 4 and hlms.landmark[id - 1].x < hlms.landmark[id].x and hlms.landmark[id - 2].x < \
                        hlms.landmark[id - 1].x and id % 4 == 0:
                    finger = finger + 1
                if id >= 5 and hlms.landmark[id - 1].y > hlms.landmark[id].y and hlms.landmark[id - 2].y > \
                        hlms.landmark[id - 1].y and id % 4 == 0:
                    finger = finger + 1





    return finger


