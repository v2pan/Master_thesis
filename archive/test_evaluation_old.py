# from row_calculus_pipeline import row_calculus_pipeline
# import os
# from database import query_database
# from extractor import extract
# from llm import ask_llm, llm_json, QUERY, CATEGORY
# import sqlparse
# import re
# from database import query_database, QueryExecutionError
# from llm import llm_json,ask_llm
# from extractor import extract
# import copy
# import json
# from llm import RessourceError
# import time
# import os
# import json
# from collections import Counter
# import matplotlib.pyplot as plt
# import numpy as np
# from join_pipeline imp#OLD
# # def visualize_errors(error_total, queries_list):
# #     #FINAL EVALUATION PLOT

# #     #PATHs for saving plots and dictionaries
# #     path_ind_dic= os.path.join(os.getcwd(), "saved_json", "individual_results")
# #     path_total_dic= os.path.join(os.getcwd(), "saved_json", "total_results")
# #     filepath_total_fig=filepath = os.path.join(os.getcwd(), "saved_plots", "total_probs")
    

# #     num_plots = len(error_total)
# #     num_cols = 2  # Adjust number of columns as needed
# #     num_rows = (num_plots + num_cols - 1) // num_cols

# #     fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 4 * num_rows))
# #     axes = axes.flatten()

# #     #Create a list of dictionaries to also save the data, in order to replot it etc.
# #     dic_list=[]
# #     colors = ['red', 'red', 'red', 'red', 'red', 'red', 'blue'] # Define colors for the bars

# #     for i, error_cnt in enumerate(error_total):
# #         error_spots = list(error_cnt.keys())
# #         counts = list(error_cnt.values())
# #         total_counts = sum(counts)
# #         if total_counts > 0: #Avoid division by zero
# #             probs = [count / total_counts for count in counts]
# #         else:
# #             probs = [0] * len(queries) #All probabilities are 0 if total_counts is 0

# #         title_part1, title_part2 = split_title_at_space(queries_list[i])

# #         #Create dictionary and append data
# #         tmp_dic={
# #             "calculus" : queries_list[i],
# #             "errors" : error_spots,
# #             "error_counts" : counts,
# #             "probabilities" : probs
# #         }

# #         sns.barplot(x='errors', y='error_counts', data=tmp_dic, ax=axes[i], palette=colors).set_title(f"{title_part1}\n{title_part2}")
# #         axes[i].tick_params(axis='x', rotation=30)
# #         #Append to dictionary list
# #         dic_list.append(tmp_dic)


# #     # Remove extra subplots if necessary
# #     for j in range(i + 1, len(axes)):
# #         fig.delaxes(axes[j])

# #     filepath_individual_plot=filepath = os.path.join(os.getcwd(), "saved_plots", "individual_probs")
# #     #Individual plot
# #     plt.tight_layout()
# #     plt.suptitle(f"Counts of Result Types for {RUNS} Runs")
# #     plt.subplots_adjust(top=0.85)
# #     fig.savefig(filepath_individual_plot, dpi=300, bbox_inches='tight')  # Save the figure with higher resolution

# #     plt.show()

# #     # TOTAL PLOT overl all distinct values
# #     fig_total, ax_total = plt.subplots(figsize=(10, 6))
# #     categories = error_total[0].keys()  # Assuming all dictionaries have the same keys
# #     width = 0.35

# #     x = np.arange(len(categories))
# #     total_counts_per_category = np.zeros(len(categories))

# #     for error_cnt in error_total:
# #         for i, cat in enumerate(categories):
# #             total_counts_per_category[i] += error_cnt[cat]

# #     total_counts = np.sum(total_counts_per_category)
# #     if total_counts > 0:
# #         probs = total_counts_per_category / total_counts
# #     else:
# #         probs = np.zeros(len(categories))

# #     #Create total dictionary
# #     total_dic={
# #             "categories" : list(categories),
# #             "probabilities" : list(probs),
# #             "total_counts" : list(total_counts_per_category)
# #         }
    
