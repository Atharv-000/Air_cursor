import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math

cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

click_threshold = 40
scrolling = False
scroll_direction = None
last_scroll_time = time.time()

def calculate_distance(p1, p2):
return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

while True:
_, frame = cap.read()
frame = cv2.flip(frame, 1)
frame_height, frame_width, _ = frame.shape
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
output = hands.process(rgb_frame)
hands_landmarks = output.multi_hand_landmarks

if hands_landmarks:
    for hand_landmarks in hands_landmarks:
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        landmarks = []
        for lm in hand_landmarks.landmark:
            x, y = int(lm.x * frame_width), int(lm.y * frame_height)
            landmarks.append((x, y))

        index_finger_tip = landmarks[8]
        thumb_tip = landmarks[4]
        middle_finger_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]

        pyautogui.moveTo(index_finger_tip[0] * screen_width / frame_width,
                         index_finger_tip[1] * screen_height / frame_height)

        # Left Click (Index + Thumb)
        if calculate_distance(index_finger_tip, thumb_tip) < click_threshold:
            pyautogui.click()
            time.sleep(0.3)

        # Right Click (Middle + Thumb)
        if calculate_distance(middle_finger_tip, thumb_tip) < click_threshold:
            pyautogui.rightClick()
            time.sleep(0.3)

        # "YES" Gesture (Index and Middle Up)
        fingers_up = [landmarks[i][1] < landmarks[i - 2][1] for i in [8, 12]]
        if fingers_up == [True, True]:
            print("YES GESTURE DETECTED")

        # Fist for Scrolling
        fingers_folded = [calculate_distance(landmarks[i], landmarks[0]) < 60 for i in [8, 12, 16, 20]]
        if all(fingers_folded):
            wrist = landmarks[0]
            knuckle = landmarks[9]
            dx = knuckle[0] - wrist[0]
            dy = knuckle[1] - wrist[1]

            angle = math.degrees(math.atan2(dy, dx))

            now = time.time()
            if now - last_scroll_time > 1:
                if angle < -20:
                    print("Scroll Up")
                    pyautogui.scroll(500)
                    last_scroll_time = now
                elif angle > 20:
                    print("Scroll Down")
                    pyautogui.scroll(-500)
                    last_scroll_time = now

cv2.imshow("AirCursor", frame)
key = cv2.waitKey(1)
if key == 27:
    break
    cap.release()
cv2.destroyAllWindows(
