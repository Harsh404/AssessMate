import logging

def setup_logging(verbose, log_file=None):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=log_file
    )

def validate_answer_key(df):
    required = ['question_id', 'correct_answer', 'points']
    if not all(col in df.columns for col in required):
        raise ValueError("Answer key missing required columns")