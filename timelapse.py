import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def classify_day_or_night(night_photo_path, img_path, similarity_threshold=0.95):
    try:
        night_photo = cv2.imread(night_photo_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if night_photo is None or img is None:
            return "Error: Unable to load images"

        size = (300, 300)
        night_photo = cv2.resize(night_photo, size)  # Adjust size as needed
        img = cv2.resize(img, size)  # Adjust size as needed

        ssim_index, _ = ssim(night_photo, img, full=True)

        if ssim_index >= similarity_threshold:
            return "Night (similar to reference night photo)"
        else:
            return "Day (not similar to reference night photo)"

    except Exception as e:
        return f"Error: {e}"

def is_valid_image(img):
    """Check if the image is valid by ensuring it is not None and has a valid shape."""
    return img is not None and img.size > 0

def load_images_from_nested_folders(folder, night_photo_path, similarity_threshold=0.95):
    images = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.jpg'): 
                img_path = os.path.join(root, file)
                try:
                    classification_result = classify_day_or_night(night_photo_path, img_path, similarity_threshold)
                    print(f"Classified {img_path} as {classification_result}")
                    if classification_result == "Day (not similar to reference night photo)":
                        img = cv2.imread(img_path)
                        if is_valid_image(img):
                            images.append(img)
                            print(f"Loaded day image: {img_path}")
                        else:
                            print(f"Warning: Invalid image file found and skipped: {img_path}")
                    else:
                        print(f"Skipped night image: {img_path}")
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")
    return images

def create_timelapse(images, output_file, fps=30):
    if not images:
        print("No images to create a timelapse.")
        return
    height, width, layers = images[0].shape
    size = (width, height)
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    
    for img in images:
        out.write(img)
    out.release()

# Paths and settings
folder_path = "path/to/images"
night_photo_path = "path/to/night_photo"
output_file = 'timelapse.avi'
similarity_threshold = 0.95 

# Load images
images = load_images_from_nested_folders(folder_path, night_photo_path, similarity_threshold)
print(f"Loaded {len(images)} day images.")

# Create timelapse
create_timelapse(images, output_file)
print(f"Timelapse video saved as {output_file}.")
