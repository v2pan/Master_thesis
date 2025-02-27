import time
from Main.row_calculus_pipeline import row_calculus_pipeline
from Main.join_pipeline import join_pipeline
from Main.combined_pipeline import combined_pipeline
from Utilities.llm import RessourceError
from Utilities.database import QueryExecutionError
import re
import statistics
import pandas as pd
import numpy as np

def evaluate_results(expected, actual,boolean=False):
    """Calculates accuracy, precision, recall, and F1-score, handling tuples."""
    
    if expected is None:
        expected = set()
    if actual is None:
        actual = set()
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

    if not boolean:
        return accuracy, precision, recall, f1_score
    if boolean:
        return f1_score==1

def write_all_metrics_to_file(metrics, filename = "all_metrics.txt"):
    """Writes all individual metrics to a text file."""
    if metrics:
        try:
            with open(filename, "w") as f:
                f.write("--- Individual Metrics ---\n")
                for i, m in enumerate(metrics):
                    accuracy, precision, recall, f1, calculus = m
                    f.write(f"Calculus {calculus}:\n")
                    f.write(f"  Accuracy: {accuracy:.4f}\n")
                    f.write(f"  Precision: {precision:.4f}\n")
                    f.write(f"  Recall: {recall:.4f}\n")
                    f.write(f"  F1-score: {f1:.4f}\n")
                f.write("\n--- Overall Metrics ---\n")
                accuracy_mean = sum(m[0] for m in metrics) / len(metrics)
                precision_mean = sum(m[1] for m in metrics) / len(metrics)
                recall_mean = sum(m[2] for m in metrics) / len(metrics)
                f1_score_mean = sum(m[3] for m in metrics) / len(metrics)
                f.write(f"Mean Accuracy: {accuracy_mean:.4f}\n")
                f.write(f"Mean Precision: {precision_mean:.4f}\n")
                f.write(f"Mean Recall: {recall_mean:.4f}\n")
                f.write(f"Mean F1-score: {f1_score_mean:.4f}\n")
            print(f"Metrics written to '{filename}'")
        except OSError as e:
            print(f"Error writing metrics to file: {e}")
    else:
        print("No metrics to write to file.")

def append_metrics_to_file(metrics, filename="metrics/test_evaluation_metrics.txt"):
    """Appends metrics to the end of the file."""
    try:
        with open(filename, "a") as f:  # Open for appending
            f.write("\n")
            f.write("--- Individual Metrics ---\n")
            f.write(f"Calculus {metrics[4]}:\n")
            f.write(f"  Accuracy: {metrics[0]:.4f}\n")
            f.write(f"  Precision: {metrics[1]:.4f}\n")
            f.write(f"  Recall: {metrics[2]:.4f}\n")
            f.write(f"  F1-score: {metrics[3]:.4f}\n")

    except OSError as e:
        print(f"Error writing metrics to file: {e}")

def append_metadata_to_file(metadata, filename="metrics/test_evaluation_metrics.txt"):
    """Appends metrics to the end of the file."""
    try:
        with open(filename, "a") as f:  # Open for appending
            # f.write("\n")
            # f.write("--- Individual Metrics ---\n")
            # f.write(f"Calculus {metrics[4]}:\n")
            # f.write(f"  Accuracy: {metrics[0]:.4f}\n")
            # f.write(f"  Precision: {metrics[1]:.4f}\n")
            # f.write(f"  Recall: {metrics[2]:.4f}\n")
            # f.write(f"  F1-score: {metrics[3]:.4f}\n")
            for i in metadata.keys():
                f.write(f"{i} AVERAGE: {metadata[i]}\n")

    except OSError as e:
        print(f"Error writing metrics to file: {e}")

def append_time_to_file(times, filename="metrics/test_evaluation_metrics.txt"):
    try:
        with open(filename, "a") as f:  # Open for appending
                f.write(f" AVERAGE Time: {round(np.mean(times),4)}\n")

    except OSError as e:
        print(f"Error writing metrics to file: {e}")

