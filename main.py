import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

class GestureVerse:
    def __init__(self, max_hands=2):
        self.cap = cv2.VideoCapture(0)
        self.drawing = mp.solutions.drawing_utils
        self.hands = mp.solutions.hands.Hands(max_num_hands=max_hands)
        self.mode = 'media'  # Default mode
        self.screen_width, self.screen_height = pyautogui.size()
        self.last_action_time = 0
        self.action_delay = 0.5  # Reduced delay to 0.5 seconds
        self.frame_count = 0
        self.fps_start_time = time.time()
        self.last_finger_count = None
        self.paint_init()

    def paint_init(self):
        self.ml = 150
        self.max_x, self.max_y = 250 + self.ml, 50
        self.curr_tool = "select tool"
        self.time_init = True
        self.rad = 40
        self.var_inits = False
        self.thick = 4
        self.prevx, self.prevy = 0, 0
        self.tools = cv2.imread("tools.png").astype('uint8')
        self.mask = np.ones((480, 640)) * 255
        self.mask = self.mask.astype('uint8')

    def count_fingers(self, hand_landmarks):
        cnt = 0
        thresh = (hand_landmarks.landmark[0].y * 100 - hand_landmarks.landmark[9].y * 100) / 2

        if (hand_landmarks.landmark[5].y * 100 - hand_landmarks.landmark[8].y * 100) > thresh:
            cnt += 1

        if (hand_landmarks.landmark[9].y * 100 - hand_landmarks.landmark[12].y * 100) > thresh:
            cnt += 1

        if (hand_landmarks.landmark[13].y * 100 - hand_landmarks.landmark[16].y * 100) > thresh:
            cnt += 1

        if (hand_landmarks.landmark[17].y * 100 - hand_landmarks.landmark[20].y * 100) > thresh:
            cnt += 1

        if (hand_landmarks.landmark[5].x * 100 - hand_landmarks.landmark[4].x * 100) > 6:
            cnt += 1

        return cnt

    def fingers_status(self, hand_landmarks):
        status = [False] * 5
        thresh = (hand_landmarks.landmark[0].y * 100 - hand_landmarks.landmark[9].y * 100) / 2

        status[0] = (hand_landmarks.landmark[5].y * 100 - hand_landmarks.landmark[8].y * 100) > thresh
        status[1] = (hand_landmarks.landmark[9].y * 100 - hand_landmarks.landmark[12].y * 100) > thresh
        status[2] = (hand_landmarks.landmark[13].y * 100 - hand_landmarks.landmark[16].y * 100) > thresh
        status[3] = (hand_landmarks.landmark[17].y * 100 - hand_landmarks.landmark[20].y * 100) > thresh
        status[4] = (hand_landmarks.landmark[5].x * 100 - hand_landmarks.landmark[4].x * 100) > 6

        return status

    def switch_mode(self, count):
        modes = ['media', 'ppt', 'virtual_mouse', 'painter']
        if count <= len(modes):
            self.mode = modes[count - 1]

    def control_media(self, count):
        current_time = time.time()
        if current_time - self.last_action_time > self.action_delay and count != self.last_finger_count:
            if count == 1:
                pyautogui.press("right")
                print('pressed : right')
            elif count == 2:
                pyautogui.press("left")
                print('pressed : left')
            elif count == 3:
                pyautogui.press("up")
                print('pressed : up')
            elif count == 4:
                pyautogui.press("down")
                print('pressed : down')
            elif count == 5:
                pyautogui.press("space")
                print('pressed : space')
            self.last_action_time = current_time
            self.last_finger_count = count

    def control_ppt(self, count):
        current_time = time.time()
        if current_time - self.last_action_time > self.action_delay and count != self.last_finger_count:
            if count == 1:
                pyautogui.press("right")
                print('pressed right')
            elif count == 2:
                pyautogui.press("left")
                print('pressed left')
            self.last_action_time = current_time
            self.last_finger_count = count

    def control_virtual_mouse(self, hand_landmarks):
        fingers = self.fingers_status(hand_landmarks)
        index_finger_tip = hand_landmarks.landmark[8]
        middle_finger_tip = hand_landmarks.landmark[12]

        # Move mouse if index and middle finger are up and others are closed
        if fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
            x = int(index_finger_tip.x * self.screen_width)
            y = int(index_finger_tip.y * self.screen_height)
            pyautogui.moveTo(x, y)

        # Stop mouse if thumb is also up
        if fingers[0] and fingers[1] and fingers[4]:
            return

        current_time = time.time()

        # Right click if index finger is half closed
        if fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
            if abs(index_finger_tip.y - hand_landmarks.landmark[7].y) < 0.05:
                if current_time - self.last_action_time > self.action_delay:
                    print("Right click detected")
                    pyautogui.rightClick()
                    self.last_action_time = current_time

        # Left click if middle finger is half closed
        if fingers[1] and not fingers[0] and not fingers[2] and not fingers[3] and not fingers[4]:
            if abs(middle_finger_tip.y - hand_landmarks.landmark[11].y) < 0.05:
                if current_time - self.last_action_time > self.action_delay:
                    print("Left click detected")
                    pyautogui.click()
                    self.last_action_time = current_time

    def control_painter(self, hand_landmarks):
        x, y = int(hand_landmarks.landmark[8].x * 640), int(hand_landmarks.landmark[8].y * 480)

        if x < self.max_x and y < self.max_y and x > self.ml:
            if self.time_init:
                self.ctime = time.time()
                self.time_init = False
            self.ptime = time.time()

            cv2.circle(self.frame, (x, y), self.rad, (0, 255, 255), 2)
            self.rad -= 1

            if (self.ptime - self.ctime) > 0.8:
                self.curr_tool = self.getTool(x)
                print("your current tool set to : ", self.curr_tool)
                self.time_init = True
                self.rad = 40

        else:
            self.time_init = True
            self.rad = 40

        if self.curr_tool == "draw":
            xi, yi = int(hand_landmarks.landmark[12].x * 640), int(hand_landmarks.landmark[12].y * 480)
            y9 = int(hand_landmarks.landmark[9].y * 480)

            if self.index_raised(yi, y9):
                cv2.line(self.mask, (self.prevx, self.prevy), (x, y), 0, self.thick)
                self.prevx, self.prevy = x, y
            else:
                self.prevx = x
                self.prevy = y

        elif self.curr_tool == "line":
            xi, yi = int(hand_landmarks.landmark[12].x * 640), int(hand_landmarks.landmark[12].y * 480)
            y9 = int(hand_landmarks.landmark[9].y * 480)

            if self.index_raised(yi, y9):
                if not self.var_inits:
                    self.xii, self.yii = x, y
                    self.var_inits = True

                cv2.line(self.frame, (self.xii, self.yii), (x, y), (50, 152, 255), self.thick)
            else:
                if self.var_inits:
                    cv2.line(self.mask, (self.xii, self.yii), (x, y), 0, self.thick)
                    self.var_inits = False

        elif self.curr_tool == "rectangle":
            xi, yi = int(hand_landmarks.landmark[12].x * 640), int(hand_landmarks.landmark[12].y * 480)
            y9 = int(hand_landmarks.landmark[9].y * 480)

            if self.index_raised(yi, y9):
                if not self.var_inits:
                    self.xii, self.yii = x, y
                    self.var_inits = True

                cv2.rectangle(self.frame, (self.xii, self.yii), (x, y), (0, 255, 255), self.thick)
            else:
                if self.var_inits:
                    cv2.rectangle(self.mask, (self.xii, self.yii), (self.xii, self.yii), (x, y), 0, self.thick)
                    self.var_inits = False

        elif self.curr_tool == "circle":
            xi, yi = int(hand_landmarks.landmark[12].x * 640), int(hand_landmarks.landmark[12].y * 480)
            y9 = int(hand_landmarks.landmark[9].y * 480)

            if self.index_raised(yi, y9):
                if not self.var_inits:
                    self.xii, self.yii = x, y
                    self.var_inits = True

                radius = int(((self.xii - x) ** 2 + (self.yii - y) ** 2) ** 0.5)
                cv2.circle(self.frame, (self.xii, self.yii), radius, (255, 255, 0), self.thick)
            else:
                if self.var_inits:
                    radius = int(((self.xii - x) ** 2 + (self.yii - y) ** 2) ** 0.5)
                    cv2.circle(self.mask, (self.xii, self.yii), radius, 0, self.thick)
                    self.var_inits = False

        elif self.curr_tool == "erase":
            xi, yi = int(hand_landmarks.landmark[12].x * 640), int(hand_landmarks.landmark[12].y * 480)
            y9 = int(hand_landmarks.landmark[9].y * 480)

            if self.index_raised(yi, y9):
                cv2.circle(self.frame, (x, y), 30, (0, 0, 0), -1)
                cv2.circle(self.mask, (x, y), 30, 255, -1)



    def getTool(self, x):
        if x < 50 + self.ml:
            return "line"
        elif x < 100 + self.ml:
            return "rectangle"
        elif x < 150 + self.ml:
            return "draw"
        elif x < 200 + self.ml:
            return "circle"
        else:
            return "erase"

    def index_raised(self, yi, y9):
        return (y9 - yi) > 40

    def run(self):
        while True:
            _, self.frame = self.cap.read()
            self.frame = cv2.flip(self.frame, 1)
            self.frame_count += 1

            result = self.hands.process(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))

            if result.multi_hand_landmarks:
                for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                    handedness = hand_handedness.classification[0].label

                    if handedness == 'Right':
                        finger_count = self.count_fingers(hand_landmarks)

                        if self.mode == 'media':
                            self.control_media(finger_count)
                        elif self.mode == 'virtual_mouse':
                            self.control_virtual_mouse(hand_landmarks)
                        elif self.mode == 'ppt':
                            self.control_ppt(finger_count)
                        elif self.mode == 'painter':
                            self.control_painter(hand_landmarks)

                    elif handedness == 'Left':
                        finger_count = self.count_fingers(hand_landmarks)
                        self.switch_mode(finger_count)

                    self.drawing.draw_landmarks(self.frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            # Display FPS and mode
            fps_end_time = time.time()
            fps = self.frame_count / (fps_end_time - self.fps_start_time)
            cv2.putText(self.frame, f"Mode: {self.mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(self.frame, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Apply mask to frame
            op = cv2.bitwise_and(self.frame, self.frame, mask=self.mask)
            self.frame[:, :, 1] = op[:, :, 1]
            self.frame[:, :, 2] = op[:, :, 2]

            # Overlay tools
            # self.frame[:self.max_y, self.ml:self.max_x] = cv2.addWeighted(self.tools, 0.7, self.frame[:self.max_y, self.ml:self.max_x], 0.3, 0)
            
                        # Before displaying the frame, add this check:
            if self.mode == 'painter':
                self.frame[:self.max_y, self.ml:self.max_x] = cv2.addWeighted(self.tools, 0.7, self.frame[:self.max_y, self.ml:self.max_x], 0.3, 0)
                cv2.putText(self.frame, self.curr_tool, (270 + self.ml, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Hand Gesture Recognition", self.frame)

            if cv2.waitKey(1) == 27:
                cv2.destroyAllWindows()
                self.cap.release()
                break

if __name__ == "__main__":
    gv = GestureVerse()
    gv.run()

