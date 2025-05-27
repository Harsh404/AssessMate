import argparse
import json
import logging
import os
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.preprocessor import preprocess_image
from src.ocr import detect_answer_regions, extract_text_from_region
from src.grader import grade_answers, compute_class_statistics
from src.utils import setup_logging, validate_answer_key

def process_image(image_path, answer_key_df, logger):
    try:
        # Preprocess the image
        image = preprocess_image(image_path)
        # Detect answer regions
        regions = detect_answer_regions(image)
        # Extract answers
        extracted_answers = []
        for region in regions:
            x, y, w, h = cv2.boundingRect(region)
            region_image = image[y:y+h, x:x+w]
            text, confidence = extract_text_from_region(region_image)
            if confidence < 50:
                logger.warning(f"Low OCR confidence ({confidence}) for region in {image_path}")
            extracted_answers.append(text.strip() if text else "")
        # Grade answers
        result = grade_answers(extracted_answers, answer_key_df)
        return {
            "student_id": Path(image_path).stem,
            "image_file": Path(image_path).name,
            **result
        }
    except Exception as e:
        logger.error(f"Error processing {image_path}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Offline Assessment Grading Tool")
    parser.add_argument("--input_dir", required=True, help="Directory containing answer sheet images")
    parser.add_argument("--key", required=True, help="Path to CSV answer key")
    parser.add_argument("--output", required=True, help="Path for output JSON report")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--log_file", help="Path to log file")
    args = parser.parse_args()

    setup_logging(args.verbose, args.log_file)
    logger = logging.getLogger(__name__)

    # Read and validate answer key
    try:
        answer_key_df = pd.read_csv(args.key)
        validate_answer_key(answer_key_df)
    except Exception as e:
        logger.error(f"Invalid answer key: {e}")
        return

    # Collect image paths
    image_paths = []
    for ext in ["*.jpg", "*.jpeg", "*.png"]:
        image_paths.extend(Path(args.input_dir).glob(ext))
    image_paths = list(map(str, image_paths))
    total_images = len(image_paths)
    logger.info(f"Found {total_images} images to process")

    # Process each image
    individual_results = []
    failed_images = 0
    for path in image_paths:
        result = process_image(path, answer_key_df, logger)
        if result:
            individual_results.append(result)
        else:
            failed_images += 1

    # Generate report
    metadata = {
        "processed_date": datetime.utcnow().isoformat() + "Z",
        "total_images": total_images,
        "successfully_processed": len(individual_results),
        "failed_images": failed_images,
        "total_questions": len(answer_key_df)
    }
    class_stats = compute_class_statistics(individual_results)
    report = {
        "metadata": metadata,
        "individual_results": individual_results,
        "class_statistics": class_stats
    }

    # Save report
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2)
    logger.info(f"Report generated at {args.output}")

if __name__ == "__main__":
    main()