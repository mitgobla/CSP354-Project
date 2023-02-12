"""
Gesture detection using MediaPipe
Author: Benjamin Dodd (1901386)
"""

import cv2 as cv
import mediapipe as mp


MP_DRAWING = mp.solutions.drawing_utils
MP_DRAWING_STYLES = mp.solutions.drawing_styles
MP_HANDS = mp.solutions.hands

VIDEO_CAPTURE = cv.VideoCapture(0)
VIDEO_CAPTURE.set(cv.CAP_PROP_FPS, 60)


with MP_HANDS.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while VIDEO_CAPTURE.isOpened():
        success, image = VIDEO_CAPTURE.read()
        if not success:
            # Skip processing as the frame was not captured
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv.cvtColor(cv.flip(image, 1), cv.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            finger_count = 0
            last_index_x, last_index_y = 0, 0
            for hand_landmarks in results.multi_hand_landmarks:
                # print(
                #     'Index finger tip coordinates: (',
                #     f'{hand_landmarks.landmark[MP_HANDS.HandLandmark.INDEX_FINGER_TIP].x * image.shape[0]}, '
                #     f'{hand_landmarks.landmark[MP_HANDS.HandLandmark.INDEX_FINGER_TIP].y * image.shape[1]})'
                # )
                last_index_x = hand_landmarks.landmark[MP_HANDS.HandLandmark.INDEX_FINGER_TIP].x * image.shape[0]
                last_index_y = hand_landmarks.landmark[MP_HANDS.HandLandmark.INDEX_FINGER_TIP].y * image.shape[1]
                if hand_landmarks.landmark[MP_HANDS.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[MP_HANDS.HandLandmark.INDEX_FINGER_DIP].y:
                    finger_count += 1

                if hand_landmarks.landmark[MP_HANDS.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[MP_HANDS.HandLandmark.MIDDLE_FINGER_DIP].y:
                    finger_count += 1

                if hand_landmarks.landmark[MP_HANDS.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[MP_HANDS.HandLandmark.RING_FINGER_DIP].y:
                    finger_count += 1

                if hand_landmarks.landmark[MP_HANDS.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[MP_HANDS.HandLandmark.PINKY_DIP].y:
                    finger_count += 1

                MP_DRAWING.draw_landmarks(
                    image=image,
                    landmark_list=hand_landmarks,
                    connections=MP_HANDS.HAND_CONNECTIONS,
                    landmark_drawing_spec=MP_DRAWING_STYLES.get_default_hand_landmarks_style(),
                    connection_drawing_spec=MP_DRAWING_STYLES.get_default_hand_connections_style())
            cv.putText(image, str(f"You are holding up {finger_count} digits"), (int(last_index_x), int(last_index_y)-20), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        cv.imshow('Hands', image)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
