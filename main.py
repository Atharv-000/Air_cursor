import cv2
import mediapipe as mp
import time
from mouse import move, click
from screeninfo import get_monitors

monitor = get_monitors()[0]
screen_width, screen_height = monitor.width, monitor.height

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_click_time = 0

def detect_click(landmarks):
    # Check distance between index and thumb tips
    index_tip = landmarks[8]
    thumb_tip = landmarks[4]
    distance = ((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2) ** 0.5
    return distance < 0.05

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark
            index_finger = landmarks[8]
            x = int(index_finger.x * screen_width)
            y = int(index_finger.y * screen_height)
            move(x, y)
            
            if detect_click(landmarks):
                if time.time() - prev_click_time > 1:
                    click()
                    prev_click_time = time.time()

    cv2.imshow("AirCursor", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
