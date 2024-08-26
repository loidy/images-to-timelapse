import os

def filter_images_by_hour(base_dir):
    selected_images = []

    valid_hours = [f'{hour:02d}' for hour in range(8, 17)]  # Hours 08 to 16
    
    for hour in valid_hours:
        hour_dir = os.path.join(base_dir, hour)
        if os.path.isdir(hour_dir):
            for minute in os.listdir(hour_dir):
                minute_dir = os.path.join(hour_dir, minute)
                if os.path.isdir(minute_dir):
                    for file in os.listdir(minute_dir):
                        if file.endswith('.jpg'):
                            img_path = os.path.join(minute_dir, file)
                            selected_images.append(img_path)
    
    return selected_images

day_folder = r"C:\Users\patri\OneDrive\Desktop\image_generator\2023-03-27\001\jpg"
filtered_images = filter_images_by_hour(day_folder)

print(f"Total selected images: {len(filtered_images)}")