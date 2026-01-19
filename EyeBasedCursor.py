import cv2
import mediapipe as mp
import pyautogui
import time

screen_w, screen_h = pyautogui.size()

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x, prev_y = None, None
alpha = 0.4  
deadzone = 0.01
scroll_threshold = 0.03
click_cooldown = 0.8
last_click_time = 0
dragging = False

LEFT_EYE = [33, 133, 160, 159, 158, 144]
RIGHT_EYE = [362, 263, 387, 386, 385, 373]
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374

def get_eye_center(landmarks, indices):
    x = sum([landmarks[i].x for i in indices]) / len(indices)
    y = sum([landmarks[i].y for i in indices]) / len(indices)
    return x, y

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0].landmark

        eye_x, eye_y = get_eye_center(face_landmarks, LEFT_EYE)

        if prev_x is None:
            prev_x, prev_y = eye_x, eye_y

        dx = eye_x - prev_x
        dy = eye_y - prev_y

        if abs(dx) < deadzone:
            dx = 0
        if abs(dy) < deadzone:
            dy = 0

        smooth_x = prev_x + alpha * dx
        smooth_y = prev_y + alpha * dy
        prev_x, prev_y = smooth_x, smooth_y

        screen_x = int(smooth_x * screen_w)
        screen_y = int(smooth_y * screen_h)
        pyautogui.moveTo(screen_x, screen_y, _pause=False)

        left_eye_open = abs(face_landmarks[LEFT_EYE_TOP].y - face_landmarks[LEFT_EYE_BOTTOM].y)
        right_eye_open = abs(face_landmarks[RIGHT_EYE_TOP].y - face_landmarks[RIGHT_EYE_BOTTOM].y)

        if left_eye_open < 0.01 and right_eye_open > 0.015 and (time.time() - last_click_time) > click_cooldown:
            pyautogui.click()
            last_click_time = time.time()

        if right_eye_open < 0.01 and left_eye_open > 0.015 and (time.time() - last_click_time) > click_cooldown:
            pyautogui.rightClick()
            last_click_time = time.time()

        if dy > scroll_threshold:
            pyautogui.scroll(-50) 
        elif dy < -scroll_threshold:
            pyautogui.scroll(50)  

        cx, cy = int(smooth_x * w), int(smooth_y * h)
        cv2.circle(img, (cx, cy), 10, (0, 255, 0), -1)
        cv2.putText(img, f"Cursor: ({screen_x}, {screen_y})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(img, "Left blink = Left Click | Right blink = Right Click | Move eyes up/down = Scroll",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

    cv2.imshow("Eye-Controlled Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
