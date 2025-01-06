from row_calculus_pipeline import get_relevant_tables, get_context, extract_where_conditions_sqlparse, execute_queries_on_conditions, compare_semantics_in_list, initial_query, update_metadata
import os
from database import query_database
from extractor import extract
from other_gemini import ask_gemini, gemini_json, QUERY, CATEGORY
import sqlparse
import re
from database import query_database, QueryExecutionError
from other_gemini import gemini_json,ask_gemini
from extractor import extract
import copy
import json
from other_gemini import RessourceError
import time
import os
import json
from collections import Counter
import matplotlib.pyplot as plt

RUNS=3
max_retries = 10
retry_delay = 60

#TO BE MODIFIED, design a file to get the output of the test, print via the playground file
# to understand where the problem has occured
#Metadata to keep track of use 
usage_metadata_total = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }

#MAIN FUNCTION
def evaluation_pipeline(queries):

    #Load the relevant dictionary
    filepath = os.path.join(os.getcwd(), "temporary", "test")
    
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
        error_cnt={"initial_result": 0, "semantic_list": 0, "wrong_result": 0, "correct_results": 0}
        #Iterate over all the runs to get the results
        for i in range(RUNS):
                
            #Retrieve the correct value
            target_value= query
            target_instance = None
            for i in loaded_dictionary:
                if i["calculus"]==target_value:
                    target_instance = i
            try:
                #Get context
                retries=4
                count=0
                while count<retries:
                    tables = get_relevant_tables(query)
                        
                    if tables is not None:
                        break
                    else:
                        count+=1

                    if tables is None:
                        return None
                    

                print(f"The relevant tables are {tables}")
                context = get_context(tables)

                #Optional, if were to use JSON files
                #Gets context by reading JSON files
                #context= get_context_json(tables)

                print(f"The context is {context}")
                print(f"The query is {query}")

                #Used for relational calculus
                #response, temp_meta = ask_gemini(f"Convert the following query to SQL. Write this query without using the AS: : {query}. Do not use subqueries, but instead use INNER JOINS. Don't rename any of the tables in the query. For every colum reference the respective table. Do not use the Keyword CAST. The structure of the database is the following: {context}.", True,max_token=1000)

                #Used for predicate calculus, selecting all rows
                
                response, temp_meta = initial_query(query,context)
                
                #Update the metadata
                update_metadata(temp_meta)


                #Extract the SQL query from the response
                sql_query = extract(response, start_marker="```sql",end_marker="```" )
                print(f"The SQL query is: {sql_query}")


                try:
                    result_of_initial_query=query_database(sql_query)
                except QueryExecutionError as e:
                    result_of_initial_query=f"{e}"

                #INNER LOGIC: Analyze SQL query, retrieve necessary items to retrieve, compare them using the LLM
                conditions = extract_where_conditions_sqlparse(sql_query)
                query_results = execute_queries_on_conditions(conditions)
                semantic_list=compare_semantics_in_list(query_results)
                print(f"The semantics list is {semantic_list}")

                # Build the list of semantic pairs as a string
                semantic_rows = ''.join(f"{i}\n" for i in semantic_list)

                #Prompt asking LLM to integrate binding
                final_prompt=f'''Write an updated SQL query like this, only using equalities. Only return the updated query. USE only the binding variables like written in bidning. If there is a CASE statement leave it intact, only change the WHERE clause, nothing else. Always end with a ';'.
                    Input: sql:SELECT name, hair FROM person WHERE person.bodypart='eyes'; binding :[('ojos',), ('augen',), 'WHERE person.bodypart ='eyes';']
                    Output: SELECT name, hair FROM person WHERE person.bodypart = 'ojos' OR person.bodypart = 'augen';
                    Input: sql:SELECT e.name, d.name AS department_name, CASE WHEN e.salary > 50000 THEN 'High' WHEN e.salary > 30000 THEN 'Medium' ELSE 'Low' END AS salary_status FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.id = 1; binding: [(1,), (2,), 'WHERE d.id =']
                    Output: SELECT e.name, d.name AS department_name, CASE WHEN e.salary > 50000 THEN 'High' WHEN e.salary > 30000 THEN 'Medium' ELSE 'Low' END AS salary_status FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.id = 1 OR d.id = 2;
                    Input: SELECT * FROM animals WHERE animal.legs<5 and animal.category='insect'; binding: [['three' , 'four', '2', "WHERE animal.legs<5 and animal.category='insect';"], ['INSECTS', "WHERE animal.legs<5 and animal.category='insect';"]]
                    Output: SELECT * FROM animals WHERE animal.some_column IN ('three', 'four', '2') AND animal.category = 'INSECTS';
                    Input: sql:{sql_query}; binding: {semantic_rows}
                    Output:'''
                print(f"The final prompt is {final_prompt}")

                # Try to modify the query with our chosen binding
                response,temp_meta = ask_gemini(final_prompt,True, max_token=1000)
                #Update the metadata
                update_metadata(temp_meta)

                print(f"The response is {response}")

                result=None
                #Extract the SQL query from the response
                try:
                    new_sql_query = extract(response, start_marker="```sql",end_marker="```" )
                    if new_sql_query is None:
                        new_sql_query = extract(response, start_marker="SELECT",end_marker=";",inclusive=True )
                except:
                    pass
                if new_sql_query is None:
                    print("No SQL query found in response.")
                    new_sql_query = ""
                else:
                    try:
                        result=query_database(new_sql_query)
                    except QueryExecutionError:
                        result="QueryExecutionError"
                
                
                data = {
                    "calculus": query,
                    # "pipeline": "row_calculus_pipeline",
                    # "tables_num": len(tables),
                    # "tables": tables,
                    "initial_result": result_of_initial_query,
                    "initial_sql_query": sql_query.replace('\n', ' '),
                    # "condition": conditions,
                    "semantic_list": semantic_list,
                    # "query_results": query_results,
                    # "sql_query": new_sql_query.replace('\n', ' '),
                    "result": result,

                }


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
            
            #Modify intitial result, only take the first line e.g. (operator does not exist: text < integer)
            data_initial_result=data["initial_result"]
            target_initial_result=target_instance["initial_result"]

            if data_initial_result is None:
                data_initial_result=data_initial_result.split('\n')[0]
            if target_initial_result is None:
                target_initial_result=target_initial_result.split('\n')[0]

            #Define function to process a list of lists, for evaluation
            def process_list(input_list):
                processed_list = []
                for item in input_list:
                    if isinstance(item, (list, tuple)):
                        processed_list.append(item[0])  # Extract the first element if it's a list or tuple
                    else:
                        processed_list.append(item)
                return processed_list

            #Define function to compare two lists ignoring the order of them
            def compare_lists_of_lists(list1, list2):
                """Compares two lists of lists, ignoring order within inner lists."""
                try:
                    return Counter(map(frozenset, list1)) == Counter(map(frozenset, list2))
                except TypeError:
                    return False  # Handles cases where inner lists contain unhashable elements


            #No add the data to the error counter, identify location of the error
            if data_initial_result!=target_initial_result:
                error_cnt["initial_result"]+=1
            elif not compare_lists_of_lists(process_list(target_instance["semantic_list"]), process_list(data["semantic_list"])):
                error_cnt["semantic_list"]+=1
            elif not compare_lists_of_lists(target_instance["result"], data["result"]):
                error_cnt["wrong_result"]+=1
            if compare_lists_of_lists(target_instance["result"], data["result"]):
                error_cnt["correct_results"]+=1
        
            print(f"The error count is {error_cnt}")

        error_total.append(error_cnt)   
        queries_list.append(query)

    #FINAL evaluation plot
    num_plots = len(error_total)
    num_cols = 2  # Adjust number of columns as needed
    num_rows = (num_plots + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 4 * num_rows))
    axes = axes.flatten()

    for i, error_cnt in enumerate(error_total):
        queries = list(error_cnt.keys())
        counts = list(error_cnt.values())
        total_counts = sum(counts)
        if total_counts > 0: #Avoid division by zero
            probs = [count / total_counts for count in counts]
        else:
            probs = [0] * len(queries) #All probabilities are 0 if total_counts is 0

        axes[i].bar(queries, probs)
        axes[i].set_xlabel("Result Type")
        axes[i].set_ylabel("Probability")
        axes[i].set_title(f"{queries_list[i]}")
        # axes[i].tick_params(axis='x', rotation=45, ha="right") #Rotate x-axis labels


    # Remove extra subplots if necessary
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()

queries=[
        "∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)",
        #"∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))",
        # "∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )", #Tmp not used
        "∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))",
        # "∃id (children_table(id, >1) ∧ fathers(id, _))" #Tmp not used
        ]
evaluation_pipeline(queries)