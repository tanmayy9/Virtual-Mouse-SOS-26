import cv2
import numpy as np
import mediapipe as mp
import pyautogui

mp_hands=mp.solutions.hands
mp_drawings=mp.solutions.drawing_calculation
hands=mp.hands.Hands(max_num_hands=1,min_detection_confidence=0.7)

screen_w,screen_h = pyautogui.size()
print("\n hand mouse control.")
prev_screen_x,prev_screen_y = 0,0

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)

while True:
    success , frame=cap.read()
    frame = cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawings.draw_landmarks(frame,hand_landmarks,mp.hands.HAND_CONNECTIONS)
        thumb_tip = hand_landmarks.landmark[4]  
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]

        fingers = [
            1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y else 0
        ] 

    cv2.imshow("Live Feed",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows    