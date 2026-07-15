import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import math
#from calculation import get_angle,get_distance

mp_hands=mp.solutions.hands
mp_drawings=mp.solutions.drawing_utils
hands=mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.7)
smoothing = 5
frame_reduction = 100

screen_w,screen_h = pyautogui.size()
print("\n hand mouse control.")
prev_screen_x,prev_screen_y = 0,0
scroll_ref_y = None

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)

click_start_time= None
click_times=[]
click_cooldown=0.5
scroll_mode=False
freeze_cursor=False


while True:
    success , frame=cap.read()
    frame = cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawings.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)
        thumb_tip = hand_landmarks.landmark[4]  
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]

        fingers = [
            1 if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y else 0
            for tip in [8,12,16,20]
        ] 
        # distnace btw thumb and index
        dist=math.hypot(thumb_tip.x - index_tip.x , thumb_tip.y-index_tip.y)
        CLICK_ENTER = 0.055
        CLICK_EXIT = 0.07
        if dist< CLICK_ENTER:
            if not freeze_cursor:
                freeze_cursor=True
                click_times.append(time.time())
                #double click check
                if len(click_times)>=2 and click_times[-1]-click_times[-2]<0.4:
                    pyautogui.doubleClick()
                    cv2.putText(frame,"Double Click",(10,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,255,255),2)
                    click_times=[]
                else:
                    pyautogui.click()
                    cv2.putText(frame,"Single Click",(10,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,255,255),2)    
        elif freeze_cursor and dist > CLICK_EXIT:
                freeze_cursor=False

        # moving cursor via index finger
        if not freeze_cursor:  
            raw_x = int(index_tip.x * frameWidth)
            raw_y = int(index_tip.y * frameHeight)
            screen_x_target = np.interp(raw_x, [frame_reduction, frameWidth - frame_reduction], [0, screen_w])
            screen_y_target = np.interp(raw_y, [frame_reduction, frameHeight - frame_reduction], [0, screen_h])
            screen_x = prev_screen_x + (screen_x_target - prev_screen_x)/smoothing
            screen_y = prev_screen_y + (screen_y_target - prev_screen_y)/smoothing
            screen_x = min(max(screen_x, 0), screen_w - 1)
            screen_y = min(max(screen_y, 0), screen_h - 1)
            pyautogui.moveTo(screen_x,screen_y,duration=0)
            prev_screen_x,prev_screen_y = screen_x,screen_y

        #scroll mode
        if sum(fingers) == 4:
            if not scroll_mode:
                 scroll_ref_y = index_tip.y
            scroll_mode=True
        else:
            scroll_mode=False
            scroll_ref_y = None

        #scroll actions
        if scroll_mode and scroll_ref_y is not None:
            delta = index_tip.y - scroll_ref_y
            if delta < -0.08:
                pyautogui.scroll(60)
                cv2.putText(frame,"Scroll Up",(10,90),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,255,0),2)  
            if delta > 0.08:
                pyautogui.scroll(-60)
                cv2.putText(frame,"Scroll Down",(10,90),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,1,(0,255,0),2)  

          
    cv2.imshow("Live Feed",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows() 