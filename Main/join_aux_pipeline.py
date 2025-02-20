import sqlparse
import re
from Main.row_calculus_pipeline import execute_queries_on_conditions,  get_context, get_relevant_tables
from Utilities.llm import ask_llm, llm_json, add_metadata, RessourceError
from Utilities.database import query_database, QueryExecutionError
from Utilities.extractor import extract
import copy
import time



#Metadata to keep track of use for the JOIN pipeline
usage_metadata_join = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }


#Trying out to implement the Join WHERE multiple things are linked
#Creation of a dictionary to store the semantic pairs

def extract_join_conditions_sqlparse(sql_query: str):
    """
    Extracts JOIN conditions (equality joins only) using sqlparse.
    """
    try:
        parsed = sqlparse.parse(sql_query)[0]
        join_conditions = []
        order_list=[]
        for token in parsed.tokens:
            if isinstance(token, sqlparse.sql.Comparison):

                # Extract join condition (assuming equality join only)
                left = str(token.left).strip()
                right = str(token.right).strip()
                operator = str(token.token_next(0)).strip() # Get the operator token
                comp=str(token.normalized).strip()
                #Order to keep track of what is on the left and right side of the join
                order = [copy.deepcopy(left), copy.deepcopy(right)]

                # Process operands to get SQL queries:
                left_is_column = re.fullmatch(r'\w+\.\w+', left)
                if left_is_column:
                    table_name, column_name = left.split('.')
                    left = f"SELECT {column_name} FROM {table_name};"

                right_is_column = re.fullmatch(r'\w+\.\w+', right)
                if right_is_column:
                    table_name, column_name = right.split('.')
                    right = f"SELECT {column_name} FROM {table_name};"
                else:
                    right = right.replace("'", "")  # Remove quotes from literals

                join_conditions.append([left, operator, comp,  right])
                order_list.append(order)
        return join_conditions, order_list
    except (IndexError, sqlparse.exceptions.ParseException) as e:
        print(f"Error parsing SQL query: {e}")
        return []
    

def compare_semantics_in_list(input_list,order):
    """
    Compares each unique item from the first list in each sublist against every element in the second list to find semantically equivalent expressions using llm_json.

    Args:
        input_list (list of lists):  Each sublist contains [left_list, condition, right_list, original_expression].

    Returns:
        result_list (list of lists): A list where each sublist contains semantically equivalent expressions.
    """
    dict_list = []
    #Iteration over all JOINs
    counter=0
    for outer_list in input_list:
        if isinstance(outer_list[0], list) and isinstance(outer_list[-1], list):
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

                phrase, temp_meta = ask_llm(f"""Write the output in natural language and ignore possible numbers.
                                Input: (2, <Comparison '<' at 0x75D1C85F0A00>)
                                Output: is smaller than
                                Input: (2, <Comparison '!=' at 0x75D1C85F0A00>)
                                Output: has a different meaning than
                                Input: (2, <Comparison '<>' at 0x75D1C85F0A00>)
                                Output: has a different meaning than
                                Input: (2, <Comparison '=' at 0x75D1C85F0A00>)
                                Output: has the same meaning as (also in another language) or is the same as
                                Input:{condition}.
                                Output:""", True, max_token=100)
                #Update the metadata
                _=add_metadata(temp_meta, usage_metadata_join)
                #add_metadata(temp_meta)
                print(f"The phrase is: {phrase}")

                same_meaning_list = []
                seen_items = set()  # Track unique items from temp_list1
                
                #Iteration over all items from one list
                type1=type(item)
                type2=type(temp_list1[0])
                prompt=f'''-- Create the intermediary table
                CREATE TABLE intermediary_table (
                expr1 VARCHAR(255),  -- 
                expr2 VARCHAR(255)  -- 
                );'''
                for item in temp_list1:
                    item_str = item[0]
                    if item_str in seen_items:
                        continue
                    seen_items.add(item_str)

                    total_prompt = f"Answer the following questions with True or False.\n"

                    #Iteation over all items from another list
                    for other_item in temp_list2:
                        other_item_str = other_item[0]
                        prompt = f"'{item_str}' {phrase} '{other_item_str}' \n"  #Simplified prompt
                        total_prompt += prompt

                    #Get response from LLM
                    json_success=False
                    while not json_success:
                        try:
                            response, temp_meta = llm_json(total_prompt, response_type=list[bool], return_metadata=True)
                            json_success=True
                        except RessourceError:
                            print(f"Resource Error occured in Join Pipeline JSON")
                            time.sleep(60)
                    _=add_metadata(temp_meta, usage_metadata_join)


                    relevant_items = [temp_list2[i][0] for i, is_relevant in enumerate(response) if is_relevant]
                
                    #Add relevant semantic equivalents to the list
                    db_tuple=()
                    for i in relevant_items:
                        db_tuple+=(item,i)
                    
                    for tuple in db_tuple:
                        query_database(f"INSERT INTO intermediary_table (expr1, expr2) VALUES {tuple}")
                    

                print(f"The key belongs to {order[counter][0]}")
                print(f"The value belongs to {order[counter][1]}")     
                dict_list.append(dict)
                #Increase counter
                counter+=1
            else:
                dict_list.append(dict)
         

    return dict_list, order

