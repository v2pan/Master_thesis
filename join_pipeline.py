import sqlparse
import re
from row_calculus_pipeline import execute_queries_on_conditions,  update_metadata, get_context, get_relevant_tables
from other_gemini import ask_gemini, gemini_json
from database import query_database, QueryExecutionError
from extractor import extract
import copy


#Trying out to implement the Join WHERE multiple things are linked
#Creation of a dictionary to store the semantic pairs

def extract_join_conditions_sqlparse(sql_query: str):
    """
    Extracts JOIN conditions (equality joins only) using sqlparse.
    """
    try:
        parsed = sqlparse.parse(sql_query)[0]
        join_conditions = []

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
        return join_conditions, order
    except (IndexError, sqlparse.exceptions.ParseException) as e:
        print(f"Error parsing SQL query: {e}")
        return []
    

def compare_semantics_in_list(input_list,order):
    """
    Compares each unique item from the first list in each sublist against every element in the second list to find semantically equivalent expressions using gemini_json.

    Args:
        input_list (list of lists):  Each sublist contains [left_list, condition, right_list, original_expression].

    Returns:
        result_list (list of lists): A list where each sublist contains semantically equivalent expressions.
    """
    dict = {}
    #Iteration over all JOINs
    for outer_list in input_list:
        if isinstance(outer_list[0], list) and isinstance(outer_list[-1], list):
            temp_list1 = outer_list[0]
            temp_list2 = outer_list[-1]
            condition = outer_list[1]
            original_expression = outer_list[2]  # Access the original expression

            goal = ask_gemini(f"""Write out the goal for this clause in natural language. Focus on the
                            semantic meaning. {original_expression}. Be brief.
                            Input: 'WHERE person.id <> 2'
                            Output: Retrieve instances where the id of the person is not 2
                            Input : {original_expression}
                            Output:
                            """)
            print(f"The goal is: {goal}")

            phrase, temp_meta = ask_gemini(f"""Write the output in natural language and ignore possible numbers.
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
            update_metadata(temp_meta)
            print(f"The phrase is: {phrase}")

            same_meaning_list = []
            seen_items = set()  # Track unique items from temp_list1
            
            #Iteration over all items from one list
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

                #Get response from LL
                response = gemini_json(total_prompt, response_type=list[bool])
                relevant_items = [temp_list2[i][0] for i, is_relevant in enumerate(response) if is_relevant]
                #Add relevant semantic equivalents to the list
                dict[item_str] = relevant_items
    print(f"The key belongs to {order[0]}")
    print(f"The value belongs to {order[1]}")       

    return dict, order

def join_pipeline(query, return_query=False):


    #Get the relevant tables
    retries=4
    count=0
    while count<retries:
        tables = get_relevant_tables(query)
        
        if tables is not None:
            break
        else:
            count+=1
    if tables is None:
        re
    print(f"The relevant tables are {tables}")
    context = get_context(tables)

    #Gets context by reading JSON files
    #context= get_context_json(tables)


    #Used for relational calculus
    #response, temp_meta = ask_gemini(f"Convert the following query to SQL. Write this query without using the AS: : {query}. Do not use subqueries, but instead use INNER JOINS. Don't rename any of the tables in the query. For every colum reference the respective table. Do not use the Keyword CAST. The structure of the database is the following: {context}.", True,max_token=1000)

    #Used for predicate calculus, selecting all rows
    response, temp_meta = ask_gemini(f"Convert the following query to SQL. Write this query without using the AS: : {query}. Do not use subqueries, but instead use INNER JOINS. Don't rename any of the tables in the query. For every colum reference the respective table. Do not use the Keyword CAST. Select all rows by starting with 'SELECT * '  The structure of the database is the following: {context}.", True,max_token=1000)
    #Update the metadata
    update_metadata(temp_meta)

    sql_query = extract(response, start_marker="```sql",end_marker="```" )
    print(f"The SQL query is: {sql_query}")

    # Example usage
    join_conditions, order = extract_join_conditions_sqlparse(sql_query)
    print(join_conditions)
    new_list = execute_queries_on_conditions(join_conditions)
    print(new_list)
    #TODO: Multiple dictinoaries for multiple JOINs
    semantic_dic, order= compare_semantics_in_list(new_list, order)
    print(semantic_dic)

    #Final prompt for modification of the query
    final_prompt=f''' First reason on what value the CASE statement is necessary, if it is to be applied. Then write  an updated SQL query, if needed. Update the Join conditions using the CASE statement if necessary. The dictionary tells us which parts have the same meaning semantically and therefore should be treated equally when executed on a join.  Always end with a ';'. The key belongs to {order[0]}. The value belongs to {order[1]}.  Make sure to use the CASE statement on the KEY value and convert them to the corresponding value. Alway put the CASE statement after the ON statement. 
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
            Input: sql:{sql_query}; binding: {semantic_dic}; order: The key belongs to {order[0]}, The values belong to {order[1]};
            Output:'''
    print(f"The final prompt is \n {final_prompt}")

    retries_left=3
    while retries_left>0:

        # Try to modify the query with our chosen binding
        response,temp_meta = ask_gemini(final_prompt,True, max_token=1000)
        #Update the metadata
        update_metadata(temp_meta)
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
            return result

# sql_query = '''SELECT 
#     children_table.id, 
#     children_table.children, 
#     fathers.name
# FROM 
#     children_table
# INNER JOIN 
#     fathers ON fathers.id = children_table.id;'''

#calculus='''∃id (children_table(id, _) ∧ fathers(id, _))'''
#calculus='''∃id (children_table(id, _) ∧ fathers(id, 'German'))'''
calculus='''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )'''
print(join_pipeline(calculus))