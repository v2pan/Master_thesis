import sqlparse
import re
from row_calculus_pipeline_comparison import execute_queries_on_conditions,  update_metadata
from other_gemini import ask_gemini, gemini_json
from database import query_database
from extractor import extract


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

                # Process operands:
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

                join_conditions.append([left, operator, right])

        return join_conditions
    except (IndexError, sqlparse.exceptions.ParseException) as e:
        print(f"Error parsing SQL query: {e}")
        return []
    

def compare_semantics_in_list(input_list):
    """
    Compares each unique item from the first list in each sublist against every element in the second list to find semantically equivalent expressions using gemini_json.

    Args:
        input_list (list of lists):  Each sublist contains [left_list, condition, right_list, original_expression].

    Returns:
        result_list (list of lists): A list where each sublist contains semantically equivalent expressions.
    """
    dict = {}

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

            for item in temp_list1:
                item_str = item[0]
                if item_str in seen_items:
                    continue
                seen_items.add(item_str)

                total_prompt = f"Answer the following questions with True or False.\n"
                for other_item in temp_list2:
                    other_item_str = other_item[0]
                    prompt = f"'{item_str}' {phrase} '{other_item_str}' \n"  #Simplified prompt
                    total_prompt += prompt

                response = gemini_json(total_prompt, response_type=list[bool])
                relevant_items = [temp_list2[i][0] for i, is_relevant in enumerate(response) if is_relevant]
                dict[item_str] = relevant_items

    return dict

# Example usage
sql_query = '''SELECT 
    children_table.id, 
    children_table.children, 
    fathers.name
FROM 
    children_table
INNER JOIN 
    fathers ON fathers.id = children_table.id;'''
join_conditions = extract_join_conditions_sqlparse(sql_query)
print(join_conditions)
new_list = execute_queries_on_conditions(join_conditions)
print(new_list)
semantic_dic= compare_semantics_in_list(new_list)
print(semantic_dic)

# # Build the list of semantic pairs as a string
# semantic_rows = '\n'.join(f"{k}:{v}" for k, v in semantic_dic.items()) 

# print(semantic_rows)
final_prompt=f'''Write an updated SQL query. Update the Join conditions using the CAST statement if necessary. The dictionary tells us which parts have the same meaning semantically and therefore should be treated euqally when executed on a join.  Always end with a ';'.
        Input sql: SELECT suppliers.name, products.value FROM suppliers JOIN products ON suppliers.id = products.supplier_id; binding: {{'uno': ['one'], 'dos': ['two'], 'tres': ['three']}}
        Output: SELECT suppliers.name, products.value FROM suppliers JOIN products ON suppliers.id = CASE products.supplier_id
        WHEN 'uno' THEN 'one'
        WHEN 'dos' THEN 'two'
        WHEN 'tres' THEN 'three'
        END;
        Input sql: SELECT employees.fullname, departments.dept_name FROM employees JOIN departments ON employees.department_id = departments.id; binding: {{'Acme Corp': ['Acme Corp'], 'Sales Dep': ['Sales Department'], 'Engeneering': ['Engineering']}}
        Output: SELECT employees.fullname, departments.dept_name FROM employees JOIN departments ON employees.department_id = CASE departments.id
        WHEN 'Acme Corp' THEN 'Acme Corp'
        WHEN 'Sales Dep' THEN 'Sales Department'
        WHEN 'Engeneering' THEN 'Engineering'
        END;
        Input: sql:{sql_query}; binding: {semantic_dic}
        Output:'''
print(f"The final prompt is {final_prompt}")
# Try to modify the query with our chosen binding
response,temp_meta = ask_gemini(final_prompt,True, max_token=1000)
#Update the metadata
update_metadata(temp_meta)

print(f"The response is {response}")
try:
    sql_query = extract(response, start_marker="```sql",end_marker="```" )
    if sql_query is None:
        sql_query = extract(response, start_marker="SELECT",end_marker=";",inclusive=True )
except:
    pass
if sql_query is None:
    print("No SQL query found in response.")
else:
    print(f"The SQL query is: {sql_query}")
    result=query_database(sql_query)
if result:
        print(result)
