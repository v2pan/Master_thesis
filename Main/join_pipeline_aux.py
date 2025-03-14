import sqlparse
import re
from Main.row_calculus_pipeline import execute_queries_on_conditions,  get_context, get_relevant_tables
from Main.join_pipeline import extract_join_conditions_sqlparse
from Main.row_calculus_aux_pipeline import create_and_populate_translation_table
from Utilities.llm import ask_llm, llm_json, add_metadata, RessourceError
from Utilities.database import query_database, QueryExecutionError
from Utilities.extractor import extract
from Utilities.llm import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import copy
import time
import re



#Metadata to keep track of use for the JOIN pipeline
usage_metadata_join = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }


#
    

def compare_semantics_in_list(input_list,order, threshold=None,two_step=False):
    """
    Compares each unique item from the first list in each sublist against every element in the second list to find semantically equivalent expressions using llm_json.

    Args:
        input_list (list of lists):  Each sublist contains [left_list, condition, right_list, original_expression].

    Returns:
        result_list (list of lists): A list where each sublist contains semantically equivalent expressions.
    """
    total_dic= {}
    dict_list = []
    #Iteration over all JOINs
    counter=0
    for outer_list in input_list:
        if isinstance(outer_list[0], list) and isinstance(outer_list[-1], list):
            soft_binding_dic ={}
            dict={}
            temp_list1 = outer_list[0]
            temp_list2 = outer_list[-1]

            necessary=True
            
            #Distinguish between cases where only one element is present and cases where both are numerical and therefore rewriting not necessary
            if len(input_list)<2 and not ( isinstance(temp_list1[0][0], (int, float)) and isinstance(temp_list2[0][0], (int, float))) : #Change down to 2
                necessary=True
            elif len(input_list)<2 and isinstance(temp_list1[0][0], (int, float)) and isinstance(temp_list2[0][0], (int, float)) :
                necessary=False
            else:
                #If both are numerical no need to rewrite the JOIN condition
                if isinstance(temp_list1[0][0], (int, float)) and isinstance(temp_list2[0][0], (int, float)):
                    necessary = False
                else:
                    prompt=f'''Do you think based on the following list {temp_list1} with type {type(temp_list1[0][0])} and {temp_list2} with type {type(temp_list2[0][0])} that some elements have the same semantic meaning but are expressed in a different format?
                    An example would be if the types were different or the formats (e.g., '18 January 2012' and '18.01.2012'), if elements had the same meaning in different languages (e.g., 'bridge' and 'brücke') or if numbers would be written as text.
                    Considering the provided lists represent what they represent, one in {type(temp_list1[0][0])} format and the other in {type(temp_list2[0][0])} format, does a case where different types represent the same semantic meaning occur in the list? If the types are different, always answer 'true'.True or False.'''
                    #Check if it is necessary to rewrite the JOIN condition
                    necessary, temp_meta=llm_json(prompt, response_type=bool, return_metadata=True)
                    _=add_metadata(temp_meta, usage_metadata_join)
            if necessary:
                condition = outer_list[1]
                original_expression = outer_list[2]  # Access the original expression

                # goal = ask_llm(f"""Write out the goal for this clause in natural language. Focus on the
                #                 semantic meaning. {original_expression}. Be brief.
                #                 Input: 'WHERE person.id <> 2'
                #                 Output: Retrieve instances where the id of the person is not 2
                #                 Input : {original_expression}
                #                 Output:
                #                 """)
                # print(f"The goal is: {goal}")

                # phrase, temp_meta = ask_llm(f"""Write the output in natural language and ignore possible numbers.
                #                 Input: (2, <Comparison '<' at 0x75D1C85F0A00>)
                #                 Output: is smaller than
                #                 Input: (2, <Comparison '!=' at 0x75D1C85F0A00>)
                #                 Output: has a different meaning than
                #                 Input: (2, <Comparison '<>' at 0x75D1C85F0A00>)
                #                 Output: has a different meaning than
                #                 Input: (2, <Comparison '=' at 0x75D1C85F0A00>)
                #                 Output: has the same meaning as (also in another language) or is the same as
                #                 Input:{condition}.
                #                 Output:""", True, max_token=100)
                # #Update the metadata
                # _=add_metadata(temp_meta, usage_metadata_join)
                # #add_metadata(temp_meta)
                # print(f"The phrase is: {phrase}")
                comparison_mapping = {
                "=": "has the same meaning as (also in another language) or is the same as",
                "<": "is smaller than",
                "!=": "has a different meaning than",
                "<>": "has a different meaning than",
                
                }

                # Extract the comparison operator from the condition (assuming condition is in a similar format)
                condition_str = str(condition)
                operator = next((op for op in comparison_mapping if op in condition_str), None)

                if operator:
                    phrase = comparison_mapping[operator]
                else:
                    phrase = "Unknown comparison"
                same_meaning_list = []
                seen_items = set()  # Track unique items from temp_list1
                
                batch_size = 10  # You can adjust batch size depending on LLM token limits and API performance
                item_batches = []
                current_batch = []

                # Collect items for batching
                for item in temp_list1:
                    item_str = item[0]
                    if item_str in seen_items:
                        continue
                    seen_items.add(item_str)
                    current_batch.append(item_str)

                    if len(current_batch) >= batch_size:
                        item_batches.append(current_batch)
                        current_batch = []

                # Add remaining items if any
                if current_batch:
                    item_batches.append(current_batch)

                # Process each batch
                for batch in item_batches:
                    total_prompts = []  # To collect all prompts for this batch
                    item_to_other_items = {}  # Mapping for later result mapping

                    for item_str in batch:
                        batch_prompt = ""
                        filtered_temp_list2 = []
                        
                        if two_step is None:
                            # Prepare prompts for each item in batch
                            for other_item in temp_list2:
                                other_item_str = other_item[0]
                                batch_prompt += f"'{item_str}' {phrase} '{other_item_str}' \n"
                            item_to_other_items[item_str] = temp_list2  # Keep full list for mapping
                            total_prompts.append(batch_prompt)

                        elif two_step is True:
                            # Prepare prompts only for filtered embeddings
                            threshold_temp_list = []
                            for other_item in temp_list2:
                                other_item_str = other_item[0]
                                emb1 = np.array(get_embedding(item_str)).reshape(1, -1)
                                emb2 = np.array(get_embedding(other_item_str)).reshape(1, -1)
                                if cosine_similarity(emb1, emb2) > threshold:
                                    batch_prompt += f"'{item_str}' {phrase} '{other_item_str}' \n"
                                    threshold_temp_list.append(other_item)
                            if threshold_temp_list:  # Only if any passed the threshold
                                total_prompts.append(batch_prompt)
                                item_to_other_items[item_str] = threshold_temp_list

                        else:  # Only Embeddings
                            relevant_items = []
                            for other_item in temp_list2:
                                other_item_str = other_item[0]
                                emb1 = np.array(get_embedding(item_str)).reshape(1, -1)
                                emb2 = np.array(get_embedding(other_item_str)).reshape(1, -1)
                                if cosine_similarity(emb1, emb2) > threshold:
                                    relevant_items.append(other_item_str)

                            # Save results directly since no LLM call is needed here
                            soft_binding_dic[item_str] = relevant_items
                            dict[item_str] = relevant_items

                    # Only proceed to LLM if we have prompts to process
                    if total_prompts:
                        full_prompt = "Answer the following questions with True or False.\n" + "\n".join(total_prompts)

                        # Get response from LLM
                        json_success = False
                        response = []
                        total_other_items = sum([len(item_to_other_items[item]) for item in batch])
                        while not json_success or len(response) != total_other_items:
                            try:
                                response, temp_meta = llm_json(full_prompt, response_type=list[bool], return_metadata=True)
                                json_success = True
                            except RessourceError:
                                print(f"Resource Error occurred in Join Pipeline JSON")
                                time.sleep(60)
                        _ = add_metadata(temp_meta, usage_metadata_join)

                        # Split responses back to respective items
                        resp_index = 0
                        for item_str in batch:
                            other_items = item_to_other_items[item_str]
                            relevant_items = []
                            for i in range(len(other_items)):
                                if response[resp_index]:
                                    relevant_items.append(other_items[i][0])
                                resp_index += 1

                            # Add relevant items to dictionaries
                            soft_binding_dic[item_str] = relevant_items
                            dict[item_str] = relevant_items

                            
                                


                    # #Add relevant semantic equivalents to the list
                    # if relevant_items is not None:
                    #     soft_binding_dic[item_str] =[] 
                    #     for i in relevant_items:
                    #         soft_binding_dic[item_str].append(i)

                    # #Add to semantic list for comparison
                    # dict[item_str] = relevant_items
                    

                print(f"The key belongs to {order[counter][0]}")
                print(f"The value belongs to {order[counter][1]}")
                expression=re.sub(r"[\s'.;=]", "", outer_list[-2])
                total_dic[expression]= soft_binding_dic
                #Increase counter
                counter+=1

                #Semantic list
                dict_list.append(dict)
            else:
                expression=re.sub(r"[\s'.;=]", "", outer_list[-2])
                total_dic[expression]= soft_binding_dic
                dict_list.append(dict)
         

    return dict_list, order, total_dic

