# import os
# import cv2
# import numpy as np
# from tqdm import tqdm

# def load_and_classify_images(base_dir):
#     classified_images = {"day": [], "night": []}
    
#     for root, dirs, files in os.walk(base_dir):
#         for file in files:
#             if file.endswith((".jpg", ".png")):  # Adjust extensions as needed
#                 image_path = os.path.join(root, file)
#                 image = cv2.imread(image_path)
                
#                 # Check if the image was successfully loaded
#                 if image is not None:
#                     avg = avg_brightness(image)
                    
#                     # Adjust threshold if necessary
#                     label = "day" if avg > 100 else "night"  # Example threshold
#                     classified_images[label].append(image_path)
    
#     return classified_images

# def avg_brightness(rgb_image):
#     hsv = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
#     sum_brightness = np.sum(hsv[:,:,2])
#     area = rgb_image.shape[0] * rgb_image.shape[1]
#     avg = sum_brightness / area
#     return avg

# def load_images_for_timelapse(image_paths):
#     images = []
#     for img_path in image_paths:
#         img = cv2.imread(img_path)
#         if img is not None and img.size > 0:
#             images.append(img)
#             print(f"Loaded image: {img_path}")
#         else:
#             print(f"Warning: Invalid image file found and skipped: {img_path}")
#     return images

# def create_timelapse(images, output_file, fps=300):
#     if not images:
#         print("No images to create a timelapse.")
#         return
    
#     height, width, layers = images[0].shape
#     size = (width, height)
#     out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    
#     for img in tqdm(images, desc="Creating timelapse"):
#         out.write(img)
#     out.release()


# # Example usage
# base_dir = r"C:\Users\patri\OneDrive\Desktop\image_generator\jpg\8"
# output_file = 'day_timelapse.avi'

# # Load and classify images
# print("Classifying images...")
# classified_images = load_and_classify_images(base_dir)

# # Load day images for timelapse
# print(f"Loading {len(classified_images['day'])} day images for timelapse...")
# day_images = load_images_for_timelapse(classified_images['day'])

# # Create timelapse video
# print("Creating timelapse video...")
# create_timelapse(day_images, output_file)
# print(f"Timelapse video saved as {output_file}.")

import os
import cv2
import numpy as np

def load_and_classify_images(base_dir):
    classified_images = {"day": [], "night": []}
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith((".jpg", ".png")):  # Adjust extensions as needed
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)
                
                # Check if the image was successfully loaded
                if image is not None:
                    avg = avg_brightness(image)
                    
                    # Adjust threshold if necessary
                    label = "day" if avg > 100 else "night"  # Example threshold
                    classified_images[label].append(image_path)
    
    return classified_images

def avg_brightness(rgb_image):
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)
    sum_brightness = np.sum(hsv[:,:,2])
    area = rgb_image.shape[0] * rgb_image.shape[1]
    avg = sum_brightness / area
    return avg

# Example usage
base_dir = r"C:\Users\patri\OneDrive\Desktop\image_generator\jpg2\20"
classified_images = load_and_classify_images(base_dir)

# Now `classified_images` contains paths to day and night images
print(f"Day images: {len(classified_images['day'])}")
print(f"Night images: {len(classified_images['night'])}")