import unittest
import cv2
import numpy as np
from src.preprocessor import preprocess_image, correct_orientation

class TestPreprocessor(unittest.TestCase):
    def test_orientation_correction(self):
        # Create test image with EXIF orientation tag
        img = Image.new('RGB', (100, 100))
        img.info['exif'] = 0x0112 << 16 | 6  # Rotate 270
        corrected = correct_orientation(img)
        self.assertEqual(corrected.size, (100, 100))

    def test_preprocessing_steps(self):
        test_image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        processed = preprocess_image(test_image)
        self.assertEqual(processed.shape, (200, 200))  # Should be grayscale

if __name__ == '__main__':
    unittest.main()