def join_pipeline(initial_sql_query, return_query=False, evaluation=False, forward=False, return_metadata=False, threshold=None,two_step=None):



    #Set global metadata to 0
    for i in usage_metadata_join.keys():
        usage_metadata_join[i]=0

    # Example usage
    join_conditions, order = extract_join_conditions_sqlparse(initial_sql_query)
    print(join_conditions)
    #Make sure this is correct, maybe rewrite to iterate again
    new_list = execute_queries_on_conditions(join_conditions)
    print(new_list)
    #TODO: Multiple dictinoaries for multiple JOINs
    semantic_dic, order, new_dic= compare_semantics_in_list(new_list, order, threshold=threshold, two_step=two_step)
    print( new_dic)
    print(order)

    #If no element are present, no need to rewrite the JOIN condition, return as it was
    if not any(semantic_dic): 
        if not return_metadata:
            if return_query:
                    return initial_sql_query
            if evaluation and not forward:
                    return initial_sql_query, semantic_dic, initial_sql_query
            elif evaluation and forward:
                    return initial_sql_query, semantic_dic, initial_sql_query
            else:
                if forward:
                    return initial_sql_query
                else:
                    return initial_sql_query
        if return_metadata:
            if return_query:
                    return initial_sql_query, usage_metadata_join
            if evaluation and not forward:
                    return initial_sql_query, semantic_dic, initial_sql_query, usage_metadata_join
            elif evaluation and forward:
                    return initial_sql_query, semantic_dic, initial_sql_query, usage_metadata_join
            else:
                if forward:
                    return initial_sql_query, usage_metadata_join
                else:
                    return initial_sql_query, usage_metadata_join

    semantic_rows = []
    tmp_count=0
    for key in  new_dic.keys():
        key_new = re.sub(r"[\s'.;=<>!%]", "", key)+"_table"
        create_and_populate_translation_table(new_dic[key], key_new)
        if semantic_dic[tmp_count]!={}:
            semantic_rows.append(key_new)
        tmp_count+=1


    #Create the binding string for, necessary for multiple JOINs
    binding_str = ""
    # for i in range(len(semantic_dic)):
    #     binding_str += f"binding {i}: {semantic_dic[i]}. The key belongs to {order[i][0]}, The values belong to {order[i][1]}\n"
    #Final prompt for modification of the query
    if len(semantic_dic)<2:
        final_prompt=f''' Extend the SQL query by the following translation table. 
            Input sql: SELECT * FROM employees INNER JOIN departments ON employees.department_id = departments.id; binding: employeesidepartmentsid_table
            Output: SELECT * FROM employees 
            INNER JOIN employeesidepartmentsid_table ON employees.department_id = employeesidepartmentsid_table.word
            INNER JOIN departments ON employeesidepartmentsid_table.synonym = departments.id;
            Input sql: SELECT employees.fullname, departments.dept_name FROM departments JOIN employees ON departments.id  = employees.department_id; binding: {{'Acme Corp': ['Acme Corp'], 'Sales Dep': ['Sales Department'], 'Engeneering': ['Engineering']}}; order: The key belongs to departments.id, The values belong to employees.department_id.
            Input: SELECT * FROM students INNER JOIN classes ON students.class_id = classes.id;binding: studentsiclassid_table
            Output: SELECT * FROM students 
            INNER JOIN studentsiclassid_table ON students.class_id = studentsiclassid_table.word
            INNER JOIN classes ON studentsiclassid_table.synonym = classes.id;
            Input: sql: SELECT * FROM students_table INNER JOIN teachers ON students_table.id = teachers.id INNER JOIN courses ON students_table.id = courses.id; binding: ['students_tableidteachersid_table']  
            Output:  SELECT *  FROM students_table  INNER JOIN students_tableidteachersid_table ON students_table.id = students_tableidteachersid_table.word  
            INNER JOIN teachers ON students_tableidteachersid_table.synonym = teachers.id  
            INNER JOIN courses ON students_table.id = courses.id;
            SELECT * FROM left_table JOIN right_table ON right_table.rtable_Song_Name=left_table.ltable_Song_Name;
            Input:  SELECT * FROM right_table INNER JOIN left_table ON left_table.ltablesongname = right_table.rtablesongname;'binding:['left_tableltablesongnameright_tablertablesongname_table']
            Output= SELECT * FROM left_table INNER JOIN right_tablertablesongnameleft_tableltablesongname_table ON left_table.ltablesongname = right_tablertablesongnameleft_tableltablesongname_table.synonym INNER JOIN right_table ON right_tablertablesongnameleft_tableltablesongname_table.word = right_table.rtablesongname;  
            Input: sql:{initial_sql_query}; binding: {semantic_rows};
            Output:'''
    
    #If multiple JOINs are present, the prompt is different, different problem as important what is substituted by what
    else:
        final_prompt=f''' Extend the SQL query by the following translation table. 
            Input sql: SELECT * FROM employees INNER JOIN departments ON employees.department_id = departments.id; binding: employeesidepartmentsid_table
            Output: SELECT * FROM employees 
            INNER JOIN employeesidepartmentsid_table ON employees.department_id = employeesidepartmentsid_table.word
            INNER JOIN departments ON employeesidepartmentsid_table.synonym = departments.id;
            Input: sql: SELECT * FROM students_table INNER JOIN teachers ON students_table.id = teachers.id INNER JOIN courses ON students_table.id = courses.id; binding: ['students_tableidteachersid_table']  
            Output:  SELECT *  FROM students_table  INNER JOIN students_tableidteachersid_table ON students_table.id = students_tableidteachersid_table.word  
            INNER JOIN teachers ON students_tableidteachersid_table.synonym = teachers.id  
            INNER JOIN courses ON students_table.id = courses.id;  
            Input: sql:{initial_sql_query}; binding: {semantic_rows};
            Output:'''
    

    retries_left=3
    while retries_left>0:
        print(f"The final prompt is \n {final_prompt}")
        # Try to modify the query with our chosen binding
        response,temp_meta = ask_llm(final_prompt,True, max_token=1000)
        _ = add_metadata(temp_meta, usage_metadata_join)
        #Update the metadata
        #add_metadata(temp_meta)
        print(f"The response is {response}")

        #Extract query and get result
        try:
            sql_query = extract(response, start_marker="```sql",end_marker="```" )
            if sql_query is None:
                sql_query = extract(response, start_marker="SELECT",end_marker=";",inclusive=True )
        except:
            pass
        if sql_query is None:
            print("No SQL query found in response.")
            return None
        else:
            print(f"The SQL query is: {sql_query}")
            #If only query is to be returned, going on with another pipeline
            if return_query:
                return sql_query
            
            try:
                result=query_database(sql_query,printing=False)
            except QueryExecutionError:
                retries_left-=1
                print("Query not executable")
                result=None
            if not return_metadata:
                if evaluation and not forward:
                    return sql_query, semantic_dic, result
                elif evaluation and forward:
                    return initial_sql_query, semantic_dic, sql_query
                else:
                    if forward:
                        return sql_query
                    else:
                        return result
            else:
                if evaluation and not forward:
                    return sql_query, semantic_dic, result, usage_metadata_join
                elif evaluation and forward:
                    return initial_sql_query, semantic_dic, sql_query, usage_metadata_join
                else:
                    if forward:
                        return sql_query, usage_metadata_join
                    else:
                        return result, usage_metadata_join
