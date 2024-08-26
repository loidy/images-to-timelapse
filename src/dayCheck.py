import os
import cv2
import numpy as np

def load_and_classify_images(img_folder):
    classified_images = {"day": [], "night": []}
    
    for root, dirs, files in os.walk(img_folder):
        for file in files:
            if file.endswith((".jpg", ".png")): 
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)
                
                if image is not None:
                    avg = avg_brightness(image)
                    
                    label = "day" if avg > 100 else "night" 
                    classified_images[label].append(image_path)
    
    return classified_images

def avg_brightness(rgb_image):
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
    sum_brightness = np.sum(hsv[:,:,2])
    area = rgb_image.shape[0] * rgb_image.shape[1]
    avg = sum_brightness / area
    return avg

img_folder = r"C:\Users\patri\OneDrive\Desktop\image_generator\jpg2"
classified_images = load_and_classify_images(img_folder)

print(f"Day images: {len(classified_images['day'])}")
print(f"Night images: {len(classified_images['night'])}")