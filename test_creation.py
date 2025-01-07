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
from evaluation import evaluate_results

max_retries = 10
retry_delay = 60

#Appending to JSON file 
def append_to_json(output, filepath):
    """Appends a dictionary to an existing JSON file or creates a new one if it doesn't exist."""
    if not os.path.exists(filepath):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=4, ensure_ascii=False)
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
    write=[]
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
                accuracy, precision, recall, f1_score = evaluate_results(result, output)
                if accuracy == 1 and precision == 1 and recall == 1 and f1_score == 1:
                    write.append(data)
                    #Definition of the output path
                    filepath = os.path.join(os.getcwd(),"temporary", "total_test") #Construct the full path
                    append_to_json(write, filepath)
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
                


         
        


queries = [
    (
        '''∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)''',
        {(2, 'Giovanni', '11'), (1, 'Peter', 'ten')}
    )
    # ,
    # (
    #     '''∃id ∃patients_pd (doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12)''',
    #     {(1, 'Peter', 'ten')}
    # ),
    # (
    #     '''∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog'))''',
    #     {(1, 'Pierre', 20, 1, 'bill', 'chien')}
    # ),
    # (
    #     '''∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))''',
    #     {(3, 'Diego', 15, 3, 'chris', 'dog'), (4, 'Marcel', 11, 4, 'juan', 'perro'), (1, 'Pierre', 20, 1, 'bill', 'chien')}
    # ),
    # (   '''∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog'))''',
    #     {(2, 'Vladi', 10, 2, 'diego', 'chat')}
    # ),
    # (
    #     '''∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z))''',
    #     {(0, 4, 'zero', 'Gerhard'), (1, 1, 'one', 'Joachim'), (2,'many', 'two', 'Dieter')}
    # ),
    # (
    #     '''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )''',
    #     {(1, '1', 'one', 'Joachim', 1, 'Julia'), (2, 'many', 'two', 'Dieter', 2, 'Petra')}
    # ),
    # (
    #     '''∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))''',
    #     {(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)}
    # ),
    # (
    #     '''∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))''',
    #     {('surviver1000', '1 million', 1, 'surviver1000', True), ('makeuptutorial', '1000 thousand', 3, 'makeuptutorial', False), ('surviver1000', '1 million', 2, 'surviver1000', True), ('princess', 'one thousand', 3, 'princess', True)}
    # ),
    # (
    #     '''∃id (children_table(id, >1) ∧ fathers(id, _))''',
    #     {(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')}
    # ),
    # (
    #     '''ARTISTS(a,,), ALBUMS(,a,"Reputation",2017),SONGS(,a2,song_name,),ALBUMS(a2,a,)''',
    #     {(1, 1, 'Reputation', '2017', 1, 'Taylor Swift', 'English', 1, 1, 'Delicate', '3:52'), (2, 2, 'Reputation', '2017', 2, 'Reputation Artist', 'English', 2, 2, 'New Year’s Day', '3:55')}
    # ),
    # (
    # '''∃d weather(d, city, temperature, rainfall) ∧ website_visits(d, page, visits)''',
    # {('2023 10 26', 'London', 12, 0, '2023 October 26', 'about', 500), ('2023 10 26', 'London', 12, 0, '2023 October 26', 'homepage', 1000), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'about', 500), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'homepage', 1000), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'contact', 200), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'homepage', 1200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'contact', 200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'homepage', 1200)}
    # )
]
test_creation_pipeline(queries)