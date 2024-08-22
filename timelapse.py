import os
import cv2
from tqdm import tqdm

def is_valid_image(img):
    """Check if the image is valid by ensuring it is not None and has a valid shape."""
    return img is not None and img.size > 0

def load_images_from_nested_folders(folder):
    images = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.jpg'):  # Ensure it's a JPG file
                img_path = os.path.join(root, file)
                try:
                    img = cv2.imread(img_path)
                    if is_valid_image(img):
                        images.append(img)
                        print(f"Loaded image: {img_path}")
                    else:
                        print(f"Warning: Invalid image file found and skipped: {img_path}")
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

# Update this path to the root folder containing your images
folder_path = r"C:\Users\patri\OneDrive\Desktop\image_generator\2024-01-20\001\jpg\00"
output_file = 'timelapse.avi'

# Load images
print("Loading images...")
images = load_images_from_nested_folders(folder_path)
print(f"Loaded {len(images)} images.")

# Create timelapse video
print("Creating timelapse video...")
create_timelapse(images, output_file)
print(f"Timelapse video saved as {output_file}.")