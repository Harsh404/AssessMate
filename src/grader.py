import numpy as np

def grade_answers(extracted, answer_key):
    total = answer_key['points'].sum()
    score = 0
    answers = {}
    for i, row in answer_key.iterrows():
        qid = str(row['question_id'])
        correct = row['correct_answer'].lower()
        points = row['points']
        answer = extracted[i].lower() if i < len(extracted) else ''
        answers[qid] = extracted[i] if i < len(extracted) else ''
        if answer == correct:
            score += points
    return {
        'raw_score': score,
        'total_possible': total,
        'percentage': round(score / total * 100, 2) if total > 0 else 0,
        'answers': answers
    }

def compute_class_statistics(results):
    if not results:
        return {}
    percentages = [res['percentage'] for res in results]
    avg = np.mean(percentages)
    med = np.median(percentages)
    std = np.std(percentages)
    grade_dist = {
        'A (90-100)': sum(90 <= p <= 100 for p in percentages),
        'B (80-89)': sum(80 <= p < 90 for p in percentages),
        'C (70-79)': sum(70 <= p < 80 for p in percentages),
        'D (60-69)': sum(60 <= p < 70 for p in percentages),
        'F (0-59)': sum(p < 60 for p in percentages)
    }
    return {
        'average_score': round(avg, 2),
        'median_score': round(med, 2),
        'highest_score': round(max(percentages), 2),
        'lowest_score': round(min(percentages), 2),
        'standard_deviation': round(std, 2),
        'grade_distribution': grade_dist
    }