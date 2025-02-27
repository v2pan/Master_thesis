import sys
sys.path.insert(0, '/home/vlapan/Documents/Masterarbeit/Relational')
import os
from Utilities.database import query_database
from Utilities.extractor import extract
from Utilities.llm import ask_llm, llm_json, QUERY, CATEGORY
import sqlparse
import re
from Utilities.database import query_database
from Utilities.llm import llm_json,ask_llm, RessourceError,  add_metadata
from Utilities.extractor import extract
import copy
import time
from Main.row_calculus_pipeline import extract_where_conditions_sqlparse, execute_queries_on_conditions

retry_delay=60

#Metadata to keep track of use 
usage_metadata_row = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }



def create_and_populate_translation_table(TOTAL_DIC, comparison):
    try:
        comparison = re.sub(r"[\s'.;=]", "", comparison)

        delete_table_prompt = f"DROP TABLE IF EXISTS {comparison}_table CASCADE;"
        query_database(delete_table_prompt)  # Execute the table deletion query

        # Get the type of the first key
        type_word = type(list(TOTAL_DIC.keys())[0])

        # Check if the type is str or int
        if type_word == str:
            type_word = "TEXT"
        elif type_word == int:
            type_word = "INTEGER"
        else:
            raise TypeError(f"Unexpected type: {type_word}, expected str or int.")
        
        type_synonym = type(TOTAL_DIC[list(TOTAL_DIC.keys())[0]][0])
        if type_synonym == str:
            type_synonym = "TEXT"
        elif type_synonym == int:
            type_synonym = "INTEGER"
        else:
            raise TypeError(f"Unexpected type: {type_synonym}, expected str or int.")


        # Create the translation table if it doesn't exist
        create_table_prompt = f'''CREATE TABLE IF NOT EXISTS {comparison}_table(
            word {type_word} NOT NULL,
            synonym {type_synonym} NOT NULL
        );'''
        query_database(create_table_prompt)  # Execute the table creation query

        print(f"The table with the name {comparison}_table was created.")
        
        # Prepare the INSERT query to populate the table
        population_prompt = f"INSERT INTO {comparison}_table (word, synonym) VALUES "
        values = []
        
        # Loop through the dictionary and create the values part of the query
        for key, synonyms in TOTAL_DIC.items():
            for synonym in synonyms:
                    values.append(f"('{key}', '{synonym}')")
        
        if values:
            population_prompt += ', '.join(values) + ';'
            query_database(population_prompt)  # Execute the insert query
        else:
            print("No values to insert.")
            
        print("Table created and populated successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")