def join_pipeline(initial_sql_query, return_query=False, evaluation=False, forward=False, return_metadata=False):


    # #Get the relevant tables
    # retries=4
    # count=0
    # while count<retries:
    #     tables = get_relevant_tables(query)
        
    #     if tables is not None:
    #         break
    #     else:
    #         count+=1
    # if tables is None:
    #     re
    # print(f"The relevant tables are {tables}")
    # context = get_context(tables)

    # #Gets context by reading JSON files
    # #context= get_context_json(tables)


    # #Used for relational calculus
    # #response, temp_meta = ask_llm(f"Convert the following query to SQL. Write this query without using the AS: : {query}. Do not use subqueries, but instead use INNER JOINS. Don't rename any of the tables in the query. For every colum reference the respective table. Do not use the Keyword CAST. The structure of the database is the following: {context}.", True,max_token=1000)

    # #Used for predicate calculus, selecting all rows
    # response, temp_meta = ask_llm(f"Convert the following query to SQL. Write this query without using the AS: : {query}. Do not use subqueries, but instead use INNER JOINS. Don't rename any of the tables in the query. For every colum reference the respective table. Do not use the Keyword CAST. Select all rows by starting with 'SELECT * '  The structure of the database is the following: {context}.", True,max_token=1000)
    # #Update the metadata
    # add_metadata(temp_meta)

    # initial_sql_query = extract(response, start_marker="```sql",end_marker="```" )
    # print(f"The SQL query is: {initial_sql_query}")

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
    semantic_dic, order= compare_semantics_in_list(new_list, order)
    print(semantic_dic)
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

    #Create the binding string for, necessary for multiple JOINs
    binding_str = ""
    for i in range(len(semantic_dic)):
        binding_str += f"binding {i}: {semantic_dic[i]}. The key belongs to {order[i][0]}, The values belong to {order[i][1]}\n"
    #Final prompt for modification of the query
    if len(semantic_dic)<2:
        final_prompt=f''' First reason on what value the CASE statement is necessary, if it is to be applied. Then write  an updated SQL query, if needed. Update the Join conditions using the CASE statement if necessary. The dictionary tells us which parts have the same meaning semantically and therefore should be treated equally when executed on a join.  Always end with a ';'. The key belongs to {order[0][0]}. The value belongs to {order[0][1]}.  Make sure to use the CASE statement on the KEY value and convert them to the corresponding value. Alway put the CASE statement after the ON statement. Make sure the tables and the attributes on which the JOIN is performed are not changed, instead if necessary add CASE statements.
            Input sql: SELECT suppliers.name, products.value FROM suppliers JOIN products ON suppliers.id = products.supplier_id; binding: {{'uno': ['one'], 'dos': ['two'], 'tres': ['three']}}; order: The key belongs to products.supplier_id, The values belong to suppliers.id.
            Output: SELECT suppliers.name, products.value FROM suppliers JOIN products ON suppliers.id = CASE products.supplier_id
            WHEN 'uno' THEN 'one'
            WHEN 'dos' THEN 'two'
            WHEN 'tres' THEN 'three'
            END;
            Input sql: SELECT employees.fullname, departments.dept_name FROM departments JOIN employees ON departments.id  = employees.department_id; binding: {{'Acme Corp': ['Acme Corp'], 'Sales Dep': ['Sales Department'], 'Engeneering': ['Engineering']}}; order: The key belongs to departments.id, The values belong to employees.department_id.
            Output: SELECT employees.fullname, departments.dept_name FROM employees JOIN departments ON employees.department_id = CASE departments.id
            WHEN 'Acme Corp' THEN 'Acme Corp'
            WHEN 'Sales Dep' THemployees.department_idEN 'Sales Department'
            WHEN 'Engeneering' THEN 'Engineering'
            END;
            Input: sql:{initial_sql_query}; binding: {semantic_dic[0]}; order: The key belongs to {order[0][0]}, The values belong to {order[0][1]};
            Output:'''
    
    #If multiple JOINs are present, the prompt is different, different problem as important what is substituted by what
    else:
        final_prompt=f''' Reason about in what position the CASE statement for modifying the JOIN would make sense. Then write an updated SQL query, if needed. The dictionary tells us which parts have the same meaning semantically and therefore should be treated equally when executed on a join.  Always end with a ';'.  Foe each non-empty dictionary add the CASE statement only to the corresponding JOIN. Think aboout how you could place the CASE statement such that it doesn't have to be applied multiple times, when applying once cleverly would be enough. Alway put the CASE statement after the ON statement. Think about whether it makes sense to substitute the key by the value or the value by the key.Dont JOIN the same attribute with itself please, always join two different attributes.  Make sure the tables and the attributes on which the JOIN is performed are not changed, instead if necessary add CASE statements. 
                Input: SELECT students.name, courses.title 
                FROM students 
                JOIN enrollments ON students.id = enrollments.student_id 
                JOIN courses ON enrollments.course_id = courses.id;
                binding 1: {{'CS101': ['Introduction to Computer Science'], 'MATH201': ['Calculus II']}}; The key belongs to courses.id, The values belong to enrollments.course_id.
                binding 2: {{}}. The key belongs to enrollments.student_id. The value belongs to student_id.
                Output: SELECT students.name, courses.title FROM students JOIN enrollments ON students.id = enrollments.student_id JOIN courses ON enrollments.course_id = CASE courses.id WHEN 'CS101' THEN 'Introduction to Computer Science' WHEN 'MATH201' THEN 'Calculus II' END;
                Input: SELECT *
                FROM widgets
                INNER JOIN gizmos ON widgets.part_id = gizmos.id
                INNER JOIN sprockets ON widgets.part_id = sprockets.id;
                binding1: {{1: ['Gear A'], 2: ['Gear B'], 3: ['Gear C']}}; The key belongs to widgets.part_id, The values belong to gizmos.id.
                binding 2: {{}}; The key belongs to widgets.sprocket_id, The values belong to sprockets.id.
                Output: SELECT * 
                FROM widgets 
                INNER JOIN gizmos ON widgets.part_id = CASE gizmos.id 
                                                        WHEN 'Gear A' THEN 1 
                                                        WHEN 'Gear B' THEN 2 
                                                        WHEN 'Gear C' THEN 3 
                                                        ELSE NULL  -- Add NULL in else clause
                                                    END
                INNER JOIN sprockets ON widgets.sprocket_id = sprockets.id;
                Input: sql:{initial_sql_query}; 
                binding: {binding_str};
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


# sql_query = '''SELECT 
#     children_table.id, 
#     children_table.children, 
#     fathers.name
# FROM 
#     children_table
# INNER JOIN 
#     fathers ON fathers.id = children_table.id;'''

#calculus='''∃id (children_table(id, _) ∧ fathers(id, _))'''
#calculus='''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )'''
# calculus='''∃d (weather(d, city, temperature, rainfall) ∧ website_visits(d, page, visits)'''
# print(join_pipeline(calculus))