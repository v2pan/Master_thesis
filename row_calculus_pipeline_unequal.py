import os
from database import query_database
from extractor import extract
from other_gemini import ask_gemini, gemini_json, QUERY, CATEGORY
import sqlparse
import re
from database import query_database
from other_gemini import gemini_json,ask_gemini
from extractor import extract
import copy

#Metadata to keep track of use 

def get_context(tables):
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    combined_context = ""

    for t in tables:
        context_text = ""
        
        # Define file paths for content and context
        context_file_path = os.path.join(current_directory, 'saved_info', f'{t}_context.txt')

        # Check if content and context files already exist
        if os.path.exists(context_file_path):
            with open(context_file_path, 'r') as context_file:
                context_text = context_file.read()
        else:
            # SQL query for schema (context) with constraints
            unique = f'''SELECT 
                c.column_name,
                c.is_nullable,
                c.data_type,
                constraints.constraint_type
            FROM 
                information_schema.columns c
            LEFT JOIN (
                SELECT 
                    kcu.column_name,
                    tc.constraint_type
                FROM 
                    information_schema.table_constraints tc
                JOIN 
                    information_schema.key_column_usage kcu
                ON 
                    tc.constraint_name = kcu.constraint_name
                WHERE 
                    tc.table_name = '{t}'
            ) AS constraints 
            ON c.column_name = constraints.column_name
            WHERE 
                c.table_name = '{t}';
            '''

            # SQL query to get column names in the correct order
            column_names_query = f'''SELECT 
                c.column_name
            FROM 
                information_schema.columns c
            WHERE 
                c.table_name = '{t}'
            ORDER BY 
                c.ordinal_position;
            '''

            # Fetch data from the database
            cond = query_database(unique, False)
            column_names = query_database(column_names_query, False)  # Assuming query_database returns results as strings
            
            # Convert column names to a formatted string for the context
            column_names_text = "\n".join([col[0] for col in column_names])  # Assuming `query_database` returns list of tuples (col_name, ...)

            # Combine schema information and column names
            with open(context_file_path, 'w') as context_file:
                context_file.write(f"The name of the table is {t}\n\n")
                context_file.write(f"Columns in the table {t} (in correct order):\n{column_names_text}\n\n")
                context_file.write(f"Schema Information:\n{str(cond)}")
            
            context_text = f"The name of the table is {t}\n\n"
            context_text += f"Columns in the table {t} (in correct order):\n{column_names_text}\n\n"
            context_text += f"Schema Information:\n{str(cond)}"

        # Append each table's context and content to the main text
        combined_context += f"{context_text}\n"


    #print(f"The combined descriptive text is:\n {combined_text}")
    print("--------------------")
    
    # Final combination of descriptive texts, with inter-table relationships
    '''final_text = ask_gemini(
        f"Combine and describe the relationships between the following tables if necessary. {combined_text}"
    )'''

    return combined_context  # Return the combined descriptive text for all tables

#Retrieve the context from the saved JSON files
def get_context_json(tables):
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    combined_context = ""

    for t in tables:
        context_text = ""
        
        # Define file paths for content and context
        context_file_path = os.path.join(current_directory, 'saved_json', f'{t}.json')

        # Check if content and context files already exist
        if os.path.exists(context_file_path):
            with open(context_file_path, 'r') as context_file:
                context_text = context_file.read()
        else:
            print(f"The data for table {t} is not available in JSON format.")

        # Append each table's context and content to the main text
        combined_context += f"For the table {t}\n{context_text}\n"
    
    return combined_context  # Return the combined descriptive text for all tables

