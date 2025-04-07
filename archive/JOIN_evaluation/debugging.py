import pandas
import numpy
import re
import time
import csv
import os

from Main.combined_pipeline import combined_pipeline
path="Data/itunes_amazon_raw_data/labeled_data.csv"

#Read the file
data=pandas.read_csv(path, skiprows=5, encoding='unicode_escape')
data

#Index
index_start = 0
index_end = 50
class_vector=data['label']
left_table=data.iloc[:,4:10]
right_table=data.iloc[:,10:16]

#Import the necessary parts from the pipeline
from Evaluation.evaluation import evaluate_results
from Main.combined_pipeline import combined_pipeline
from Evaluation.test_evaluation import evaluate_results
from Utilities.database import query_database

#Function for populating the database
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
        
        
#Function for the definition of the BLEU score
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import numpy as np
from nltk.tokenize import word_tokenize

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

#Define the index range


execution_mode = "local"
#execution_mode = "global"
#Running locally
if execution_mode == "local":
    create_and_populate_table(left_table.iloc[index_start:index_end, :], "left_table")
    create_and_populate_table(right_table.iloc[index_start:index_end, :], "right_table")
    ground_truth_left = data.iloc[index_start:index_end, ]
    ground_truth_left = ground_truth_left[ground_truth_left["label"] == 1]
    ground_truth_left = ground_truth_left.iloc[:, 4:10]
    

#4-10
else: 
    create_and_populate_table(left_table, "left_table")
    create_and_populate_table(right_table, "right_table")
    ground_truth_left = data
    ground_truth_left = ground_truth_left[ground_truth_left["label"] == 1]
    ground_truth_left = ground_truth_left.iloc[:, 4:10]



create_and_populate_table(ground_truth_left, "ground_truth_left")
ground_truth_answer=query_database("SELECT * FROM ground_truth_left;", printing=False)
ground_truth_answer       

# Series of threshold
threshold_series = []
i = 0
while i < 1:
    i += 1 / 8
    threshold_series.append(i)

# For testing purposes
two_step_values = [True]
# threshold_series = [0.9]

# dict={}

for threshold in threshold_series:
    for two_step in two_step_values:

        print("Running logic with two_step=None (No threshold applied)")
        already_run_none = True  # Set to True after the first run

        # Execute and write the output to the file
        start = time.time()
        try:
            answer, metadata = combined_pipeline(query=None, initial_sql_query="SELECT * FROM right_table JOIN left_table ON left_table.aggregate = right_table.aggregate;", aux=True, threshold=threshold, two_step=two_step)
        except Exception as e:
            print(f"An error occurred: {e}")
            metadata = {'prompt_token_count': 0, 'candidates_token_count': 0, 'total_token_count': 0, 'total_calls': 0}
        end = time.time()

        # Problematic situation solution prompt
        solution_prompt = "SELECT * FROM left_table INNER JOIN left_tableaggregateright_tableaggregate_table ON left_table.aggregate = left_tableaggregateright_tableaggregate_table.word INNER JOIN right_table ON left_tableaggregateright_tableaggregate_table.synonym = right_table.aggregate;"

        # Try to get the answer
        required_answer = set()
        try:
            required_answer = query_database(solution_prompt, printing=False)
        except:
            required_answer = set()

        # dict[two_step]=required_answer
        
        # import json

        # # Define the file name
        # json_filename = "required_answers.json"

        # # Save the dictionary to a JSON file
        # with open(json_filename, "w") as json_file:
        #     json.dump(results_dict, json_file, indent=4)

        # print(f"Dictionary saved to {json_filename}")
        # # correct_answer = required_answer == answer
        unique_result = list(set(tuple(sorted(set(t))) for t in required_answer))

        try:
            accuracy, precision, recall, f1_score = evaluate_results(ground_truth_answer, unique_result)
        except:
            accuracy, precision, recall, f1_score = 0, 0, 0, 0

        n_gram_range = [1, 2, 3, 4]
        bleu_scores = {}

        for n_gram in n_gram_range:
            score = average_best_bleu_score(ground_truth_answer, required_answer, n_gram=n_gram)
            bleu_scores[n_gram] = score  # Store in dictionary
            print(f"BLEU-{n_gram} score: {score:.4f}")  # Nicely formatted output

        # --- Write to CSV ---
        csv_row = {
            "accuracy": accuracy,
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
            "total_calls": metadata['total_calls']
        }

        csv_file = "results_output_gemini_debugging.csv"

        # Check if file exists to decide whether to write headers
        file_exists = os.path.isfile(csv_file)

        # Write data
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=csv_row.keys())
            if not file_exists:
                writer.writeheader()  # Write headers if file doesn't exist
            writer.writerow(csv_row)


