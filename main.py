import os
import sys

import cv2
import mediapipe as mp

from audio_generation import *

# creating the detector and initializing the mixer
handsDetector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
mixer.init()
frame_size = (960, 720)
lowest_pitch = 110

while (cap.isOpened()):
    try:
        ret, frame = cap.read()
        if cv2.waitKey(1) & 0xFF == ord('q') or not ret:
            break
        flipped = np.fliplr(frame)
        # converting into RGB for detection
        flippedRGB = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
        flippedRGB = cv2.resize(flippedRGB, frame_size, interpolation=cv2.INTER_AREA)
        # detecting hands
        results = handsDetector.process(flippedRGB)
        # drawing the index finger fingertips
        if results.multi_hand_landmarks is not None:
            if len(results.multi_hand_landmarks) >= 2:
                hands_number = 2
                # multiplying by the frame's size
                x_tip_1 = int(results.multi_hand_landmarks[0].landmark[8].x *
                              flippedRGB.shape[1])
                y_tip_1 = int(results.multi_hand_landmarks[0].landmark[8].y *
                              flippedRGB.shape[0])
                cv2.circle(flippedRGB, (x_tip_1, y_tip_1), 3, (255, 0, 0), -1)
                x_tip_2 = int(results.multi_hand_landmarks[1].landmark[8].x *
                              flippedRGB.shape[1])
                y_tip_2 = int(results.multi_hand_landmarks[1].landmark[8].y *
                              flippedRGB.shape[0])
                cv2.circle(flippedRGB, (x_tip_2, y_tip_2), 3, (255, 0, 0), -1)

            elif len(results.multi_hand_landmarks) >= 1:
                hands_number = 1
                # multiplying by the frame's size
                x_tip_1 = int(results.multi_hand_landmarks[0].landmark[8].x *
                              flippedRGB.shape[1])
                y_tip_1 = int(results.multi_hand_landmarks[0].landmark[8].y *
                              flippedRGB.shape[0])
                cv2.circle(flippedRGB, (x_tip_1, y_tip_1), 3, (255, 0, 0), -1)
        else:
            hands_number = 0

        # converting back to BGR, drawing lines and text
        res_image = cv2.cvtColor(flippedRGB, cv2.COLOR_RGB2BGR)
        res_image = cv2.resize(res_image, frame_size, interpolation=cv2.INTER_AREA)
        res_image = cv2.line(res_image, (frame_size[0] // 2, 0), (frame_size[0] // 2, frame_size[1]), (64, 255, 64), 2)
        cv2.putText(res_image, 'Pitch', (50 + frame_size[0] // 2, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    frame_size[0] / 1440, (64, 255, 64), 1, cv2.LINE_AA)
        res_image = cv2.line(res_image, (0, 3 * frame_size[1] // 4), (frame_size[0] // 2, 3 * frame_size[1] // 4), (64, 255,
                                                                                                                    64), 2)
        cv2.putText(res_image, 'Volume', (30, 3 * frame_size[1] // 4 + 50), cv2.FONT_HERSHEY_SIMPLEX,
                    frame_size[0] / 1440, (64, 255, 64), 1, cv2.LINE_AA)

        if hands_number < 2:
            # if less than two hands are detected, showing reminder to show them
            cv2.putText(res_image, 'Two hands must be visible in the picture', (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        frame_size[0] / 1440, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            # if hand number one is more to the right than hand number 2
            if x_tip_1 > x_tip_2:
                # finding the frequency and volume of the sound
                if x_tip_1 != frame_size[0] // 2:
                    pitch = frame_size[0] // 2 / (x_tip_1 - frame_size[0] // 2) * lowest_pitch
                    if pitch < 0:
                        volume = 0
                    else:
                        volume = max((3 * frame_size[1] // 4 - y_tip_2) / (3 * frame_size[1] // 4), 0)
                else:
                    pitch = 0
                    volume = 0
            else:
                # finding the frequency and volume of the sound
                if x_tip_2 != frame_size[0] // 2:
                    pitch = frame_size[0] // 2 / (x_tip_2 - frame_size[0] // 2) * lowest_pitch
                    if pitch < 0:
                        volume = 0
                    else:
                        volume = max((3 * frame_size[1] // 4 - y_tip_1) / (3 * frame_size[1] // 4), 0)
                else:
                    pitch = 0
                    volume = 0
            # generating and playing the audio
            generate(pitch, volume)
        # showing the picture
        cv2.imshow("CV Theremin", res_image)
    except KeyboardInterrupt:
        break

# closing and deleting unnecessary things
if os.path.exists('sound.wav'):
    os.remove('sound.wav')
handsDetector.close()