# #     #Save the two dictionaires
# #     with open(path_ind_dic, 'w', encoding="utf-8") as f:
# #         json.dump(dic_list, f, indent=4, ensure_ascii=False )
# #     with open(path_total_dic, 'w', encoding='utf-8') as f:
# #         json.dump(total_dic, f, indent=4, ensure_ascii=False)

# #     sns.barplot(x='categories', y='total_counts', data=total_dic, ax=ax_total, palette=colors).set_title(f"Total Probabilities of Result Types")
# #     plt.xticks(rotation=30)
# #     plt.tight_layout()
# #     fig_total.savefig(filepath_total_fig, dpi=300, bbox_inches='tight')  # Save the figure with higher resolution
# #     plt.show()



#         with open(filepath, 'r', encoding='utf-8') as f:
#             loaded_dictionary = json.load(f)
#         print(f"Dictionary loaded successfully from {filepath}")
#         print(loaded_dictionary) # Print the loaded dictionary to verify
#     except FileNotFoundError:
#         print(f"Error: File not found at {filepath}")
#     except json.JSONDecodeError:
#         print(f"Error: Invalid JSON data in {filepath}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     error_total=[]
#     queries_list=[]
#     #Iterate over the whole list of input queries
#     for query, join in queries:

#         api_retries = 0
#         #error_cnt={"initial_result": 0, "semantic_list": 0, "wrong_result": 0, "correct_results": 0}
#         error_cnt={"initial_sql_query_join": 0, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 0, "result_where": 0,  "correct_results": 0}
#         #Iterate over all the runs to get the results
#         for i in range(RUNS):
                
#             try:
                
#                 #GET results from the pipeline
#                 initial_sql_query_join, semantic_list_join, result_join, initial_sql_query_where, semantic_list_where, result_where, output =combined_pipeline(query=query, evaluation=True)
                    
#                 data = {
#                     "calculus": query,
#                     "initial_sql_query_join": initial_sql_query_join.replace('\n', ' ') if initial_sql_query_join is not None else None,
#                     "semantic_list_join": semantic_list_join,
#                     "result_join": result_join,
#                     "initial_sql_query_where": initial_sql_query_where.replace('\n', ' ') if initial_sql_query_where is not None else None,
#                     "semantic_list_where": semantic_list_where,
#                     "result_where": result_where,
#                     "output": output   
#                 }
#                 # try:
#                 #     initial_query_result=query_database(initial_query)
#                 # except QueryExecutionError as e:
#                 #     initial_query_result=f"{e}"
#                 #     initial_query_result=initial_query_result.split('\n')[0]


#                 # data = {
#                 #     "calculus": query,
#                 #     # "pipeline": "row_calculus_pipeline",
#                 #     # "tables_num": len(tables),
#                 #     # "tables": tables,
#                 #     "initial_result": initial_query_result,
#                 #     "initial_sql_query": initial_query_result,
#                 #     # "condition": conditions,
#                 #     "semantic_list": semantic_list,
#                 #     # "query_results": query_results,
#                 #     # "sql_query": new_sql_query.replace('\n', ' '),
#                 #     "result": result,

#                 # }


#                 #Retrieve target instances from the loaded dictionary
#                 target_value= query
#                 target_instance = None
#                 for i in loaded_dictionary:
#                     if i["calculus"]==target_value:
#                         target_instance = i
                

                

#             except QueryExecutionError as e:
#                 print("Exception has occured, when executing on database")
#                 continue
#             except RessourceError as e: #Quota exception occurs quite frequently, due to free version of the API 
#                 print("Ressource Error!")
#                 api_retries += 1
#                 print(f"Error(attempt {api_retries}/{max_retries}): {e}")
#                 if api_retries < max_retries:
#                     print(f"Waiting {retry_delay} seconds before retrying...")
#                     time.sleep(retry_delay)
#                 else:
#                     print(f"Maximum retries reached.")
#                     # Append zeros for failed cases
#                     raise Exception(f"Maximum retries reached.")
            
