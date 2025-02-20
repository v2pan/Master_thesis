import os
import sys
sys.path.insert(0, '/home/vlapan/Documents/Masterarbeit/Relational')
from Utilities.database import query_database
from Utilities.extractor import extract
print(os.getcwd())
from Utilities.llm import ask_llm, llm_json, QUERY, CATEGORY
from Utilities.database import query_database, QueryExecutionError
from Utilities.llm import llm_json,ask_llm, add_metadata
from Utilities.extractor import extract
import json
from Utilities.llm import RessourceError
import time
import os
import json
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from Main.combined_pipeline import combined_pipeline
from Evaluation.evaluation import test_cases, evaluate_results, write_all_metrics_to_file, append_metrics_to_file, append_metadata_to_file, append_time_to_file
import seaborn as sns
import pandas as pd
import re
from matplotlib import ticker
from Utilities.test_creation import append_to_json, append_to_json_dic



#TO BE MODIFIED, design a file to get the output of the test, print via the playground file
# to understand where the problem has occured
#Metadata to keep track of use 



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
def process_list_where(input_list):
    if not input_list:
        return input_list
    processed_list = []
    if type(input_list)==list:
        if len(input_list)==1:
            for item in input_list[0]:
                if isinstance(item, (list, tuple)):
                    processed_list.append(item[0])  # Extract the first element if it's a list or tuple
                else:
                    processed_list.append(item)
        else:
            for lists in input_list:
                sublist = []
                for item in lists:
                    sublist.append(item)
                processed_list.append(sublist)
            return 
        
    else:
        raise ValueError("Input must be a list of lists or tuples")
    return processed_list

def compare_semantic_join(dict1, dict2):
    """Compares dictionaries, ignoring the order of elements in lists. True if the same"""

    #Convert to dictionaries
    if type(dict1)==list:
        dict1=dict1[0]
    if type(dict2)==list:
        dict2=dict2[0]

    if dict1 is None and dict2 is None:
        return True
    if dict1 is None or dict2 is None:
        return False
    
    if dict1.keys() != dict2.keys():
        return False  # Different keys

    for key in dict1:
        if not isinstance(dict1[key], list) or not isinstance(dict2[key], list):
            if dict1[key] != dict2[key]: #check non-list items
              return False
        elif set(dict1[key]) != set(dict2[key]):  # Compare sets to ignore list order
            return False

    return True  # Dictionaries are equivalent (ignoring list order)

#Define function to compare two lists ignoring the order of them
def compare_lists_of_lists(list1, list2):
    """Compares two lists of lists, ignoring order within inner lists. Return True if the same, otherwise return false."""
    if not list1 and not list2:
        return True
    elif not list1 or not list2:
        return False
    try:
        if len(list1) != len(list2):
            return False
        else:
            for i in range(len(list1)):
                result=set(list1[i])==set(list2[i])
                if not result:
                    return False
            return True
            #return Counter(map(frozenset, list1)) == Counter(map(frozenset, list2))
    except TypeError:
        return False  # Handles cases where inner lists contain unhashable elements

#Load the dictionary with the intermediary results
def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_dictionary = json.load(f)
        #print(f"Dictionary loaded successfully from {filepath}")
        #print(loaded_dictionary) # Print the loaded dictionary to verify
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
 
    result_join_data=data["result_join"]
    result_join_target=target_instance["result_join"]

    if result_join_data is not None:
        if "SELECT" in result_join_data and type(result_join_data)==str:
            result_join_data=initial_query_transform(result_join_data)
    if result_join_target is not None:
        if  "SELECT" in result_join_target and type(result_join_target)==str:
            result_join_target=initial_query_transform(result_join_target)



    #No add the data to the error counter, identify location of the error
    #If result is the same, then the result is correct and nothing more is investigated
    if compare_lists_of_lists(target_instance["output"], data["output"]):
        error_cnt["correct_results"]+=1
    else:
        if target_initial_query_result_join!=initial_query_result_join:
            error_cnt["initial_sql_query_join"]+=1
        elif not compare_semantic_join(target_instance["semantic_list_join"], data["semantic_list_join"]):
            error_cnt["semantic_list_join"]+=1
        elif result_join_data!=result_join_target and semantic_list_join[0] is not None:
            error_cnt["result_join"]+=1
        elif target_initial_query_result_where!=initial_query_result_where:
            error_cnt["initial_sql_query_where"]+=1
        elif not compare_lists_of_lists(process_list_where(target_instance["semantic_list_where"]), process_list_where(data["semantic_list_where"])):
            error_cnt["semantic_list_where"]+=1
        elif not compare_lists_of_lists(target_instance["result_where"], data["result_where"]):
            error_cnt["result_where"]+=1
    
        print(f"The error count is {error_cnt}")

    return error_cnt

