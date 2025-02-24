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

def create_and_populate_translation_table(TOTAL_DIC, comparison):
    try:
        # Create the translation table if it doesn't exist
        create_table_prompt = f'''CREATE TABLE IF NOT EXISTS {comparison}_table(
            word TEXT NOT NULL,
            synonym TEXT NOT NULL
        );'''
        query_database(create_table_prompt)  # Execute the table creation query
        
        # Prepare the INSERT query to populate the table
        population_prompt = "INSERT INTO {comparison}_table (word, synonym) VALUES "
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


retry_delay=60

#Metadata to keep track of use 
usage_metadata_row = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }

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
            #

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
    
    return semantic_dic





#MAIN FUNCTION
def row_calculus_pipeline_aux(initial_sql_query, evaluation=False, return_metadata=False):
    
  

    #Metadata to keep track of use set so 0
    for i in usage_metadata_row.keys():
        usage_metadata_row[i]=0
    
    #INNER LOGIC: Analyze SQL query, retrieve necessary items to retrieve, compare them using the LLM
    conditions = extract_where_conditions_sqlparse(initial_sql_query)
    query_results = execute_queries_on_conditions(conditions)
    semantic_list=list_semantics_aux(query_results)
    print(f"The semantics list is {semantic_list}")

    
print("Test")