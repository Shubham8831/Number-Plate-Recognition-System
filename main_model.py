import cv2
import pytesseract
import os
import imutils

# Path to Tesseract (change if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Directories
INPUT_FOLDER = r"C:\Users\shubu\Desktop\Number Plate Recognition System\data"
OUTPUT_FOLDER = r"C:\Users\shubu\Desktop\Number Plate Recognition System\output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blurred, 30, 200)
    return edged

def detect_plate(image, original):
    contours = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    plate = None
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            plate = original[y:y+h, x:x+w]
            return plate, (x, y, w, h)
    return None, None

def recognize_text(plate_image):
    gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--psm 8')  # psm 8 for single word
    return text.strip()

def process_images():
    for filename in os.listdir(INPUT_FOLDER):
        if filename.endswith(".jpg"):
            path = os.path.join(INPUT_FOLDER, filename)
            image = cv2.imread(path)
            edged = preprocess(image)
            plate_img, bbox = detect_plate(edged, image)

            if plate_img is not None:
                text = recognize_text(plate_img)
                print(f"[INFO] {filename}: Detected plate -> {text}")
                x, y, w, h = bbox
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            else:
                print(f"[INFO] {filename}: No plate detected.")

            cv2.imwrite(os.path.join(OUTPUT_FOLDER, filename), image)

if __name__ == "__main__":
    process_images()