def list_semantics_aux(input_list):
    """
    Compare each pair of expressions in a sublist to determine if they have the same semantic meaning
    using the llm_json function. 

    Args:
    - input_list (list of lists): The input list of expressions and comparisons.

    Returns:
    - semantic_list (list of lists): A list of lists where each sublist contains expressions with the same semantic meaning.
    """
    semantic_dic = {}  # Store the results
    semantic_list = []
    #For duplicate elimination
    from Main.combined_pipeline import TOTAL_DIC
    
    # Iterate over each sublist in the input list
    for outer_list in input_list:
        #Identify the binding and the elemetn
        if (type(outer_list[0]) == str and type(outer_list[-1]) == list) or (type(outer_list[-1]) == str and type(outer_list[0]) == list):
            temp_list = None
            temp_string = None
            
            #Auxiliary variable to determine which part of the list is the string and which is the list
            left=None
            # Determine which part of the list is the string and which is the list, comparing them against on another
            # Cases where both are different not yet covered
            if type(outer_list[0]) == str:
                temp_string = outer_list[0]
                temp_list = outer_list[-1]
                left=True
            else:
                temp_string = outer_list[-1]
                temp_list = outer_list[0]
                left=False
            condition=outer_list[1]
            
            #Let LLM generate a goal to make sure LLM takes right decision
            # goal,temp_meta=ask_llm(f'''Write out the goal for this clause in natural language. Focus on the
            #                 semantic meaning. {outer_list[-2]}. Be brief.
            #                 Input: 'WHERE person.id <> 2'
            #                 Output: Retrieve instances where the id of the person is not 2
            #                 Input : {outer_list[-2]}
            #                 Output:
            #                 ''', True, max_token=100)
            # print(f"The goal is {goal}")
            #add_metadata(temp_meta)
            #Ask LLM to generate a phrase for the comparison
            phrase,temp_meta=ask_llm(f'''Write the output out in natural languge and ignore possible numbers
                              Input: (2, <Comparison '<' at 0x75D1C85F0A00>)
                              Output: is smaller than
                              Input: (2, <Comparison '!=' at 0x75D1C85F0A00>)
                              Output: has NOT the same meaning (also in another language) as
                              Input: (2, <Comparison '<>' at 0x75D1C85F0A00>)
                              Output: has NOT the same meaning (also in another language) as
                              Input: (2, <Comparison '=' at 0x75D1C85F0A00>)
                              Output: has the same meaning as (also in antoher language) or is the same as
                              Input:{condition}.
                              Output:''',True, max_token=100)
            
            #Update the metadata
            _ = add_metadata(temp_meta,usage_metadata_row)
            print(f"The phrase is:\n {phrase}. ")

            print(f"temp_string: {temp_string}")
            print(f"temp_list: {temp_list}")

            # Compare the string with the items in the list using llm_json
            soft_binding_dic = {}
            # Compare the string with the items in the list using llm_json
            soft_binding_list = []

            #Final prompt with list
            #total_prompt="Answer the following questions with True or False." # Change in connection with bakery Fahrenheit/Celcius example
            total_prompt=f"Answer the following questions with True or False. Reason you thinking, especially considering the units, converting units to another and then answering the question.  \n"
            # Iterate over the items in temp_list and compare with temp_string
            for item in temp_list:
                item=item[0]

                #Deletes unnecessary "\n"
                if type(item)!=int:
                    item=item.replace("\n", "")
                if type(temp_string)!=int:
                    temp_string=temp_string.replace("\n", "")
                if type(phrase)!=int:
                    phrase=phrase.replace("\n", "")
                #Actual logic, this is where the semantic binding occurs
                if left:
                    prompt = f"'{temp_string}'  {phrase} '{item}' \n"
                else:
                    prompt = f" '{item}'  {phrase} '{temp_string}' \n"
                #Add condition to the prompt
                total_prompt+=prompt

            #Figure out the binding by giving out a list of lists    
            # response = llm_json(total_prompt, response_type=list[bool])

            answer,temp_meta=ask_llm(total_prompt,return_metadata=True)
            _=add_metadata(temp_meta,usage_metadata_row)
            response, temp_meta = llm_json(f"For this question \n{total_prompt} \n The following asnwer was given {answer}. Return the necessary answer whether this question is true or False", response_type=list[bool], return_metadata=True)  # Expect a list of booleans back
            _=add_metadata(temp_meta,usage_metadata_row)
            #Check if response has same length
            if len(response)!=len(temp_list):
                print("Error")
                print("The response and the temp_list have different lengths")
                print(f"The response is {response}")
                print(f"The temp_list is {temp_list}")
                break

            #Retrieve the relevant items
            relevant_items = [temp_list[i] for i, is_relevant in enumerate(response) if is_relevant]

            if relevant_items is not None:
                soft_binding_dic[temp_string] =[] 
                for i in relevant_items:
                    i=i[0]
                    soft_binding_dic[temp_string].append(i)

            #Add to List for duplicate elimination
            #For duplicate elimination
            if relevant_items is not None:
                TOTAL_DIC[temp_string]=[]
                for i in relevant_items:
                    i=i[0]
                    if i!=temp_string:
                        TOTAL_DIC[temp_string].append(i)

            
            #Appen to final dictionary please:
            semantic_dic[outer_list[-2]] = soft_binding_dic

            #Adding for List:
            for i in relevant_items:
                soft_binding_list.append(i)

            #Add the where clause
            soft_binding_list.append(outer_list[-2]) 
            # If there are any items that have the same meaning, add temp_string and the matching items to the result list
            if soft_binding_list:
                semantic_list.append(soft_binding_list)
    
    return semantic_dic, semantic_list





