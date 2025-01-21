from row_calculus_pipeline import get_relevant_tables, get_context, extract_where_conditions_sqlparse, execute_queries_on_conditions, compare_semantics_in_list, initial_query, update_metadata
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
from combined_pipeline import combined_pipeline
from evaluation import evaluate_results, test_cases

max_retries = 30
retry_delay = 60

path= os.path.join(os.getcwd(),"temporary", "total_test")

#Appending to JSON file 
def append_to_json(output, filepath):
    """Appends a dictionary to an existing JSON file or creates a new one if it doesn't exist."""
    if not os.path.exists(filepath):
        try:
            #Append a list of dictionaries
            write=[]
            write.append(output)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(write, f, indent=4, ensure_ascii=False)
            print(f"Created new file {filepath} with data.")
            return True
        except Exception as e:
            print(f"Error creating file {filepath}: {e}")
            return False
    else:
        try:
            with open(filepath, 'r+', encoding='utf-8') as f:
                existing_data = json.load(f)
                existing_data.append(output)  # Append the new data
                f.seek(0)  # Crucial: Go back to the beginning of the file
                json.dump(existing_data, f, indent=4, ensure_ascii=False)
                f.truncate()  # Important: Truncate the file to remove the old content
                print(f"Data appended to {filepath} successfully.")
                return True
        except json.JSONDecodeError as e:
            print(f"Error decoding existing data in {filepath}: {e}.  Creating new file.")
            return append_to_json(output, filepath) #Recursively try creating a new file if decoding fails.
        except Exception as e:
            print(f"An error occurred while appending to {filepath}: {e}")
            return False
        


#MAIN FUNCTION
def test_creation_pipeline(queries):
    api_retries = 0
    #Iterate over the whole list of input queries
    for query, result in queries:
        match=False
        while not match:
            try:

                #Initialize it empty
                initial_sql_query_where, semantic_list_where, result_where = None, None, None
                initial_sql_query_join, semantic_list_join, result_join = None, None, None
                output=None

                initial_sql_query_join, semantic_list_join, result_join, initial_sql_query_where, semantic_list_where, result_where, output =combined_pipeline(query=query, evaluation=True)
                    
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


                # data = {
                #     "calculus": query,
                #     # "pipeline": "row_calculus_pipeline",
                #     # "tables_num": len(tables),
                #     # "tables": tables,
                #     "initial_result": result_of_initial_query,
                #     "initial_sql_query": sql_query.replace('\n', ' '),
                #     # "condition": conditions,
                #     "semantic_list": semantic_list,
                #     # "query_results": query_results,
                #     # "sql_query": new_sql_query.replace('\n', ' '),
                #     "result": result,

                # }
                try:
                    accuracy, precision, recall, f1_score = evaluate_results(result, output)
                except TypeError as e:
                    print(f"Error evaluating results: {e}")
                    accuracy, precision, recall, f1_score = 0, 0, 0, 0
                if accuracy == 1 and precision == 1 and recall == 1 and f1_score == 1:
                    #Definition of the output path
                    filepath = path #Construct the full path
                    append_to_json(data, filepath)
                    match=True
                else:
                    print(f"Result does not match!")
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
                

#Test creation done for all 19 examples
queries= test_cases
print(len(queries))
#test_creation_pipeline(queries)




