import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

input_folder = r"C:\Users\patri\OneDrive\Desktop\image_generator\2024-01-20\001\jpg\test"

def detect_saturation(image, saturation_threshold=20):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    print(s.max())
    return s.max() <= saturation_threshold

def walkdir(folder):
    """Walk through every files in a directory"""
    for dirpath, dirs, files in os.walk(folder):
        for filename in files:
            yield os.path.join(dirpath, filename)

night_images = 0
day_images = 0
for filepath in tqdm([filepath for filepath in walkdir(input_folder) if filepath.endswith('.jpg')]):
    img = cv2.imread(filepath)

    if 'jpg/02/15' in filepath:
        print(filepath)
        plt.imshow(img)
        plt.show()
    if img is not None and detect_saturation(img):
        night_images += 1
    else:
        day_images += 1
        print(f"Day image: {filepath}")

print(f'{night_images} night images detected over {night_images + day_images}')