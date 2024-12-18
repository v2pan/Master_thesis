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


#Metadata to keep track of use 
usage_metadata_total = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }

#MAIN FUNCTION
def row_calculus_pipeline(query):
    
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
    except QueryExecutionError:
        result_of_initial_query="QueryExecutionError"


    data = {
        "calculus": query,
        "pipeline": "row_calculus_pipeline",
        "tables_num": len(tables),
        "tables": tables,
        "initial_result": result_of_initial_query
    }
    filepath = os.path.join(os.getcwd(), "Test_creation") #Construct the full path

    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)  # Use indent for pretty-printing
        print(f"Dictionary written successfully to {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")


    # #INNER LOGIC: Analyze SQL query, retrieve necessary items to retrieve, compare them using the LLM
    # conditions = extract_where_conditions_sqlparse(sql_query)
    # query_results = execute_queries_on_conditions(conditions)
    # semantic_list=compare_semantics_in_list(query_results)
    # print(f"The semantics list is {semantic_list}")

    # # Build the list of semantic pairs as a string
    # semantic_rows = ''.join(f"{i}\n" for i in semantic_list)

    # #Prompt asking LLM to integrate binding
    # final_prompt=f'''Write an updated SQL query like this, only using equalities. Only return the updated query. USE only the binding variables like written in bidning. If there is a CASE statement leave it intact, only change the WHERE clause, nothing else. Always end with a ';'.
    #     Input: sql:SELECT name, hair FROM person WHERE person.bodypart='eyes'; binding :[('ojos',), ('augen',), 'WHERE person.bodypart ='eyes';']
    #     Output: SELECT name, hair FROM person WHERE person.bodypart = 'ojos' OR person.bodypart = 'augen';
    #     Input: sql:SELECT e.name, d.name AS department_name, CASE WHEN e.salary > 50000 THEN 'High' WHEN e.salary > 30000 THEN 'Medium' ELSE 'Low' END AS salary_status FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.id = 1; binding: [(1,), (2,), 'WHERE d.id =']
    #     Output: SELECT e.name, d.name AS department_name, CASE WHEN e.salary > 50000 THEN 'High' WHEN e.salary > 30000 THEN 'Medium' ELSE 'Low' END AS salary_status FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.id = 1 OR d.id = 2;
    #     Input: SELECT * FROM animals WHERE animal.legs<5 and animal.category='insect'; binding: [['three' , 'four', '2', "WHERE animal.legs<5 and animal.category='insect';"], ['INSECTS', "WHERE animal.legs<5 and animal.category='insect';"]]
    #     Output: SELECT * FROM animals WHERE animal.some_column IN ('three', 'four', '2') AND animal.category = 'INSECTS';
    #     Input: sql:{sql_query}; binding: {semantic_rows}
    #     Output:'''
    # print(f"The final prompt is {final_prompt}")

    # # Try to modify the query with our chosen binding
    # response,temp_meta = ask_gemini(final_prompt,True, max_token=1000)
    # #Update the metadata
    # update_metadata(temp_meta)

    # print(f"The response is {response}")

    # #Extract the SQL query from the response
    # try:
    #     sql_query = extract(response, start_marker="```sql",end_marker="```" )
    #     if sql_query is None:
    #         sql_query = extract(response, start_marker="SELECT",end_marker=";",inclusive=True )
    # except:
    #     pass
    # if sql_query is None:
    #     print("No SQL query found in response.")
    # else:
    #     result=query_database(sql_query)
    # #Print total usage
    # print(usage_metadata_total)
    # #Return result
    # if result:
    #     return result

row_calculus_pipeline("∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)")