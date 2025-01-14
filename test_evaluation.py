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
from evaluation import test_cases, evaluate_results
import seaborn as sns
import pandas as pd
import re
from matplotlib import ticker




#TO BE MODIFIED, design a file to get the output of the test, print via the playground file
# to understand where the problem has occured
#Metadata to keep track of use 
usage_metadata_total = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }

import re

def split_title_at_space(title):
    """Splits a title at the closest space to the midpoint."""
    if not title or len(title) <= 1:
        return title, ""  # Handles empty or single-word titles

    midpoint = len(title) // 2
    
    # Find the closest space to the midpoint (using regex for robustness)
    
    closest_space_index = None
    min_distance = float('inf')
    list=re.finditer(r"\s", title)
    for match in list:
        index = match.start()
        distance = abs(index - midpoint)
        if distance < min_distance:
            min_distance = distance
            closest_space_index = index
            
    if closest_space_index is not None:
      title_part1 = title[:closest_space_index].strip()
      title_part2 = title[closest_space_index:].strip()
      return title_part1, title_part2
    else:
      return title, ""

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

#Load the dictionary with the intermediary results
def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_dictionary = json.load(f)
        print(f"Dictionary loaded successfully from {filepath}")
        print(loaded_dictionary) # Print the loaded dictionary to verify
        return loaded_dictionary
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        raise FileNotFoundError
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON data in {filepath}")
        raise json.JSONDecodeError
    except Exception as e:
        print(f"An error occurred: {e}")
        raise Exception
    
def comparison_logic(result_dic, target_instance):
    #Strucutre of result dictionary
    # result_dic={
    #                 "initial_sql_query_join" : initial_sql_query_join,
    #                 "semantic_list_join" : semantic_list_join,
    #                 "result_join" : result_join,
    #                 "initial_sql_query_where" : initial_sql_query_where,
    #                 "semantic_list_where" : semantic_list_where,
    #                 "result_where" : result_where,
    #                 "output" : output
    #             }

    # Initialize error counter
    error_cnt={"initial_sql_query_join": 0, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 0, "result_where": 0,  "correct_results": 0}
    # Create variables using dictionary unpacking
    initial_sql_query_join, semantic_list_join, result_join, initial_sql_query_where, semantic_list_where, result_where, output = \
    result_dic.get("initial_sql_query_join"), result_dic.get("semantic_list_join"), result_dic.get("result_join"), \
    result_dic.get("initial_sql_query_where"), result_dic.get("semantic_list_where"), result_dic.get("result_where"), \
    result_dic.get("output")

    #Covering case, semantic list is None
    if not semantic_list_join:
        result_join=initial_sql_query_join
    elif not semantic_list_join[0]:
        result_join=initial_sql_query_join
    data = {
        #"calculus": query,
        "initial_sql_query_join": initial_sql_query_join.replace('\n', ' ') if initial_sql_query_join is not None else None,
        "semantic_list_join": semantic_list_join,
        "result_join": result_join.replace('\n', ' ') if result_join and type(result_join)==str else None,
        "initial_sql_query_where": initial_sql_query_where.replace('\n', ' ') if initial_sql_query_where is not None else None,
        "semantic_list_where": semantic_list_where,
        "result_where": result_where,
        "output": output   
    }
                    

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
 

    #FIX the issue of farwarding the initial_query
    # if initial_sql_query_join_copy is not None:
    #     if initial_sql_query_join_copy == data["result_join"] or initial_sql_query_join_copy.replace('\n', ' ') == data["result_where"]:
    #         data["result_join"]=[]

    #TESTING PURPOSE
    if target_initial_query_result_join!=initial_query_result_join:
        pass
    elif not compare_lists_of_lists(process_list(target_instance["semantic_list_join"]), process_list(data["semantic_list_join"])):
        pass
    elif not compare_lists_of_lists(target_instance["result_join"], data["result_join"]):
        pass
    elif target_initial_query_result_where!=initial_query_result_where:
        pass
    elif not compare_lists_of_lists(process_list(target_instance["semantic_list_where"]), process_list(data["semantic_list_where"])):
        pass
    elif not compare_lists_of_lists(target_instance["result_where"], data["result_where"]):
        pass

    #No add the data to the error counter, identify location of the error
    #If result is the same, then the result is correct and nothing more is investigated
    if compare_lists_of_lists(target_instance["output"], data["output"]):
        error_cnt["correct_results"]+=1
    else:
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
    
        print(f"The error count is {error_cnt}")

    return error_cnt