# #Calculate average values
# def calculate_average_metrics(filepath):
#     """Calculates and prints average metrics from a file."""
#     try:
#         with open(filepath, "r") as f:
#             lines = f.readlines()
#     except FileNotFoundError:
#         print(f"Error: File '{filepath}' not found.")
#         return

#     kpis= ['Accuracy', 'Precision', 'Recall', 'F1-score']
#     metrics = {}
#     for line in lines:
#         for kpi in kpis:
#         # Extract calculus name (more robust matching)
#         match = re.search(f"kpi", line)
#         if match:
#             number = match.group(1).strip()
#             metrics[number] = .append(number) 
        
#     with open(filepath, "a") as f:
#             f.write("\n--- Average Metrics ---\n")
#             for kpi in metrics.keys():
#                 f.write(f"Average {kpi}: {metrics[kpi].mean()}\n")

def calculate_average_metrics(filepath):
    """Calculates and prints average metrics from a file."""
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return

    kpis = ['Accuracy', 'Precision', 'Recall', 'F1-score']
    metrics_data = {}  # Use a dictionary to store the data


    for line in lines:
        for kpi in kpis:
            match = re.search(r"{}:\s*([\d.]+)".format(kpi), line)  # Improved regex
            if match:
                value = float(match.group(1))  # Extract and convert to float
                if kpi not in metrics_data:
                    metrics_data[kpi] = []
                metrics_data[kpi].append(value)


    # Check if any metrics were found
    if not metrics_data:
        print("No matching metrics found in the file.")
        return


    with open(filepath, "a") as f:
        f.write("\n--- Average Metrics ---\n")
        for kpi, values in metrics_data.items():
            if values:  # Check if the list is not empty
              avg = statistics.mean(values)
              f.write(f"Average {kpi}: {avg:.2f}\n")  # Format to 2 decimal places
            else:
              f.write(f"Average {kpi}: N/A\n")  # Indicate no data

def calculate_average_tokens(filepath):
    """Calculates and prints average metrics from a file."""
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return
    
    kpis = ['prompt_token_count', 'candidates_token_count', 'total_token_count', 'total_calls', 'AVERAGE Time']
    metrics_data = {}  # Use a dictionary to store the data
    for kpi in kpis:
        metrics_data[kpi] = []

    for line in lines:
        for kpi in kpis:
            #match = re.search(r"{}:\s*([\d.]+)".format(kpi), line)  # Improved regex
            if kpi in line:
                match = re.search(r"([\d.]+)", line)
                value = float(match.group(1))
                metrics_data[kpi].append(value)
            # if match:
            #     value = float(match.group(1))  # Extract and convert to float
            #     if kpi not in metrics_data:
            #         metrics_data[kpi] = []
            #     metrics_data[kpi].append(value)


    # Check if any metrics were found
    if not metrics_data:
        print("No matching metrics found in the file.")
        return


    with open(filepath, "a") as f:
        f.write("\n--- Average Metrics ---\n")
        for kpi, values in metrics_data.items():
            if values:  # Check if the list is not empty
                avg = statistics.mean(values)
                f.write(f"Average {kpi}: {avg:.2f}\n")  # Format to 2 decimal places
            else:
                f.write(f"Average {kpi}: N/A\n")  # Indicate no data





