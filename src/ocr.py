import cv2
import pytesseract

def detect_answer_regions(image):
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = 500
    filtered = [c for c in contours if cv2.contourArea(c) > min_area]
    sorted_contours = sorted(filtered, key=lambda c: cv2.boundingRect(c)[1])
    return sorted_contours

def extract_text_from_region(region_image):
    text = pytesseract.image_to_string(region_image, config='--psm 7')
    return text.strip()