#MAIN FUNCTION
def row_calculus_pipeline(initial_sql_query, evaluation=False, return_metadata=False):
    
  

    #Metadata to keep track of use set so 0
    for i in usage_metadata_row.keys():
        usage_metadata_row[i]=0
    
    #INNER LOGIC: Analyze SQL query, retrieve necessary items to retrieve, compare them using the LLM
    conditions = extract_where_conditions_sqlparse(initial_sql_query)
    query_results = execute_queries_on_conditions(conditions)
    semantic_dic, semantic_list=list_semantics_aux(query_results)
    print(f"The semantics dic is {semantic_dic}")

    #Create and populate the translation table
    semantic_rows=[]
    for key in semantic_dic.keys():
        create_and_populate_translation_table(semantic_dic[key], key)
        semantic_rows.append(key)


    
    #Prompt asking LLM to integrate binding
    final_prompt=f'''Write an updated SQL query like this. Incorporate the additional tables as an intermediate output please.
        Input: sql:SELECT * FROM vehicles INNER JOIN owners ON vehicles.owner_id = owners.id WHERE vehicles.color = 'red'; semantic_rows = [wherevehiclescolorred_table]
        Output: SELECT * FROM vehicles 
        INNER JOIN owners ON vehicles.owner_id = owners.id 
        INNER JOIN wherevehiclescolorred_table ON wherevehiclescolorred_table.synonym = vehicles.color 
        WHERE wherevehiclescolorred_table.word = 'red';
        Input: sql: SELECT * FROM employees INNER JOIN departments ON employees.dept_id = departments.id WHERE employees.job_title = 'engineer'; semantic_rows = [whereemployeesjobtitleengineer_table]
        Output: SELECT * FROM employees 
        INNER JOIN departments ON employees.dept_id = departments.id 
        INNER JOIN whereemployeesjobtitleengineer_table ON whereemployeesjobtitleengineer_table.synonym = employees.job_title 
        WHERE whereemployeesjobtitleengineer_table.word = 'engineer';
        Input: sql:{initial_sql_query}; semantic_rows: {semantic_rows}
        Output:'''
    print(f"The final prompt is {final_prompt}")

   # Try to modify the query with our chosen binding
    response,temp_meta = ask_llm(final_prompt,True, max_token=1000)
    #Update the metadata
    _ = add_metadata(temp_meta,usage_metadata_row)

    print(f"The response is {response}")

    #Extract the SQL query from the response
    try:
        sql_query = extract(response, start_marker="```sql",end_marker="```" )
        if sql_query is None:
            sql_query = extract(response, start_marker="SELECT",end_marker=";",inclusive=True )
    except:
        pass
    if sql_query is None:
        print("No SQL query found in response.")
    else:
        try:
            result=query_database(sql_query)
        except:
            result=None
    #Clean the result
    if result is not None:
        cleaned_result = []
        for i in semantic_dic.keys():
            for word in semantic_dic[i].keys():
                for row in result:
                    found = False
                    new_row = []
                    for item in row:
                        # Check if word is equal to current item and if we haven't found it yet
                        if item == word and not found:
                            found = True  # Set the flag to True so we don't remove further occurrences
                        else:
                            new_row.append(item)  # Add to new row if it's not the first occurrence of the word
                    cleaned_result.append(tuple(new_row))  # Add the modified row (as a tuple)

        result = cleaned_result
    #print(usage_metadata_total)
    #Return result
    print(usage_metadata_row)
    if not return_metadata:
        if evaluation:
            return initial_sql_query, semantic_list, result
        else:
            return result
    if return_metadata:
        if evaluation:
            return initial_sql_query, semantic_list, result, usage_metadata_row
        else:
            return result, usage_metadata_row


    