def error_logic(loaded_dictionary, queries):
    max_retries = 30
    #MODIFY
    retry_delay = 60

    


    error_query_dic={}
    api_retries = 0
    #Iterate over the whole list of input queries
    
    if not isinstance(queries, list):
        queries = [queries]

 
    for query in queries:

        # usage_metadata_total = {
        #     "prompt_token_count": 0,
        #     "candidates_token_count": 0,
        #     "total_token_count": 0,
        #     "total_calls": 0
        # }
        
        #error_cnt={"initial_result": 0, "semantic_list": 0, "wrong_result": 0, "correct_results": 0}
        error_cnt={"initial_sql_query_join": 0, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 0, "result_where": 0,  "correct_results": 0}
        #IterTest
        #Counter variable
        l=0
        metrics = []  # List to store metrics for each test case
        metadata={
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }
        times=[]
        while l < RUNS:
            start=time.process_time()
                        
            #GET results from the 
            try:
                initial_sql_query_join, semantic_list_join, result_join, initial_sql_query_where, semantic_list_where, result_where, output, tmp_metadata =combined_pipeline(query=query, evaluation=True)
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
            
            #Write target output as a list of tuples as expected
            #target_output = [tuple(target_instance["output"])]
            list_output=[]
            target_output=target_instance["output"]
            if output is not None:
                for i in target_output:
                    list_output.append(tuple(i))
            target_output=list_output

            #KPI calculation
            accuracy, precision, recall, f1_score = evaluate_results(output, target_output)
            metrics.append([accuracy, precision, recall, f1_score])
            metadata = add_metadata(tmp_metadata, metadata)
            end=time.process_time()
            times.append(end-start)

        #Calculate average values for accuracy, precision, recall, f1_score
        #and add it to appropriate folder
        num_positions = len(metrics[0])  # Assumes all inner lists have the same length
        averages = [sum(metrics[i][j] for i in range(len(metrics))) / len(metrics) for j in range(num_positions)]
        metrics_list=[]
        [metrics_list.append(i) for i in averages]
        metrics_list.append(query)

        modelname= "gemini-1.5-flash"
        append_metrics_to_file(metrics_list ,filename="metrics/test_evaluation_metrics_" + modelname + ".txt")

        #Work with metadata
        for i in metadata.keys():
            metadata[i]=metadata[i]/RUNS

        append_metadata_to_file(metadata, filename="metrics/test_evaluation_metrics_" + modelname + ".txt")
        
        #Append the time taken for the whole pipeline
        append_time_to_file(times, filename="metrics/test_evaluation_metrics_" + modelname + ".txt")

        error_query_dic[query]=error_cnt
        
        #Additionally write to path
        path_query_error= os.path.join(os.getcwd(), "saved_json", "error_query_list_" + modelname)
        append_to_json_dic(error_query_dic, path_query_error)
    
    #Write that to a file
    #write_all_metrics_to_file(overall_metrics, filename="test_evaluation_metrics")

    #Return necessary output
    return None


#MAIN FUNCTION
def evaluation_pipeline(queries):

    #Load the relevant dictionary
    filepath = os.path.join(os.getcwd(), "temporary", "total_test")
    loaded_dictionary = load_data(filepath)

    #Evaluate the results
    error_logic(loaded_dictionary,queries)

    #visualize_errors(error_total, queries_list)
    
    

# index=[16,17]
# new_queries=[]
# for i in index:
#     new_queries.append(queries[i])
# queries=new_queries

#How many runs per expression, Done everything
RUNS=3
queries= [i for i, _ in test_cases]
# evaluation_pipeline(queries)








