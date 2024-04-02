import pytesseract
import os
import json
from PIL import Image
import Levenshtein
pytesseract.pytesseract.tesseract_cmd = "assets/tesseract/tesseract.exe"
img_dir = "images"
json_name = 'achievement_processed_data.json'

config = f'--psm 7 -l DIN-Alternate'

import cv2
import numpy as np

img = Image.open("130728501911.png")
d = pytesseract.image_to_boxes(img, config=config+" -c tessedit_create_boxfile=1", output_type=pytesseract.Output.DICT)

frame = np.array(img)
frame = frame[:, :, ::-1].copy()
height, width = frame.shape[:2]

n_boxes = len(d['char'])
for i in range(n_boxes):
	(x, y, a, b) = (d['left'][i], d['top'][i], d['right'][i], d['bottom'][i])
	frame = cv2.rectangle(frame, (x, height-y), (a, height-b), (0, 255, 0), 1)

frame_with_text = frame.copy()
detected = pytesseract.image_to_string(img, config=config)
print(detected)
# frame_with_text = cv2.putText(frame_with_text, detected_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

import matplotlib.pyplot as plt
plt.imshow(cv2.cvtColor(frame_with_text, cv2.COLOR_BGR2RGB))
plt.show()
# cv2.imshow("abc", frame_with_text)
# cv2.waitKey(20)