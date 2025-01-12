import time
from row_calculus_pipeline import row_calculus_pipeline
from join_pipeline import join_pipeline
from combined_pipeline import combined_pipeline
from other_gemini import RessourceError
from database import QueryExecutionError

def evaluate_results(expected, actual):
    """Calculates accuracy, precision, recall, and F1-score, handling tuples."""
    if type(expected)!=set:
        set(expected)
    if type(actual)!=set:
        set(actual)
    expected_frozensets = {frozenset(t) for t in expected}
    actual_frozensets = {frozenset(t) for t in actual}

    tp = len(expected_frozensets.intersection(actual_frozensets))  # True positives
    fp = len(actual_frozensets - expected_frozensets)  # False positives
    fn = len(expected_frozensets - actual_frozensets)  # False negatives

    accuracy = (tp) / (tp + fp + fn) if (tp + fp + fn) > 0 else 0  # Avoid division by zero
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0  # Avoid division by zero
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0  # Avoid division by zero
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0  # Avoid division by zero

    return accuracy, precision, recall, f1_score



test_cases = [
    (
        '''∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)''',
        {(2, 'Giovanni', '11'), (1, 'Peter', 'ten')}
    ),
    (
        '''∃id ∃patients_pd (doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12)''',
        {(1, 'Peter', 'ten')}
    ),
    (
        '''∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog'))''',
        {(1, 'Pierre', 20, 1, 'bill', 'chien')}
    ),
    (
        '''∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))''',
        {(3, 'Diego', 15, 3, 'chris', 'dog'), (4, 'Marcel', 11, 4, 'juan', 'perro'), (1, 'Pierre', 20, 1, 'bill', 'chien')}
    ),
    (   '''∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog'))''',
        {(2, 'Vladi', 10, 2, 'diego', 'chat')}
    ),
    (
        '''∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z))''',
        {(0, '4', 'zero', 'Gerhard'), (1, '1', 'one', 'Joachim'), (2,'many', 'two', 'Dieter')}
    ),
    (
        '''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )''',
        {(1, '1', 'one', 'Joachim', 1, 'Julia'), (2, 'many', 'two', 'Dieter', 2, 'Petra')}
    ),
    (
        '''∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))''',
        {(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)}
    ),
    (
        '''∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))''',
        {('surviver1000', '1 million', 1, 'surviver1000', True), ('makeuptutorial', '1000 thousand', 3, 'makeuptutorial', False), ('surviver1000', '1 million', 2, 'surviver1000', True), ('princess', 'one thousand', 3, 'princess', True)}
    ),
    (
        '''∃id (children_table(id, >1) ∧ fathers(id, _))''',
        {(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')}
    ),
    (
        '''ARTISTS(a,,), ALBUMS(,a,"Reputation",2017),SONGS(,a2,song_name,),ALBUMS(a2,a,)''',
        {(1, 1, 'Reputation', '2017', 1, 'Taylor Swift', 'English', 1, 1, 'Delicate', '3:52'), (2, 2, 'Reputation', '2017', 2, 'Reputation Artist', 'English', 2, 2, 'New Year’s Day', '3:55')}
    ),
    (
    '''∃d weather(d, city, temperature, rainfall) ∧ website_visits(d, page, visits)''',
    {('2023 10 26', 'London', 12, 0, '2023 October 26', 'about', 500), ('2023 10 26', 'London', 12, 0, '2023 October 26', 'homepage', 1000), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'about', 500), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'homepage', 1000), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'contact', 200), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'homepage', 1200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'contact', 200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'homepage', 1200)}
    )
    
]

# max_retries = 10
# retry_delay = 60

# metrics = []  # List to store metrics for each test case
# retries = 0
# for calculus, expected_result in test_cases:
    
#     while retries < max_retries:
#         try:
#             #Run the actual pipeline
#             actual_result = set(combined_pipeline(calculus))

#             #Calculate the necessary metrics
#             accuracy, precision, recall, f1_score = evaluate_results(expected_result, actual_result)
#             metrics.append((accuracy, precision, recall, f1_score, calculus))
#             break  # Exit the inner loop if successful
#         except RessourceError as e: #Quota exception occurs quite frequently, due to free version of the API 
#             print("Ressource Error!")
#             retries += 1
#             print(f"Error running calculus '{calculus}' (attempt {retries}/{max_retries}): {e}")
#             if retries < max_retries:
#                 print(f"Waiting {retry_delay} seconds before retrying...")
#                 time.sleep(retry_delay)
#             else:
#                 print(f"Maximum retries reached for calculus '{calculus}'.")
#                 metrics.append((0, 0, 0, 0,calculus)) # Append zeros for failed cases
#                 continue
#         except QueryExecutionError as e:
#             print("Exception has occured, when executing on database")
#             metrics.append((0, 0, 0, 0,calculus))
#             continue
#         except TypeError as e:
#             print("Type Error has occured")

                


