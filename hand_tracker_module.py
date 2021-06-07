import time

import cv2
import mediapipe as mp


class HandDetector():
    def __init__(self, mode=False, maxHands=2, detect_confidence=0.7, track_confidence=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detect_confidence = detect_confidence
        self.track_confidence = track_confidence
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.maxHands, self.detect_confidence,
                                         self.track_confidence)  # static_img param is False by default
        self.mp_draw = mp.solutions.drawing_utils

    def find_Hands(self, img, draw=True):
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_img)

        # Make sure something is detected
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            # Extract individually if multiple hands present
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    # use builtin mediapipe fn to plot landmarks on image
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def find_Position(self, img, handId=0, draw=True):
        '''
        Returns list of x,y coordinates of landmarks for a particular hand
        '''
        lm_list = []
        if self.results.multi_hand_landmarks:
            # Access using hand id
            hand_obj = self.results.multi_hand_landmarks[handId]
            # Get each landmark
            for id, lm in enumerate(hand_obj.landmark):
                # landmarks coords must be converted from ratio to absolute values of img dimensions
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id,cx,cy)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
        return lm_list


def main():
    init_time = 0
    curr_time = 0

    cap = cv2.VideoCapture(0)

    detector = HandDetector()
    while True:
        ret, img = cap.read()

        img = detector.find_Hands(img)
        lm_list = detector.find_Position(img)

        if len(lm_list) != 0:
            print(lm_list[4])  # for tip of thumb

        curr_time = time.time()
        fps = 1 / (curr_time - init_time)
        init_time = curr_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