def error_logic(loaded_dictionary, queries):
    max_retries = 30
    #MODIFY
    retry_delay = 30

    

    error_total=[]
    queries_list=[]
    api_retries = 0
    #Iterate over the whole list of input queries
    for query in queries:

        
        #error_cnt={"initial_result": 0, "semantic_list": 0, "wrong_result": 0, "correct_results": 0}
        error_cnt={"initial_sql_query_join": 0, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 0, "result_where": 0,  "correct_results": 0}
        #Iterate over all the runs to get the results
        
        #Counter variable
        l=0
                
        while l < RUNS:
                        
            #GET results from the 
            try:
                initial_sql_query_join, semantic_list_join, result_join, initial_sql_query_where, semantic_list_where, result_where, output =combined_pipeline(query=query, evaluation=True)
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
                    continue
                else:
                    print(f"Maximum retries reached.")
                    # Append zeros for failed cases
                    raise Exception(f"Maximum retries reached.")
            result_dic={
                "initial_sql_query_join" : initial_sql_query_join,
                "semantic_list_join" : semantic_list_join,
                "result_join" : result_join,
                "initial_sql_query_where" : initial_sql_query_where,
                "semantic_list_where" : semantic_list_where,
                "result_where" : result_where,
                "output" : output
            }
            #Retrieve target instances from the loaded dictionary
            target_value= query
            target_instance = None
            for i in loaded_dictionary:
                if i["calculus"]==target_value:
                    target_instance = i
            error_cnt_tmp = comparison_logic(result_dic, target_instance)
            for key in error_cnt.keys():
                error_cnt[key] += error_cnt_tmp[key]
            l+=1

        error_total.append(error_cnt)   
        queries_list.append(query)
    return error_total, queries_list

def visualize_errors(error_total, queries_list):
    #FINAL EVALUATION PLOT

    #PATHs for saving plots and dictionaries
    path_ind_dic= os.path.join(os.getcwd(), "saved_json", "individual_results")
    path_total_dic= os.path.join(os.getcwd(), "saved_json", "total_results")
    filepath_total_fig=filepath = os.path.join(os.getcwd(), "saved_plots", "total_probs")
    filepath_individual_plot=filepath = os.path.join(os.getcwd(), "saved_plots", "individual_probs")

    num_plots = len(error_total)
    num_cols = 2  # Adjust number of columns as needed
    num_rows = (num_plots + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 4 * num_rows))
    axes = axes.flatten()

    #Create a list of dictionaries to also save the data, in order to replot it etc.
    dic_list=[]
    colors = ['red', 'red', 'red', 'red', 'red', 'red', 'blue'] # Define colors for the bars

    for i, error_cnt in enumerate(error_total):
        error_spots = list(error_cnt.keys())
        counts = list(error_cnt.values())
        total_counts = sum(counts)
        if total_counts > 0: #Avoid division by zero
            probs = [count / total_counts for count in counts]
        else:
            probs = [0] * len(queries) #All probabilities are 0 if total_counts is 0

        title_part1, title_part2 = split_title_at_space(queries_list[i])

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
        sns.barplot(x='errors', y='error_counts', data=tmp_dic, ax=axes[i], palette=colors).set_title(f"{title_part1}\n{title_part2}")
        axes[i].tick_params(axis='x', rotation=30)
        #Append to dictionary list
        dic_list.append(tmp_dic)


    # Remove extra subplots if necessary
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    #Individual plot
    plt.tight_layout()
    plt.suptitle(f"Counts of Result Types for {RUNS} Runs")
    plt.subplots_adjust(top=0.85)
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
            "probabilities" : list(probs),
            "total_counts" : list(total_counts_per_category)
        }
    
    #Save the two dictionaires
    with open(path_ind_dic, 'w', encoding="utf-8") as f:
        json.dump(dic_list, f, indent=4, ensure_ascii=False )
    with open(path_total_dic, 'w', encoding='utf-8') as f:
        json.dump(total_dic, f, indent=4, ensure_ascii=False)

    sns.barplot(x='categories', y='total_counts', data=total_dic, ax=ax_total, palette=colors).set_title(f"Total Probabilities of Result Types")
    plt.xticks(rotation=30)
    plt.tight_layout()
    fig_total.savefig(filepath_total_fig, dpi=300, bbox_inches='tight')  # Save the figure with higher resolution
    plt.show()


#MAIN FUNCTION
def evaluation_pipeline(queries):

    #Load the relevant dictionary
    filepath = os.path.join(os.getcwd(), "temporary", "total_test")
    loaded_dictionary = load_data(filepath)

    #Evaluate the results
    error_total, queries_list =error_logic(loaded_dictionary,queries)

    visualize_errors(error_total, queries_list)
    
    
    

#How many runs per expression
RUNS=2
queries= [i for i, _ in test_cases]
queries=[queries[-1], queries[-2]]
evaluation_pipeline(queries)