import math
import time
from ctypes import cast, POINTER

import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

import hand_tracker_module as htm

############################################################
wCam, hCam = 640, 480
############################################################


init_time = 0
curr_time = 0  # For FPS

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get volume range for mapping with gesture distance range
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

# Initial values
vol = 0
bar_val = 400
bar_prec = 0

while True:
    ret, img = cap.read()

    img = detector.find_Hands(img)
    lm_list = detector.find_Position(img, draw=False)

    if len(lm_list) != 0:
        # Landmark 4 and 8 indicate the positions of tip of thumb and tip of index finger respectively.
        x1, y1 = lm_list[4][1], lm_list[4][2]
        x2, y2 = lm_list[8][1], lm_list[8][2]

        xmid, ymid = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (xmid, ymid), 15, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)  # Get distance by which index and thumb fingers are apart

        # Based on Observations,
        # Range of distance between the two fingers is  25 to 250
        # Range of System Volume in pycaw is -6.5 to 0

        vol = np.interp(length, [25, 240], [min_vol, max_vol])
        bar_val = np.interp(length, [25, 250], [400, 150])
        bar_perc = np.interp(length, [25, 250], [0, 100])

        volume.SetMasterVolumeLevel(vol, None)

        if length < 26:
            cv2.circle(img, (xmid, ymid), 15, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(bar_val)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(bar_perc)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    curr_time = time.time()
    fps = 1 / (curr_time - init_time)
    init_time = curr_time
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cv2.imshow("image", img)

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