def extract_where_conditions_sqlparse(sql_query):
    """
    Extracts WHERE clause conditions, handling both left and right operands.  More robust than simple string parsing.
    """
    try:
        parsed = sqlparse.parse(sql_query)[0]
        where_clause = None
        for token in parsed.tokens:
            if isinstance(token, sqlparse.sql.Where):
                where_clause = token
                break

        if where_clause:
            conditions = []
            for token in where_clause.tokens:
                where_clause_str = str(where_clause).strip()
                if isinstance(token, sqlparse.sql.Comparison):
                    left = str(token.left).strip()
                    right = str(token.right).strip()
                    operator = str(token.token_next(0)).strip()

                    #Process Left Operand
                    left_is_column = re.fullmatch(r'\w+\.\w+', left)  # More robust column check
                    if left_is_column:
                        table_name, column_name = left.split('.')
                        left = f"SELECT {column_name} FROM {table_name};"
                    
                    # Process Right Operand
                    right_is_column = re.fullmatch(r'\w+\.\w+', right) # More robust column check
                    if right_is_column:
                        table_name, column_name = right.split('.')
                        right = f"SELECT {column_name} FROM {table_name};"
                    else:
                        #Handle literal values (remove quotes)
                        right = right.replace("'", "")

                    print(where_clause.get_name)
                    conditions.append([left, operator,where_clause_str, right])
                elif isinstance(token, sqlparse.sql.IdentifierList):
                    print("Warning: Complex IdentifierList in WHERE clause not fully handled.")

            return conditions
        else:
            return [] #No WHERE clause found.
    except (IndexError, sqlparse.exceptions.ParseException) as e:
        print(f"Error parsing SQL query: {e}")
        return [] #Return empty list on parse error.

def execute_queries_on_conditions(conditions_list):
    """
    Executes `query_database` for each item in the list of conditions
    that contains both 'SELECT' and 'FROM' in the string.
    If a condition contains both 'SELECT' and 'FROM', it replaces the
    condition in the original list with the result of `query_database`.
    
    Args:
    - conditions_list (list of lists): List of conditions to check.
    
    Returns:
    - The modified list
    """
    copy_list=copy.deepcopy(conditions_list)
    # Iterate over each item in the list of conditions
    for outer_index, list_outer in enumerate(copy_list):
        for inner_index, item in enumerate(list_outer):
            
            # Check if the condition contains both "SELECT" and "FROM"
            if isinstance(item, str) and 'SELECT' in item and 'FROM' in item:
                # Execute the query if it contains the correct keywords
                query_result = query_database(item,False)
                
                # Replace the condition with the query result
                copy_list[outer_index][inner_index] = query_result
    return copy_list




def compare_semantics_in_list(input_list):
    """
    Compare each pair of expressions in a sublist to determine if they have the same semantic meaning
    using the gemini_json function. 

    Args:
    - input_list (list of lists): The input list of expressions and comparisons.

    Returns:
    - result_list (list of lists): A list of lists where each sublist contains expressions with the same semantic meaning.
    """
    result_list = []  # We will build this list to store the results
    
    # Iterate over each sublist in the input list
    for outer_list in input_list:
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
            print(type(condition))
            phrase=ask_gemini(f'''Write the output out in natural languge and ignore possible numbers
                              Input: (2, <Comparison '<' at 0x75D1C85F0A00>)
                              Output: is smaller than
                              Input: (2, <Comparison '<>' at 0x75D1C85F0A00>)
                              Output: does not have the same meaning as (also in antoher language)
                              Input: (2, <Comparison '=' at 0x75D1C85F0A00>)
                              Output: has the same meaning as (also in antoher language)
                              Input:{condition}.
                              Output:''')
            print(f"The phrase is:\n {phrase}. ")

            print(f"temp_string: {temp_string}")
            print(f"temp_list: {temp_list}")

            # Compare the string with the items in the list using gemini_json
            same_meaning_list = []
            seen_items = set()  # To track items we've already added
            
            # Iterate over the items in temp_list and compare with temp_string
            for item in temp_list:
                
                # # If item is identical to itself, skip
                # if temp_string in item or item in seen_items:
                #     continue
                
                #Actual logic, this is where the semantic binding occurs
                if left:
                    prompt = f"'{temp_string}  {phrase} {item}'"
                else:
                    prompt = f" '{item}  {phrase} {temp_string}'"
                gemini_prompt=ask_gemini(f''' Reformulate the following prompt to natural lagnuage if necessary {prompt}.
                                        Input: " '('two',)  is bigger than \n 9
                                        Output: "two is bigger than 9
                                        Input: {prompt}
                                        Output:''')
                response = gemini_json(gemini_prompt, response_type=bool)

                # If the response is True, add the item to the list
                if response:
                    same_meaning_list.append(item)
                    seen_items.add(item)  # Track this item as already processed
            #Appending the Where clause to the list
            same_meaning_list.append(outer_list[-2])  # Add the original string to the list
            # If there are any items that have the same meaning, add temp_string and the matching items to the result list
            if same_meaning_list:
                result_list.append( same_meaning_list)
    
    return result_list



