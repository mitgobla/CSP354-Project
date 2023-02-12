"""
Emotion detection using OpenCV and SkiKit
Author: Benjamin Dodd (1901386)
"""

import cv2 as cv
from deepface import DeepFace

VIDEO_CAPTURE = cv.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = VIDEO_CAPTURE.read()

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    face_analyse = DeepFace.analyze(frame, actions = ['emotion'], enforce_detection=False, silent = True)[0]

    dominant_emotion = face_analyse['dominant_emotion']
    region = face_analyse['region']

    # Draw text showing emotion
    cv.putText(frame, dominant_emotion, (region['x'], region['y'] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    # Draw rectangle around the face showing emotion
    cv.rectangle(frame, (region['x'], region['y']), (region['x'] + region['w'], region['y'] + region['h']), (255, 0, 0), 2)

    # Display the resulting frame
    cv.imshow('Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

VIDEO_CAPTURE.release()
cv.destroyAllWindows()
