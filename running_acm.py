from Main.combined_pipeline import combined_pipeline
from Utilities.database import query_database
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import numpy as np
from nltk.tokenize import word_tokenize
import time
import pandas as pd
import numpy as np
from Main.combined_pipeline import combined_pipeline
from Utilities.database import query_database
import os
import csv
import pandas 
import json

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

    # tp = len(expected_frozensets.intersection(actual_frozensets))  # True positives
    # fp = len(actual_frozensets - expected_frozensets)  # False positives
    # fn = len(expected_frozensets - actual_frozensets)  # False negatives
    #Adjusted for supersets
    tp = sum(any(actual >= expected for actual in actual_frozensets) for expected in expected_frozensets)  # True positives
    fp = len([actual for actual in actual_frozensets if not any(actual >= expected for expected in expected_frozensets)])  # False positives
    fn = len(expected_frozensets - {expected for expected in expected_frozensets if any(actual >= expected for actual in actual_frozensets)})  # False negatives


    accuracy = None  # Avoid division by zero
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0  # Avoid division by zero
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0  # Avoid division by zero
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0  # Avoid division by zero

    if not boolean:
        return accuracy, precision, recall, f1_score, tp, fp, fn
    if boolean:
        return f1_score==1

def create_and_populate_table_two(dataframe, table_name):
    try:
        # Clean table name (optional)
        table_name = table_name.replace(" ", "_")

        # Drop table if it exists
        delete_table_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        query_database(delete_table_query, printing=False)

        # Convert all data to string format (since we're dealing with text data)
        dataframe = dataframe.astype(str)

        # Create table with two columns (for the two columns in the dataframe)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (category TEXT, items TEXT);"
        query_database(create_table_query, printing=False)
        print(f"Table '{table_name}' created successfully.")

        # Insert data into table
        values = []
        for _, row in dataframe.iterrows():
            col1_value = row.iloc[0].replace("'", "''")  # Escape single quotes for SQL
            col2_value = row.iloc[1].replace("'", "''")  # Escape single quotes for SQL
            values.append(f"('{col1_value}', '{col2_value}')")  # Insert each row as a pair of column values

        if values:
            # Build the insert query
            insert_query = f"INSERT INTO {table_name} (category, items) VALUES {', '.join(values)};"
            query_database(insert_query, printing=False)
            print(f"Table '{table_name}' populated successfully.")
        else:
            print("No data to insert.")

    except Exception as e:
        print(f"An error occurred: {e}")

def tuple_bleu_score(candidate, reference, n_gram=1):
    """
    Compute BLEU score between two tuples treated as sentences.
    n_gram: how many grams to consider for BLEU (1, 2, 3, etc.)
    """
    weights = tuple((1.0 / n_gram for _ in range(n_gram)))  # e.g., (1.0,) for 1-gram, (0.5, 0.5) for 2-gram
    chencherry = SmoothingFunction()
    return sentence_bleu([reference], candidate, weights=weights, smoothing_function=chencherry.method1)

def average_best_bleu_score(answer, required_answer, use_n_grams=1):
    """
    Compute BLEU score for a given n-gram level.
    Ensure consistency with calc_bleu by processing tuples as strings.

    :param answer: Set of predicted tuples.
    :param required_answer: Set of ground truth tuples.
    :param use_n_grams: The specific n-gram level to compute BLEU for (1, 2, 3, 4).
    :return: BLEU score for the given n-gram level.
    """
    assert use_n_grams in (1, 2, 3, 4)
    
    # Serialize tuples into strings to match calc_bleu's approach
    answer = [tuple(str(v).lower() for v in x) for x in answer]
    required_answer = [tuple(str(v).lower() for v in x) for x in required_answer]

    if len(required_answer) == 0 or len(answer) == 0:
        return 0.0  # No data to compare

    # Tokenize and prepare both answer and required_answer
    answer_tokens = [word_tokenize(" ".join(candidate)) for candidate in answer]
    required_answer_tokens = [word_tokenize(" ".join(reference)) for reference in required_answer]

    bleu_scores = []

    for candidate in answer_tokens:
        item_bleu_scores = max([sentence_bleu([reference], candidate, smoothing_function=SmoothingFunction().method1, weights=(1.0 / use_n_grams,) * use_n_grams) for reference in required_answer_tokens])
        bleu_scores.append(item_bleu_scores)

    return np.average(bleu_scores)

