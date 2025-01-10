import os
from database import query_database
from extractor import extract
from other_gemini import ask_gemini, gemini_json, QUERY, CATEGORY
from database import query_database, QueryExecutionError
from other_gemini import gemini_json,ask_gemini
from extractor import extract
import json
from other_gemini import RessourceError
import time
import os
import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from combined_pipeline import combined_pipeline
from evaluation import test_cases
import seaborn as sns
import pandas as pd


RUNS=1
max_retries = 10
retry_delay = 60

#PATHs for saving plots and dictionaries
path_ind_dic= os.path.join(os.getcwd(), "saved_json", "individual_results")
path_total_dic= os.path.join(os.getcwd(), "saved_json", "total_results")
filepath_total_fig=filepath = os.path.join(os.getcwd(), "saved_plots", "total_probs")
filepath_individual_plot=filepath = os.path.join(os.getcwd(), "saved_plots", "individual_probs")

#TO BE MODIFIED, design a file to get the output of the test, print via the playground file
# to understand where the problem has occured
#Metadata to keep track of use 
usage_metadata_total = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }

def initial_query_transform(initial_query):

    if not initial_query:
        return initial_query
    else:
        try:
            initial_query_result=query_database(initial_query)
            return initial_query_result
        except QueryExecutionError as e:
            initial_query_result=f"{e}"
            return initial_query_result.split('\n')[0]
        
#Define function to process a list of lists, for evaluation
def process_list(input_list):
    if not input_list:
        return input_list
    processed_list = []
    for item in input_list:
        if isinstance(item, (list, tuple)):
            processed_list.append(item[0])  # Extract the first element if it's a list or tuple
        else:
            processed_list.append(item)
    return processed_list

#Define function to compare two lists ignoring the order of them
def compare_lists_of_lists(list1, list2):
    """Compares two lists of lists, ignoring order within inner lists. Return True if the same, otherwise return false."""
    if not list1 and not list2:
        return True
    elif not list1 or not list2:
        return False
    try:
        return Counter(map(frozenset, list1)) == Counter(map(frozenset, list2))
    except TypeError:
        return False  # Handles cases where inner lists contain unhashable elements
    
