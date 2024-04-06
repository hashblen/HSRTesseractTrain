import pytesseract
import os
import json
from PIL import Image
import Levenshtein
pytesseract.pytesseract.tesseract_cmd = "assets/tesseract/tesseract.exe"
img_dir = "images"
json_name = 'achievement_processed_data.json'

config = f'--psm 7 -l hsr3'

cnt_exact = 0
cnt_not = 0

for filename in os.listdir(img_dir):
    if filename.endswith(".png"):
        path = os.path.join(img_dir, filename)
        print(path)
        with Image.open(path) as img:
            readStr = pytesseract.image_to_string(img, config=config).replace("\n", " ").strip()
        with open(path[:-4]+".gt.txt", 'r', encoding='utf-8') as file:
            name = file.readline().strip()
        if name == readStr:
            cnt_exact += 1
            print("EXACT MATCH")
        else:
            print("----")
            print("Read:\t", readStr)
            print("Grnd:\t", name)
            cnt_not += 1
            print("----")

print("Exact:", cnt_exact, "Not:", cnt_not)