# if metrics:  # Check if there are any metrics (to avoid errors if all tests failed)
#     accuracy_mean = sum(m[0] for m in metrics) / len(metrics)
#     precision_mean = sum(m[1] for m in metrics) / len(metrics)
#     recall_mean = sum(m[2] for m in metrics) / len(metrics)
#     f1_score_mean = sum(m[3] for m in metrics) / len(metrics)


#     print("\n--- Overall Metrics ---")
#     print(f"Mean Accuracy: {accuracy_mean:.4f}")
#     print(f"Mean Precision: {precision_mean:.4f}")
#     print(f"Mean Recall: {recall_mean:.4f}")
#     print(f"Mean F1-score: {f1_score_mean:.4f}")
# else:
#     print("No successful test cases to calculate mean metrics.")


# def write_all_metrics_to_file(metrics, filename = "all_metrics.txt"):
#     """Writes all individual metrics to a text file."""
#     if metrics:
#         try:
#             with open(filename, "w") as f:
#                 f.write("--- Individual Metrics ---\n")
#                 for i, m in enumerate(metrics):
#                     accuracy, precision, recall, f1, calculus = m
#                     f.write(f"Calculus {calculus}:\n")
#                     f.write(f"  Accuracy: {accuracy:.4f}\n")
#                     f.write(f"  Precision: {precision:.4f}\n")
#                     f.write(f"  Recall: {recall:.4f}\n")
#                     f.write(f"  F1-score: {f1:.4f}\n")
#                 f.write("\n--- Overall Metrics ---\n")
#                 accuracy_mean = sum(m[0] for m in metrics) / len(metrics)
#                 precision_mean = sum(m[1] for m in metrics) / len(metrics)
#                 recall_mean = sum(m[2] for m in metrics) / len(metrics)
#                 f1_score_mean = sum(m[3] for m in metrics) / len(metrics)
#                 f.write(f"Mean Accuracy: {accuracy_mean:.4f}\n")
#                 f.write(f"Mean Precision: {precision_mean:.4f}\n")
#                 f.write(f"Mean Recall: {recall_mean:.4f}\n")
#                 f.write(f"Mean F1-score: {f1_score_mean:.4f}\n")
#             print(f"Metrics written to '{filename}'")
#         except OSError as e:
#             print(f"Error writing metrics to file: {e}")
#     else:
#         print("No metrics to write to file.")

# write_all_metrics_to_file(metrics)



#OLD Version

#Calculus and the expected result
# test_cases = [
#     (
#         '''∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)''',
#         {(2, 'Giovanni', '11'), (1, 'Peter', 'ten')},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃id ∃patients_pd (doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12)''',
#         {(1, 'Peter', 'ten')},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog'))''',
#         {(1, 'Pierre', 20, 1, 'bill', 'chien')},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))''',
#         {(3, 'Diego', 15, 3, 'chris', 'dog'), (4, 'Marcel', 11, 4, 'juan', 'perro'), (1, 'Pierre', 20, 1, 'bill', 'chien')},
#         "row_calculus_pipeline"
#     ),
#     (   '''∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog'))''',
#         {(2, 'Vladi', 10, 2, 'diego', 'chat')},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z))''',
#         {(0, 4, 'zero', 'Gerhard'), (1, 1, 'one', 'Joachim'), (2,'many', 'two', 'Dieter')},
#         "join_pipeline"
#     ),
#     (
#         '''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )''',
#         {(1, '1', 'one', 'Joachim', 1, 'Julia'), (2, 'many', 'two', 'Dieter', 2, 'Petra')},
#         "join_pipeline"
#     ),
#     (
#         '''∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))''',
#         {(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))''',
#         {('surviver1000', '1 million', 1, 'surviver1000', True), ('makeuptutorial', '1000 thousand', 3, 'makeuptutorial', False), ('surviver1000', '1 million', 2, 'surviver1000', True), ('princess', 'one thousand', 3, 'princess', True)},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃id (children_table(id, >1) ∧ fathers(id, _))''',
#         {(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')},
#         "combined_pipeline"
#     ),
#     (
#         '''ARTISTS(a,,), ALBUMS(,a,"Reputation",2017),SONGS(,a2,song_name,),ALBUMS(a2,a,)''',
#         {(1, 1, 'Reputation', '2017', 1, 'Taylor Swift', 'English', 1, 1, 'Delicate', '3:52'), (2, 2, 'Reputation', '2017', 2, 'Reputation Artist', 'English', 2, 2, 'New Year’s Day', '3:55')},
#         "combined_pipeline"
#     ),
#     (
#     '''∃d weather(d, city, temperature, rainfall) ∧ website_visits(d, page, visits)''',
#     {('2023 10 26', 'London', 12, 0, '2023 October 26', 'about', 500), ('2023 10 26', 'London', 12, 0, '2023 October 26', 'homepage', 1000), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'about', 500), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'homepage', 1000), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'contact', 200), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'homepage', 1200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'contact', 200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'homepage', 1200)}
#     ,"join_pipeline"
#     )

    

# ]