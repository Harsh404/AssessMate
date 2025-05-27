import unittest
import cv2
import numpy as np
from src.ocr import detect_answer_regions, extract_text_from_region

class TestOCR(unittest.TestCase):
    def test_region_detection(self):
        # Create test image with white rectangle
        img = np.zeros((500, 500), dtype=np.uint8)
        img[100:150, 100:400] = 255
        regions = detect_answer_regions(img)
        self.assertEqual(len(regions), 1)

    def test_text_extraction(self):
        # Create clean test image with text
        img = 255 * np.ones((50, 200), dtype=np.uint8)
        cv2.putText(img, "TEST", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
        text = extract_text_from_region(img)
        self.assertEqual(text.strip(), "TEST")

if __name__ == '__main__':
    unittest.main()