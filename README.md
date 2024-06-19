# images-to-timelapse

In summary, I want to:

1. filter out or fix corrupted photos in a batch
1. filter out photos that show night
1. adjust brightness of too dark photos to match the rest
1. create a video using remaining photos, one photo per frame
1. filter out parts of the video that show no activity on building of the house
1. set the length of the video to the exact value (like 1 second)

## Solution from ChatGPT

Yes, you can accomplish all of these tasks using a Python script. Here is a complete workflow using Python and relevant libraries such as OpenCV, NumPy, and `moviepy` to achieve each step:

### Step 1: Filter out or fix corrupted photos in a batch

We'll start by writing a function to detect and remove corrupted images:

```python
import cv2
import os
import numpy as np

def is_corrupted(image):
    try:
        unique_colors = len(np.unique(image.reshape(-1, image.shape[2]), axis=0))
        return unique_colors < 100
    except Exception as e:
        return True

def filter_corrupted_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        
        if img is not None and not is_corrupted(img):
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img)
        else:
            print(f"Corrupted image detected: {filename}")

input_folder = 'path_to_your_images_folder'
output_folder = 'path_to_filtered_images_folder'
filter_corrupted_images(input_folder, output_folder)
```

### Step 2: Filter out photos that show night

We'll write a function to detect and remove night images based on brightness:

```python
def is_night_image(image, brightness_threshold=50):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    return avg_brightness < brightness_threshold

def filter_night_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        
        if img is not None and not is_night_image(img):
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img)
        else:
            print(f"Night image detected: {filename}")

input_folder = 'path_to_filtered_images_folder'
output_folder = 'path_to_day_images_folder'
filter_night_images(input_folder, output_folder)
```

### Step 3: Adjust brightness of too dark photos to match the rest

We'll write a function to adjust the brightness of the images:

```python
def adjust_brightness(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def adjust_images_brightness(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        
        if img is not None:
            adjusted_img = adjust_brightness(img)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, adjusted_img)

input_folder = 'path_to_day_images_folder'
output_folder = 'path_to_brightness_adjusted_images_folder'
adjust_images_brightness(input_folder, output_folder)
```

### Step 4: Create a video using remaining photos, one photo per frame

We'll use `moviepy` to create a video from the images:

```python
from moviepy.editor import ImageSequenceClip

def create_video_from_images(input_folder, output_video_path, fps=1):
    image_files = [os.path.join(input_folder, img) for img in sorted(os.listdir(input_folder)) if img.endswith(".jpg")]
    clip = ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(output_video_path, codec="libx264")

input_folder = 'path_to_brightness_adjusted_images_folder'
output_video_path = 'output_video.mp4'
create_video_from_images(input_folder, output_video_path, fps=1)
```

### Step 5: Filter out parts of the video that show no activity on building of the house

We'll write a function to filter out static parts of the video based on frame differences:

```python
import cv2
import numpy as np

def frame_difference(frame1, frame2, threshold=30):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    return np.sum(thresh)

def filter_static_frames(video_path, output_path, change_threshold=10000):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    ret, prev_frame = cap.read()
    out.write(prev_frame)

    for _ in range(frame_count - 1):
        ret, curr_frame = cap.read()
        if ret:
            if frame_difference(prev_frame, curr_frame) > change_threshold:
                out.write(curr_frame)
            prev_frame = curr_frame

    cap.release()
    out.release()

video_path = 'output_video.mp4'
output_path = 'filtered_output_video.mp4'
filter_static_frames(video_path, output_path)
```

### Step 6: Set the length of the video to the exact value (like 1 second)

We'll use `moviepy` to trim or extend the video to the desired length:

```python
from moviepy.editor import VideoFileClip

def set_video_length(input_video_path, output_video_path, duration):
    clip = VideoFileClip(input_video_path)
    final_clip = clip.set_duration(duration)
    final_clip.write_videofile(output_video_path, codec="libx264")

input_video_path = 'filtered_output_video.mp4'
output_video_path = 'final_output_video.mp4'
duration = 1  # duration in seconds
set_video_length(input_video_path, output_video_path, duration)
```

### Putting It All Together

Here is the complete script that performs all the steps sequentially:

```python
import cv2
import os
import numpy as np
from moviepy.editor import ImageSequenceClip, VideoFileClip

def is_corrupted(image):
    try:
        unique_colors = len(np.unique(image.reshape(-1, image.shape[2]), axis=0))
        return unique_colors < 100
    except Exception as e:
        return True

def filter_corrupted_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        if img is not None and not is_corrupted(img):
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img)
        else:
            print(f"Corrupted image detected: {filename}")

def is_night_image(image, brightness_threshold=50):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    return avg_brightness < brightness_threshold

def filter_night_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        if img is not None and not is_night_image(img):
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, img)
        else:
            print(f"Night image detected: {filename}")

def adjust_brightness(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.equalizeHist(l)
    lab = cv2.merge((l, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def adjust_images_brightness(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            adjusted_img = adjust_brightness(img)
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, adjusted_img)

def create_video_from_images(input_folder, output_video_path, fps=1):
    image_files = [os.path.join(input_folder, img) for img in sorted(os.listdir(input_folder)) if img.endswith(".jpg")]
    clip = ImageSequenceClip(image_files, fps=fps)
    clip.write_videofile(output_video_path, codec="libx264")

def frame_difference(frame1, frame2, threshold=30):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    _, thresh =
