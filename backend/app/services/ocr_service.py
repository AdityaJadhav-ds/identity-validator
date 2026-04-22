import pytesseract
import cv2
import numpy as np
import os
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\Users\adity\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"


def extract_text(file_path: str):
    try:
        ext = file_path.split(".")[-1].lower()

        if ext == "pdf":
            images = convert_from_path(
                file_path,
                dpi=200,
                first_page=1,
                last_page=1,
                poppler_path=POPPLER_PATH
            )

            full_text = ""

            for i, img in enumerate(images):
                temp_path = f"temp_{i}.jpg"
                img.save(temp_path, "JPEG")

                text = process_image(temp_path)
                full_text += text + "\n"

                os.remove(temp_path)

            return full_text

        elif ext in ["jpg", "jpeg", "png"]:
            return process_image(file_path)

        return ""

    except Exception as e:
        return f"OCR_ERROR: {str(e)}"


# -----------------------------
# CORE OCR (MULTI-PASS)
# -----------------------------
def process_image(path):
    img = cv2.imread(path)

    if img is None:
        return ""

    # -------- PASS 1: RAW --------
    text_raw = pytesseract.image_to_string(img)

    # -------- PASS 2: LIGHT PREPROCESS --------
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)

    text_gray = pytesseract.image_to_string(gray)

    # -------- PASS 3: PAN TARGETED --------
    h, w = gray.shape
    pan_region = gray[int(h*0.3):int(h*0.6), int(w*0.2):int(w*0.8)]

    config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    text_pan = pytesseract.image_to_string(pan_region, config=config)

    # -------- COMBINE --------
    return text_raw + "\n" + text_gray + "\n" + text_pan