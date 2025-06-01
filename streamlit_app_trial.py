import streamlit as st
import cv2
import pytesseract
import numpy as np
import imutils
from PIL import Image

# telling pytesseract where is tesseract.exe is located on Windows.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="Number Plate Recognition", layout="centered")

st.title("Number Plate Recognition")
st.write("Upload a vehicle image, and the app will detect and read the number plate.")

uploaded_file = st.file_uploader("Choose a vehicle image", type=["jpg", "jpeg", "png"])

# fn takes rgb image and give edges
def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(blurred, 30, 200)
    return edged

# function to give plate region
def detect_plate(image, original):
    contours = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            plate_img = original[y:y+h, x:x+w]
            return plate_img, (x, y, w, h)
    return None, None

# function to find text from the plate region
def recognize_text(plate_img):
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--psm 8')
    return text.strip()


if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    edged = preprocess(image_cv)
    plate_img, bbox = detect_plate(edged, image_cv)

    if plate_img is not None:
        number = recognize_text(plate_img)
        x, y, w, h = bbox
        cv2.rectangle(image_cv, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image_cv, number, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2) 
        
        st.success(f" Recognized Number: **{number}**")
        st.image(cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB), caption="Detected Plate", use_column_width=True)
    else:
        st.warning(" No number plate found.")