#MAIN FUNCTION
def evaluation_pipeline(queries):

    #Load the relevant dictionary
    filepath = os.path.join(os.getcwd(), "temporary", "total_test")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_dictionary = json.load(f)
        print(f"Dictionary loaded successfully from {filepath}")
        print(loaded_dictionary) # Print the loaded dictionary to verify
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON data in {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

    error_total=[]
    queries_list=[]
    #Iterate over the whole list of input queries
    for query in queries:

        api_retries = 0
        #error_cnt={"initial_result": 0, "semantic_list": 0, "wrong_result": 0, "correct_results": 0}
        error_cnt={"initial_sql_query_join": 0, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 0, "result_where": 0,  "correct_results": 0}
        #Iterate over all the runs to get the results
        for i in range(RUNS):
                
            try:
                
                #GET results from the pipeline
                initial_sql_query_join, semantic_list_join, result_join, initial_sql_query_where, semantic_list_where, result_where, output =combined_pipeline(query=query, evaluation=True)
                initial_sql_query_join_copy= initial_sql_query_join
                data = {
                    "calculus": query,
                    "initial_sql_query_join": initial_sql_query_join.replace('\n', ' ') if initial_sql_query_join is not None else None,
                    "semantic_list_join": semantic_list_join,
                    "result_join": result_join,
                    "initial_sql_query_where": initial_sql_query_where.replace('\n', ' ') if initial_sql_query_where is not None else None,
                    "semantic_list_where": semantic_list_where,
                    "result_where": result_where,
                    "output": output   
                }
                

                #Retrieve target instances from the loaded dictionary
                target_value= query
                target_instance = None
                for i in loaded_dictionary:
                    if i["calculus"]==target_value:
                        target_instance = i
                                

                initial_query_result_join = None
                initial_query_result_where = None
                target_initial_query_result_join = None
                target_initial_query_result_where = None

                results_list = [
                    initial_query_result_join,
                    initial_query_result_where,
                    target_initial_query_result_join,
                    target_initial_query_result_where
                ]

                initial_list= [initial_sql_query_join, initial_sql_query_where, target_instance["initial_sql_query_join"], target_instance["initial_sql_query_where"] ]

                for i in range(len(results_list)):
                    results_list[i]= initial_query_transform(initial_list[i])

                initial_query_result_join = results_list[0]
                initial_query_result_where = results_list[1]
                target_initial_query_result_join = results_list[2]
                target_initial_query_result_where = results_list[3]
                
                

            except QueryExecutionError as e:
                print("Exception has occured, when executing on database")
                continue
            except RessourceError as e: #Quota exception occurs quite frequently, due to free version of the API 
                print("Ressource Error!")
                api_retries += 1
                print(f"Error(attempt {api_retries}/{max_retries}): {e}")
                if api_retries < max_retries:
                    print(f"Waiting {retry_delay} seconds before retrying...")
                    time.sleep(retry_delay)
                else:
                    print(f"Maximum retries reached.")
                    # Append zeros for failed cases
                    raise Exception(f"Maximum retries reached.")

            #FIX the issue of farwarding the initial_query
            if initial_sql_query_join_copy is not None:
                if initial_sql_query_join_copy == data["result_join"] or initial_sql_query_join_copy.replace('\n', ' ') == data["result_where"]:
                    data["result_join"]=[]

            #No add the data to the error counter, identify location of the error
            if target_initial_query_result_join!=initial_query_result_join:
                error_cnt["initial_sql_query_join"]+=1
            elif not compare_lists_of_lists(process_list(target_instance["semantic_list_join"]), process_list(data["semantic_list_join"])):
                error_cnt["semantic_list_join"]+=1
            elif not compare_lists_of_lists(target_instance["result_join"], data["result_join"]):
                error_cnt["result_join"]+=1
            elif target_initial_query_result_where!=initial_query_result_where:
                error_cnt["initial_sql_query_join"]+=1
            elif not compare_lists_of_lists(process_list(target_instance["semantic_list_where"]), process_list(data["semantic_list_where"])):
                error_cnt["semantic_list_where"]+=1
            elif not compare_lists_of_lists(target_instance["result_where"], data["result_where"]):
                error_cnt["result_where"]+=1
            if compare_lists_of_lists(target_instance["output"], data["output"]):
                error_cnt["correct_results"]+=1
        
            print(f"The error count is {error_cnt}")

        error_total.append(error_cnt)   
        queries_list.append(query)
    
   

    #FINAL EVALUATION PLOT
    num_plots = len(error_total)
    num_cols = 2  # Adjust number of columns as needed
    num_rows = (num_plots + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 4 * num_rows))
    axes = axes.flatten()

    #Create a list of dictionaries to also save the data, in order to replot it etc.
    dic_list=[]

    for i, error_cnt in enumerate(error_total):
        error_spots = list(error_cnt.keys())
        counts = list(error_cnt.values())
        total_counts = sum(counts)
        if total_counts > 0: #Avoid division by zero
            probs = [count / total_counts for count in counts]
        else:
            probs = [0] * len(queries) #All probabilities are 0 if total_counts is 0

        # Split the title into two lines at the midpoint
        title_parts = queries_list[i]
        midpoint = len(title_parts) // 2  # Integer division for midpoint
        title_part1 = " ".join(title_parts[:midpoint])
        title_part2 = " ".join(title_parts[midpoint:])

        #Create dictionary and append data
        tmp_dic={
            "calculus" : queries_list[i],
            "errors" : error_spots,
            "error_counts" : counts,
            "probabilities" : probs
        }

        # axes[i].bar(error_spots, probs)
        # axes[i].set_xlabel("Result Type")
        # axes[i].set_ylabel("Probability")
        # axes[i].set_title(f"{title_part1}\n{title_part2}")
        # axes[i].tick_params(axis='x', rotation=45, labelrotation=90)
        sns.barplot(x='errors', y='probabilities', data=tmp_dic, ax=axes[i],).set_title(f"{title_part1}\n{title_part2}")

        

        dic_list.append(tmp_dic)


    # Remove extra subplots if necessary
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.xticks(rotation=30)
    plt.tight_layout()
    fig.savefig(filepath_individual_plot, dpi=300, bbox_inches='tight')  # Save the figure with higher resolution

    plt.show()

    # TOTAL PLOT overl all distinct values
    fig_total, ax_total = plt.subplots(figsize=(10, 6))
    categories = error_total[0].keys()  # Assuming all dictionaries have the same keys
    width = 0.35

    x = np.arange(len(categories))
    total_counts_per_category = np.zeros(len(categories))

    for error_cnt in error_total:
        for i, cat in enumerate(categories):
            total_counts_per_category[i] += error_cnt[cat]

    total_counts = np.sum(total_counts_per_category)
    if total_counts > 0:
        probs = total_counts_per_category / total_counts
    else:
        probs = np.zeros(len(categories))

    #Create total dictionary
    total_dic={
            "categories" : list(categories),
            "probabilities" : list(probs)
        }
    
    #Save the two dictionaires
    with open(path_ind_dic, 'w', encoding="utf-8") as f:
        json.dump(dic_list, f, indent=4, ensure_ascii=False )
    with open(path_total_dic, 'w', encoding='utf-8') as f:
        json.dump(total_dic, f, indent=4, ensure_ascii=False)

    sns.barplot(x='categories', y='probabilities', data=total_dic, ax=ax_total,).set_title(f"Total Probabilities of Result Types'")
    plt.xticks(rotation=30)
    plt.tight_layout()
    fig_total.savefig(filepath_total_fig, dpi=300, bbox_inches='tight')  # Save the figure with higher resolution
    plt.show()
    

#Only get predicate calculus expressions
queries=[i for i, _ in test_cases]
#queries=[queries[0], queries[1], queries[2], queries[3]]
queries=[queries[0]]

evaluation_pipeline(queries)