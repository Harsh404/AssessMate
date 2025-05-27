import unittest
import pandas as pd
from src.grader import grade_answers, compute_class_statistics

class TestGrader(unittest.TestCase):
    def setUp(self):
        self.answer_key = pd.DataFrame({
            'question_id': [1, 2],
            'correct_answer': ['A', 'B'],
            'points': [1, 1]
        })

    def test_perfect_score(self):
        extracted = ['A', 'B']
        result = grade_answers(extracted, self.answer_key)
        self.assertEqual(result['raw_score'], 2)

    def test_case_insensitivity(self):
        extracted = ['a', 'b']
        result = grade_answers(extracted, self.answer_key)
        self.assertEqual(result['raw_score'], 2)

if __name__ == '__main__':
    unittest.main()