#             #Modify intitial result, only take the first line e.g. (operator does not exist: text < integer)
#             target_initial_result=target_instance["initial_result"]

#             try:
#                 query_database(target_instance["initial_sql_query"])
#             except QueryExecutionError as e:
#                 target_initial_result=target_initial_result.split('\n')[0]

#             #Define function to process a list of lists, for evaluation
#             def process_list(input_list):
#                 processed_list = []
#                 for item in input_list:
#                     if isinstance(item, (list, tuple)):
#                         processed_list.append(item[0])  # Extract the first element if it's a list or tuple
#                     else:
#                         processed_list.append(item)
#                 return processed_list

#             #Define function to compare two lists ignoring the order of them
#             def compare_lists_of_lists(list1, list2):
#                 """Compares two lists of lists, ignoring order within inner lists."""
#                 try:
#                     return Counter(map(frozenset, list1)) == Counter(map(frozenset, list2))
#                 except TypeError:
#                     return False  # Handles cases where inner lists contain unhashable elements


#             #No add the data to the error counter, identify location of the error
#             if data["initial_result"]!=target_initial_result:
#                 error_cnt["initial_result"]+=1
#             elif not compare_lists_of_lists(process_list(target_instance["semantic_list"]), process_list(data["semantic_list"])):
#                 error_cnt["semantic_list"]+=1
#             elif not compare_lists_of_lists(target_instance["result"], data["result"]):
#                 error_cnt["wrong_result"]+=1
#             if compare_lists_of_lists(target_instance["result"], data["result"]):
#                 error_cnt["correct_results"]+=1
        
#             print(f"The error count is {error_cnt}")

#         error_total.append(error_cnt)   
#         queries_list.append(query)

#     #FINAL EVALUATION PLOT
#     num_plots = len(error_total)
#     num_cols = 2  # Adjust number of columns as needed
#     num_rows = (num_plots + num_cols - 1) // num_cols

#     fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 4 * num_rows))
#     axes = axes.flatten()

#     for i, error_cnt in enumerate(error_total):
#         queries = list(error_cnt.keys())
#         counts = list(error_cnt.values())
#         total_counts = sum(counts)
#         if total_counts > 0: #Avoid division by zero
#             probs = [count / total_counts for count in counts]
#         else:
#             probs = [0] * len(queries) #All probabilities are 0 if total_counts is 0

#         axes[i].bar(queries, probs)
#         axes[i].set_xlabel("Result Type")
#         axes[i].set_ylabel("Probability")
#         axes[i].set_title(f"{queries_list[i]}")


#     # Remove extra subplots if necessary
#     for j in range(i + 1, len(axes)):
#         fig.delaxes(axes[j])

#     plt.tight_layout()
#     plt.show()

#     # TOTAL PLOT
#     fig_total, ax_total = plt.subplots(figsize=(10, 6))
#     categories = error_total[0].keys()  # Assuming all dictionaries have the same keys
#     width = 0.35

#     x = np.arange(len(categories))
#     total_counts_per_category = np.zeros(len(categories))

#     for error_cnt in error_total:
#         for i, cat in enumerate(categories):
#             total_counts_per_category[i] += error_cnt[cat]

#     total_counts = np.sum(total_counts_per_category)
#     if total_counts > 0:
#         probs = total_counts_per_category / total_counts
#     else:
#         probs = np.zeros(len(categories))

#     ax_total.bar(categories, probs, width)
#     ax_total.set_ylabel('Probability of Occurrence')
#     ax_total.set_xlabel('Result Type')
#     ax_total.set_title('Total Probabilities of Result Types')
#     plt.tight_layout()
#     plt.show()

# #Sometimes, multiple entries, solve that problem
# queries=[
#         ["∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)"]]
# evaluation_pipeline(queries)

# #OLD



