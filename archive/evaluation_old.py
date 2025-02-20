import time
from Main.row_calculus_pipeline import row_calculus_pipeline

def evaluate_results(expected, actual):
    """Calculates accuracy, precision, recall, and F1-score."""
    expected_set = set(expected)
    actual_set = set(actual)

    tp = len(expected_set.intersection(actual_set))  # True positives
    fp = len(actual_set - expected_set)  # False positives
    fn = len(expected_set - actual_set)  # False negatives

    accuracy = (tp) / (tp + fp + fn) if (tp + fp + fn) > 0 else 0 #Avoid division by zero
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0 #Avoid division by zero
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0 #Avoid division by zero
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0 #Avoid division by zero

    return accuracy, precision, recall, f1_score


test_cases = [
    (
        '''{id, name, patients_pd | doctors(id, name, patients_pd) ∧ patients_pd < 12}''',
        ['doctors'],
        {(2, 'Giovanni', '11'), (1, 'Peter', 'ten')}
    ),
    (
        '''{id, name, patients_pd | doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12}''',
        ['doctors'],
        {(1, 'Peter', 'ten')}
    ),
    (
        '''{name, shares | ∃id (SHAREOWNER1ROW(id, name, shares) ∧ ANIMALOWNER1ROW(id , _, 'dog'))}''',
        ['shareowner1row', 'animalowner1row'],
        {('Pierre', 20)}
    ),
    (
        '''{name, shares | ∃id (SHAREOWNER(id, name, shares) ∧ ANIMALOWNER(id , _, 'dog'))}''',
        ['shareowner', 'animalowner'],
        {('Diego', 15), ('Marcel', 11), ('Pierre', 20)}
    ),

]

max_retries = 3
retry_delay = 60

metrics = []  # List to store metrics for each test case

for calculus, tables, expected_result in test_cases:
    retries = 0
    while retries < max_retries:
        try:
            actual_result = set(row_calculus_pipeline(calculus, tables))
            accuracy, precision, recall, f1_score = evaluate_results(expected_result, actual_result)
            metrics.append((accuracy, precision, recall, f1_score))
            break  # Exit the inner loop if successful
        except Exception as e: #Quota exception occurs quite frequently, due to free version of the API 
            retries += 1
            print(f"Error running calculus '{calculus}' (attempt {retries}/{max_retries}): {e}")
            if retries < max_retries:
                print(f"Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
            else:
                print(f"Maximum retries reached for calculus '{calculus}'.")
                metrics.append((0, 0, 0, 0)) # Append zeros for failed cases

                


if metrics:  # Check if there are any metrics (to avoid errors if all tests failed)
    accuracy_mean = sum(m[0] for m in metrics) / len(metrics)
    precision_mean = sum(m[1] for m in metrics) / len(metrics)
    recall_mean = sum(m[2] for m in metrics) / len(metrics)
    f1_score_mean = sum(m[3] for m in metrics) / len(metrics)


    print("\n--- Overall Metrics ---")
    print(f"Mean Accuracy: {accuracy_mean:.4f}")
    print(f"Mean Precision: {precision_mean:.4f}")
    print(f"Mean Recall: {recall_mean:.4f}")
    print(f"Mean F1-score: {f1_score_mean:.4f}")
else:
    print("No successful test cases to calculate mean metrics.")