def create_and_populate_table(dataframe, table_name):
    try:
        # Clean table name (optional)
        table_name = table_name.replace(" ", "_")

        # Drop table if it exists
        delete_table_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        query_database(delete_table_query, printing=False)

        # Convert all data to string format
        dataframe = dataframe.astype(str)

        # Create table with a single column
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (Aggregate TEXT);"
        query_database(create_table_query, printing=False)
        print(f"Table '{table_name}' created successfully.")

        # Insert data into table
        values = []
        for _, row in dataframe.iterrows():
            row_values = "\n".join(row.astype(str))  # Concatenate row values with newline separator
            values.append(f"('{row_values.replace("'", "''")}')")  # Escape single quotes for SQL

        if values:
            insert_query = f"INSERT INTO {table_name} VALUES {', '.join(values)};"
            query_database(insert_query, printing=False)
            print(f"Table '{table_name}' populated successfully.")
        else:
            print("No data to insert.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Load the dataframe annd upload to database
path="Data/DBLP-ACM/ACM.csv"
data_id=pandas.read_csv(path, encoding='unicode_escape')
data_id=data_id.replace("'", "''", regex=True)
data_id["aggregate_id"]= data_id.iloc[:, 2:].astype(str).agg("\n".join, axis=1)
data_id=data_id[["id","aggregate_id"]]


path="Data/DBLP-ACM/DBLP2.csv"
data_link=pandas.read_csv(path, encoding='unicode_escape')
data_link=data_link.replace("'", "''", regex=True)
data_link["aggregate_link"]= data_link.iloc[:, 2:].astype(str).agg("\n".join, axis=1)
data_link=data_link[["id","aggregate_link"]]

path_truth="Data/DBLP-ACM/DBLP-ACM_perfectMapping.csv"
gt= pandas.read_csv(path_truth)
gt=gt.replace("'", "''", regex=True)
gt = gt.sample(n=100, random_state=42)

merged_first = gt.merge(data_id, left_on='idACM', right_on='id')
merged_second =merged_first.merge(data_link, left_on='idDBLP', right_on='id')
merged_final=merged_second[["aggregate_id","aggregate_link"]]

create_and_populate_table(merged_final[["aggregate_id"]], "unique_left")
create_and_populate_table(merged_final[["aggregate_link"]], "unique_right")
create_and_populate_table_two(merged_final, "ground_truth")
 
def calculate_write(two_step_values, threshold_series, filename, csv_filename):
    # Define file name
    file_name = filename

    
    result_dict={}
    for threshold in threshold_series:
        result_dict[threshold] = {}  # Initialize threshold key
        for two_step in two_step_values:
            two_step_temp=two_step
            if two_step_temp==None:
                two_step_temp="None"
            result_dict[threshold][two_step_temp] = []  # Initialize two_step key

            # Execute and write the output to the file
            start = time.time()
            try:
                answer, metadata = combined_pipeline(query=None, initial_sql_query="SELECT * FROM unique_right JOIN unique_left ON unique_left.aggregate = unique_right.aggregate;", aux=True, threshold=threshold, two_step=two_step)
            except Exception as e:
                print(f"An error occurred: {e}")
                metadata = {'prompt_token_count': 0, 'candidates_token_count': 0, 'total_token_count': 0, 'total_calls': 0}
            end = time.time()

            # Problematic situation solution prompt
            solution_prompt = "SELECT * FROM unique_leftaggregateunique_rightaggregate_table;"

            # Try to get the answer
            required_answer = set()
            try:
                required_answer = query_database(solution_prompt, printing=False)
            except:
                required_answer = []
            
            try:
                result_dict[threshold][two_step].append(required_answer)
                # Save the updated dictionary back to the JSON file
                with open(file_name, "w") as file:
                    json.dump(result_dict, file, indent=4)
            except:
                pass
            
            ground_truth_answer = query_database("SELECT * FROM ground_truth;", printing=False)

            #correct_answer = required_answer == answer
            unique_result = list(set(tuple(sorted(set(t))) for t in required_answer))

            try:
                accuracy, precision, recall, f1_score, tp, fp, fn  = evaluate_results(ground_truth_answer, unique_result)
            except:
                accuracy, precision, recall, f1_score, tp, fp , fn = 0, 0, 0, 0,0,0,0

            
            n_gram_range = [1, 2, 3, 4]
            bleu_scores = {}

            for n_gram in n_gram_range:
                score = average_best_bleu_score(ground_truth_answer, required_answer, use_n_grams=n_gram)
                bleu_scores[n_gram] = score  # Store in dictionary
                print(f"BLEU-{n_gram} score: {score:.4f}")  # Nicely formatted output

            # --- Write to CSV ---
            csv_row = {
                "precision": precision,
                "recall": recall,
                "f1_score": f1_score,
                "execution_time": end - start,
                "threshold": threshold,
                "two_step": two_step,
                "bleu_1": bleu_scores[1],
                "bleu_2": bleu_scores[2],
                "bleu_3": bleu_scores[3],
                "bleu_4": bleu_scores[4],
                "prompt_token_count": metadata['prompt_token_count'],
                "candidates_token_count": metadata['candidates_token_count'],
                "total_token_count": metadata['total_token_count'],
                "total_calls": metadata['total_calls'],
                "tp":tp,
                "fp":fp,
                "fn":fn,
            }

            csv_file = csv_filename

            # Check if file exists to decide whether to write headers
            file_exists = os.path.isfile(csv_file)

            #Define the file name
            #json_filename = "required_answers.json"

            # # Save the dictionary to a JSON file
            #with open(json_filename, "w") as json_file:
            #    json.dump(dict, json_file, indent=4)

            # Write data
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=csv_row.keys())
                if not file_exists:
                    writer.writeheader()  # Write headers if file doesn't exist
                writer.writerow(csv_row)


# two_step_values = [ False, None]
# threshold_series = [0.5, 0.6]







threshold_series = [0.5, 0.625, 0.75, 0.875]

threshold_series.append(0.9)
threshold_series.append(0.95)
threshold_series.append(0.975)
# For testing purposes
two_step_values = [True, False]

#calculate_write(two_step_values, threshold_series, "ACM/required_answers.json", "ACM/results_output_acm.csv")


two_step_values = [None]
threshold_series = [0.5]
calculate_write(two_step_values, threshold_series, "ACM/required_answers_None.json", "ACM/results_output_acm_none.csv")