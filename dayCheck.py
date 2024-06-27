import cv2
import pytesseract
from pytesseract import Output

# Set the path to the Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_datetime_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    cropped = gray[0:int(h*0.1), int(w*0.75):w]
    cropped = cv2.threshold(cropped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    config = '--psm 6' 
    text = pytesseract.image_to_string(cropped, config=config)

    return text.strip()

if __name__ == "__main__":
    image_path = "path/to/image"
    extracted_text = extract_datetime_from_image(image_path)
    print(f"Date and time: {extracted_text}")