test_cases = [
    (
        '''∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)''',
        {(2, 'Giovanni', '11'), (1, 'Peter', 'ten')} #0
    ),
    (
        '''∃id ∃patients_pd (doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12)''',
        {(1, 'Peter', 'ten')} #1
    ),
    (
        '''∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog'))''',
        {(1, 'Pierre', 20, 1, 'bill', 'chien')} #2
    ),
    (
        '''∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))''', #3
        {(3, 'Diego', 15, 3, 'chris', 'dog'), (4, 'Marcel', 11, 4, 'juan', 'perro'), (1, 'Pierre', 20, 1, 'bill', 'chien')}
    ),
    (   '''∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog'))''', #4
        {(2, 'Vladi', 10, 2, 'diego', 'chat')}
    ),
    (
        '''∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z))''', #5
        {(0, '4', 'zero', 'Gerhard'), (1, '1', 'one', 'Joachim'), (2,'many', 'two', 'Dieter')}
    ),
    (
        '''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )''', #6
        {(1, '1', 'one', 'Joachim', 1, 'Julia'), (2, 'many', 'two', 'Dieter', 2, 'Petra')}
    ),
    (
        '''∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))''', #7
        {(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)}
    ),
    (
        '''∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))''', #8
        {('surviver1000', '1 million', 1, 'surviver1000', True), ('makeuptutorial', '1000 thousand', 3, 'makeuptutorial', False), ('surviver1000', '1 million', 2, 'surviver1000', True), ('princess', 'one thousand', 3, 'princess', True)}
    ),
    (
        '''∃id (children_table(id, >1) ∧ fathers(id, _))''', #9
        {(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')}
    ),
    (
        '''ARTISTS(a,,), ALBUMS(,a,"Reputation",2017),SONGS(,a2,song_name,),ALBUMS(a2,a,)''', #10
        {(1, 1, 'Reputation', '2017', 1, 'Taylor Swift', 'English', 1, 1, 'Delicate', '3:52'), (2, 2, 'Reputation', '2017', 2, 'Reputation Artist', 'English', 2, 2, 'New Year’s Day', '3:55')}
    ),
    (
    '''∃date weather(date, city, temperature, rainfall) ∧ website_visits(date, page, visits)''', #11
    {('2023 10 26', 'London', 12, 0, '2023 October 26', 'about', 500), ('2023 10 26', 'London', 12, 0, '2023 October 26', 'homepage', 1000), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'about', 500), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'homepage', 1000), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'contact', 200), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'homepage', 1200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'contact', 200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'homepage', 1200)}
    ),
    ( 
        '''∃item bakery_sales(item,_,_) ∧ oven_temperature(item, >200 °C)''', #12
        {('Baguettes', '400 °F','8 dozen', '10.00 per dozen')}
    ),
    (
        '''∃item bakery_sales(item,quantity < 55,_) ∧ oven_temperature(item,_)''', #13
        {('Pain au Chocolat', '3 dozen', '15.00 per dozen', '200 °F') }
    ),
    (
        '''∃item bakery_sales(item, > 90,_) ∧ oven_temperature(item, >180 °C)''', #14
        {('Baguettes', '400 °F','8 dozen', '10.00 per dozen')}
    ),
    (
        '''∃movie movies(movie,_, _) ∧ movies_personal(movie, _)''', #15
        {('Wings of Desire', 'fantasy', '4/5', 'Der Himmel über Berlin', '5/5'), ('Amélie', 'comedy', '5/5', 'Die fabelhafte Welt der Amélie', '4/5'), ('The Shawshank Redemption', 'thriller', '3/5', 'Die Flucht aus Shawshank', '3/5')}
    ),
    (
        '''∃movie movies(movie,_, _) ∧ movies_personal(movie, >70%)''', #16
        {('Wings of Desire', 'fantasy', '4/5', 'Der Himmel über Berlin', '5/5'), ('Amélie', 'comedy', '5/5', 'Die fabelhafte Welt der Amélie', '4/5')}
    ),
    (
        '''∃ movies(\"The sky over Berlin\",_,_)''', #17
        {('Wings of Desire', 'fantasy','4/5' )}
    ),
    (
        '''∃clicks influencers( _ , clicks) ∧ publication_clicks(_ , clicks)''', #18
        {('princess', 'one thousand', '24.12.2022', '1000'), ('makeuptutorial', '1000 thousand', '17.01.2011', '1000000'), ('surviver1000', '1 million', '17.01.2011', '1000000')}
    )

]

# calculate_average_metrics("metrics/test_evaluation_metrics_1_5_soft.txt")
# calculate_average_tokens("metrics/test_evaluation_metrics_1_5_soft.txt")