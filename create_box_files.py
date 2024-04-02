import pytesseract
import os
import json
from PIL import Image
import Levenshtein
import unicodedata
pytesseract.pytesseract.tesseract_cmd = "assets/tesseract/tesseract.exe"
img_dir = "images"
json_name = 'achievement_processed_data.json'

config = f'--psm 7 -l DIN-Alternate'

"""img = Image.open("130728501911.png")
d = pytesseract.image_to_boxes(img, config=config+" -c tessedit_create_boxfile=1", output_type=pytesseract.Output.DICT)
d2 = pytesseract.image_to_boxes(img, config=config+" -c tessedit_create_boxfile=1")
width, height = img.size
mini_x = min(d["left"])
maxi_x = max(d["right"])
mini_y = min(d["bottom"])
maxi_y = max(d["top"])
print(d2 + f'\t {mini_x} {mini_y} {maxi_x} {maxi_y} 0')"""


for filename in os.listdir(img_dir):
    if filename.endswith(".png"):
        path = os.path.join(img_dir, filename)
        print(path)
        with Image.open(path) as img:
            d = pytesseract.image_to_boxes(img, config=config+" -c tessedit_create_boxfile=1", output_type=pytesseract.Output.DICT)
            d2 = pytesseract.image_to_boxes(img, config=config+" -c tessedit_create_boxfile=1")
        mini_x = min(d["left"])
        maxi_x = max(d["right"])
        mini_y = min(d["bottom"])
        maxi_y = max(d["top"])
        print(f'\t {mini_x} {mini_y} {maxi_x} {maxi_y} 0')
        with open(path[:-4]+".gt.txt", 'r', encoding='utf-8') as file:
            name = file.readline().strip()
            line = unicodedata.normalize('NFC', name)
        width, height = img.size
        with open(path[:-4]+".box", 'w', encoding='utf-8') as file:
            for i in range(1, len(line)):
                char = line[i]
                prev_char = line[i - 1]
                if unicodedata.combining(char):
                    file.write('%s 0 0 %d %d 0\n' % ((prev_char + char), width, height))
                elif not unicodedata.combining(prev_char):
                    file.write('%s 0 0 %d %d 0\n' % (prev_char, width, height))
            if not unicodedata.combining(line[-1]):
                file.write('%s 0 0 %d %d 0\n' % (line[-1], width, height))
                
            file.write(f'\t {mini_x} {mini_y} {maxi_x} {maxi_y} 0\n')
