import cv2
import numpy as np


def preprocess_image(file_path: str):
    # Read image
    image = cv2.imread(file_path)

    if image is None:
        raise ValueError("Invalid image file")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Denoise
    gray = cv2.medianBlur(gray, 3)

    # Threshold (binarization)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return thresh