# # For testing purposes
# two_step_values = [None]

# for threshold in threshold_series:
#     for two_step in two_step_values:

#         print("Running logic with two_step=None (No threshold applied)")
#         already_run_none = True  # Set to True after the first run

#         # Execute and write the output to the file
#         start = time.time()
#         try:
#             answer, metadata = combined_pipeline(query=None, initial_sql_query="SELECT * FROM right_table JOIN left_table ON left_table.aggregate = right_table.aggregate;", aux=True, threshold=threshold, two_step=two_step)
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             metadata = {'prompt_token_count': 0, 'candidates_token_count': 0, 'total_token_count': 0, 'total_calls': 0}
#         end = time.time()

#         # Problematic situation solution prompt
#         solution_prompt = "SELECT * FROM left_table INNER JOIN left_tableaggregateright_tableaggregate_table ON left_table.aggregate = left_tableaggregateright_tableaggregate_table.word INNER JOIN right_table ON left_tableaggregateright_tableaggregate_table.synonym = right_table.aggregate;"

#         # Try to get the answer
#         required_answer = set()
#         try:
#             required_answer = query_database(solution_prompt, printing=False)
#         except:
#             required_answer = set()

#         correct_answer = required_answer == answer
#         unique_result = list(set(tuple(sorted(set(t))) for t in required_answer))

#         try:
#             accuracy, precision, recall, f1_score = evaluate_results(ground_truth_answer, unique_result)
#         except:
#             accuracy, precision, recall, f1_score = 0, 0, 0, 0

#         n_gram_range = [1, 2, 3, 4]
#         bleu_scores = {}

#         for n_gram in n_gram_range:
#             score = average_best_bleu_score(ground_truth_answer, required_answer, n_gram=n_gram)
#             bleu_scores[n_gram] = score  # Store in dictionary
#             print(f"BLEU-{n_gram} score: {score:.4f}")  # Nicely formatted output

#         # --- Write to CSV ---
#         csv_row = {
#             "accuracy": accuracy,
#             "precision": precision,
#             "recall": recall,
#             "f1_score": f1_score,
#             "execution_time": end - start,
#             "threshold": threshold,
#             "two_step": two_step,
#             "bleu_1": bleu_scores[1],
#             "bleu_2": bleu_scores[2],
#             "bleu_3": bleu_scores[3],
#             "bleu_4": bleu_scores[4],
#             "prompt_token_count": metadata['prompt_token_count'],
#             "candidates_token_count": metadata['candidates_token_count'],
#             "total_token_count": metadata['total_token_count'],
#             "total_calls": metadata['total_calls']
#         }

#         csv_file = "results_output_gemini_debugging.csv"

#         # Check if file exists to decide whether to write headers
#         file_exists = os.path.isfile(csv_file)

#         # Write data
#         with open(csv_file, mode='a', newline='') as file:
#             writer = csv.DictWriter(file, fieldnames=csv_row.keys())
#             if not file_exists:
#                 writer.writeheader()  # Write headers if file doesn't exist
#             writer.writerow(csv_row)