import cv2
import numpy as np
from PIL import Image, ImageOps

def correct_orientation(img):
    try:
        exif = img._getexif()
    except AttributeError:
        exif = None
    if exif:
        orientation = exif.get(0x0112, 1)
        if orientation == 3:
            img = img.rotate(180, expand=True)
        elif orientation == 6:
            img = img.rotate(270, expand=True)
        elif orientation == 8:
            img = img.rotate(90, expand=True)
    return img

def preprocess_image(image_path):
    with Image.open(image_path) as img:
        img = correct_orientation(img)
        img = img.convert('RGB')
        opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh