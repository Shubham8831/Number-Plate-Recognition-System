# Number Plate Recognition Streamlit App

This project is simple **Number Plate Recognition** system built with **Streamlit**, **OpenCV**, and **Tesseract OCR**. It enables users to upload an image of a vehicle, automatically detect the number plate, and recognize the text on the plate. The recognized number and an annotated image are displayed to the user.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)

   * [Clone the Repository](#clone-the-repository)
   * [Python Environment](#python-environment)
   * [Install Python Dependencies](#install-python-dependencies)
   * [Install Tesseract OCR](#install-tesseract-ocr)
5. [Running the App](#running-the-app)
6. [Project Structure](#project-structure)
7. [How It Works](#how-it-works)

   * [Image Preprocessing](#image-preprocessing)
   * [Number Plate Detection](#number-plate-detection)
   * [Text Recognition](#text-recognition)
8. [Usage](#usage)
9. [Customization](#customization)
10. [Troubleshooting](#troubleshooting)
11. [Future Improvements](#future-improvements)
12. [License](#license)

---

## Project Overview

The **Number Plate Recognition Streamlit App** allows users to upload an image of a vehicle, detects the license plate region using classical computer vision techniques, and recognizes the alphanumeric text on the plate using Tesseract OCR. 

---

## Features

* **Streamlit Interface**
* **OpenCV-based Detection**
* **Tesseract OCR**

---

## Requirements

* **Python 3.7+**
* **Tesseract OCR** installed on your system
* The following Python packages (listed in `requirements.txt`):

  * `streamlit`
  * `opencv-python`
  * `pytesseract`
  * `numpy`
  * `Pillow`
  * `imutils`

---

## Installation

Follow these steps to set up and run the application:

### Clone the Repository

```bash
git clone https://github.com/yourusername/number_plate_streamlit_app.git
cd number_plate_streamlit_app
```

### Python Environment

It is recommended to create a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Python Dependencies

Install all required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### Install Tesseract OCR

Tesseract OCR must be installed separately and be available in your system's PATH.

* **Windows**:

  1. Download the installer from the [official Tesseract repository](https://github.com/tesseract-ocr/tesseract).
  2. Run the installer and note the installation path (e.g., `C:\Program Files\Tesseract-OCR`).
  3. Add the installation directory to your **PATH** environment variable.

* **macOS**:

  ```bash
  brew install tesseract
  ```

* **Linux (Debian/Ubuntu-based)**:

  ```bash
  sudo apt update
  sudo apt install tesseract-ocr
  ```

To verify the installation, run:

```bash
tesseract --version
```

You should see Tesseract’s version information.

> **Note**: If Tesseract is not in your PATH, you can set the path in `app.py` by uncommenting and modifying the following line:
>
> ```python
> pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
> ```

---

## Running the App

Once dependencies and Tesseract are installed, launch the Streamlit app:

```bash
streamlit run app.py
```

This will open a new browser window interface. You can upload a vehicle image and see the detected number plate.

---

## Project Structure

```plaintext
number_plate_recognition_system/
├── streamlit_app_trial.py             # Main Streamlit application script
├── main_model.py
├── data
├── requirements.txt   
└── README.md          

```

* **streamlit_app_trial.py**: Contains the full implementation of the Streamlit app—including image uploading, preprocessing, plate detection, and OCR.
* **requirements.txt**: required Python libraries.
* **README.md**

---

## How It Works

The application follows a 3-step process:

1. **Image Preprocessing**
2. **Number Plate Detection**
3. **Text Recognition**

### Image Preprocessing

* **Grayscale Conversion**: The RGB image is converted to grayscale to simplify processing.
* **Noise Reduction**: A bilateral filter is applied to smooth the image while preserving edges. This helps reduce false-positive edges.
* **Edge Detection**: The Canny edge detector highlights strong gradients (edges)


### Number Plate Detection

* **Contour Extraction**: Contours are identified from the edged image using OpenCV’s `findContours` function.
* **Contour Filtering**: Contours are sorted by area (descending), and the top 10 largest are considered.
* **Quadrilateral Approximation**: For each contour, the algorithm approximates the shape using `approxPolyDP`. If a contour has exactly 4 vertices (indicating a quadrilateral), it is assumed to be the plate.
* **Bounding Box**: Once a quadrilateral is found, a bounding rectangle is computed to extract the plate region from the original image.


### Text Recognition

* **Grayscale Conversion of Plate**: The cropped plate image is converted to grayscale again 
* **Tesseract OCR**: Using `pytesseract.image_to_string` with `--psm 8` (treat the image as a single word/line) to extract alphanumeric text.
* **Post-processing**: The returned string is stripped of whitespace. You can add further cleaning (e.g., removing non-alphanumeric characters) if needed.

---

## Usage

1. **Start the App**: Run `streamlit run app.py` in your terminal.
2. **Upload Image**
3. **View Results**

   * it display the recognized number plate text.
   * An annotated image with the bounding box around the detected plate and the recognized text will be shown.

---

## Improvements to be made if i had extra time

1. **Deep Learning-Based Detection**
2. **Video Processing**
3. **API creation**
4. **Deploy**

---
