import cv2
import numpy as np
import os

cap = cv2.VideoCapture("Pedro.mp4")
idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    print("Frame", idx)
    idx += 1
cap.release()