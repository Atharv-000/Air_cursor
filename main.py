import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Webcam
cap = cv2.VideoCapture(0)

# Screen Size
screen_w, screen_h = pyautogui.size()

def get_landmarks(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    return result

def is_fist(lm):
    """Return True if all fingers are folded (fist)."""
    return (
        lm[8].y > lm[6].y and   # Index tip below knuckle
        lm[12].y > lm[10].y and # Middle tip below knuckle
        lm[16].y > lm[14].y and # Ring tip below knuckle
        lm[20].y > lm[18].y     # Pinky tip below knuckle
    )

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    result = get_landmarks(frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            # Cursor position (Index tip)
            x, y = int(lm[8].x * w), int(lm[8].y * h)
            screen_x, screen_y = screen_w / w * x, screen_h / h * y
            pyautogui.moveTo(screen_x, screen_y)

            # Coordinates for thumb, index, and middle
            thumb_x, thumb_y = int(lm[4].x * w), int(lm[4].y * h)
            index_x, index_y = int(lm[8].x * w), int(lm[8].y * h)
            middle_x, middle_y = int(lm[12].x * w), int(lm[12].y * h)

            # Left Click (Thumb + Index close)
            if abs(index_x - thumb_x) < 40 and abs(index_y - thumb_y) < 40:
                pyautogui.click()
                pyautogui.sleep(0.25)

            # Right Click (Thumb + Middle close)
            if abs(middle_x - thumb_x) < 40 and abs(middle_y - thumb_y) < 40:
                pyautogui.rightClick()
                pyautogui.sleep(0.25)

            # YES Gesture (Index + Middle raised up)
            if lm[8].y < lm[6].y and lm[12].y < lm[10].y:
                cv2.putText(frame, "YES GESTURE!", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            # Detect Fist
            if is_fist(lm):
                wrist_y = lm[0].y
                middle_knuckle_y = lm[9].y

                if wrist_y > middle_knuckle_y:  # Hand facing up
                    pyautogui.scroll(50)  # Scroll up
                    cv2.putText(frame, "SCROLL UP", (50, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

                else:  # Hand facing down
                    pyautogui.scroll(-50)  # Scroll down
                    cv2.putText(frame, "SCROLL DOWN", (50, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    # Show camera window
    cv2.imshow("AirCursor - Virtual Mouse", frame)

    # Exit on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