def row_calculus_pipeline(query, tables):
    # Generate context by writing or reading tables' info
    #Gets context by querying database
    context = get_context(tables)

    #Gets context by reading JSON files
    #context= get_context_json(tables)

    print(f"The context is {context}")
    print(f"The query is {query}")

    response = ask_gemini(f"Convert the following query to SQL. Write this query without using the AS: : {query}. Do not use subqueries, but instead use INNER JOINS. Don't rename any of the tables in the query. For every colum reference the respective table. The structure of the database is the following: {context}.")
    #print(f"The response query is:\n {response}")
    sql_query = extract(response, start_marker="```sql",end_marker="```" )
    print(f"The SQL query is: {sql_query}")

    conditions2 = extract_where_conditions_sqlparse(sql_query)
    new_list = execute_queries_on_conditions(conditions2)
    # Example usage
    semantic_list=compare_semantics_in_list(new_list)
    print(f"The semantics list is {semantic_list}")

    # Build the list of semantic pairs as a string
    semantic_rows = ''.join(f"{i}\n" for i in semantic_list)

    final_prompt=f'''Write an updated SQL query like this, only using equalities. Only return the updated query. USE only the binding variables like written in bidning.
        Input: sql:SELECT name, hair FROM person WHERE person.bodypart='eyes'; binding :[('ojos',), ('augen',), 'WHERE person.bodypart ='eyes';']
        Output: SELECT name, hair FROM person WHERE person.bodypart = 'ojos' OR person.bodypart = 'augen';
        Input: sql:{sql_query} binding: {semantic_rows}
        Output:'''
    print(f"The final prompt is {final_prompt}")
    # Try to modify the query with our chosen binding
    response = ask_gemini(final_prompt)
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
        query_database(sql_query)
    

#Shareowner and Animalowner examples with equality
#calculus='''{name, shares | ∃id (SHAREOWNER1ROW(id, name, shares) ∧ ANIMALOWNER1ROW(id , _, 'dog'))}'''
#row_calculus_pipeline(calculus, ['shareowner1row', 'animalowner1row'])
calculus='''{name, shares | ∃id (SHAREOWNER(id, name, shares) ∧ ANIMALOWNER(id , _, 'dog'))}'''
row_calculus_pipeline(calculus, ['shareowner', 'animalowner'])

#Negation example
#calculus = '''{name, shares | ∃id (SHAREOWNER(id, name, shares) ∧ ¬ANIMALOWNER(id, _, 'dog'))}'''
#row_calculus_pipeline(calculus, ['shareowner', 'animalowner'])

#Doctors example with inequality
#calculus='''{id, name, patients_pd | doctors(id, name, patients_pd) ∧ patients_pd < 12}'''
#row_calculus_pipeline(calculus, ['doctors'])
# ----------------------------------------------------
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Only used for testing purposes
# def write_list_to_text_file(new_list, filename="output.txt"):
#     """
#     Writes the list of conditions (new_list) to a text file.

#     Args:
#     - new_list (list of lists): The list to write to the text file.
#     - filename (str): The name of the text file to write the list into.
#     """
#     with open(filename, "w") as file:
#         # Iterate through the list of lists
#         for sublist in new_list:
#             # Write each sublist as a string in the file
#             file.write(str(sublist) + "\n")

# def retrieve_values_from_text_file(filename="output.txt"):
#     """
#     Retrieves the conditions and their semantic meanings from the text file.

#     Args:
#     - filename (str): The name of the text file to read from.

#     Returns:
#     - result_list (list of lists): The parsed list of semantic expressions.
#     """
#     result_list = []
    
#     with open(filename, "r") as file:
#         # Read the file line by line
#         for line in file:
#             # Convert the string representation of each sublist back into a list
#             sublist = eval(line.strip())  # Using eval to safely interpret the string as a list
#             result_list.append(sublist)

#     return result_list