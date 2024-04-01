import pytesseract
import os
import json
from PIL import Image
import Levenshtein
pytesseract.pytesseract.tesseract_cmd = "assets/tesseract/tesseract.exe"
img_dir = "images"
json_name = 'achievement_processed_data.json'

config = f'--psm 7 -l DIN-Alternate'

with open(json_name, 'r', encoding='utf-8') as proc_data_file:
    data = json.load(proc_data_file)


def get_closest_name_match(name_from_image: str):
    maxCost = 0.
    maxName = ""
    maxId = -1
    for c_id in data.keys():
        chiveName = data[c_id]["title"]
        cost = Levenshtein.ratio(name_from_image, chiveName)
        if cost > maxCost:
            maxCost = cost
            maxName = chiveName
            maxId = c_id
    if maxCost < 0.5:
        raise ValueError("No close match")
    return maxName, maxId


for filename in os.listdir(img_dir):
    if filename.endswith(".png"):
        path = os.path.join(img_dir, filename)
        print(path)
        with Image.open(path) as img:
            readStr = pytesseract.image_to_string(img, config=config).replace("\n", " ").strip()
        print("Read:\t", readStr)
        name = get_closest_name_match(readStr)[0]
        print("Found:\t", name)
        with open(path[:-4]+".gt.txt", 'w', encoding='utf-8') as file:
            file.write(name)
