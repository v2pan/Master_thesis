import sqlparse
import re
from database import query_database
from other_gemini import gemini_json,ask_gemini
from extractor import extract

#Works great for this query:

sql2 = """
SELECT name, shares
FROM shareowner1row
INNER JOIN animalowner1row ON shareowner1row.id = animalowner1row.owner_id
WHERE animalowner1row.category = 'dog' animalowner1row.animalname = 'bill';
"""
    #However problems occurs when I have such a query
sql3='''SELECT name, shares
    FROM shareowner1row
    WHERE id IN (SELECT owner_id FROM animalowner1row WHERE category = 'dog' AND animalname='bill');'''
def extract_where_conditions_sqlparse(sql_query):
    """
    Extracts WHERE clause conditions using sqlparse. More robust than simple string parsing.
    """

    
    # Parse the SQL query and extract the first statement
    parsed = sqlparse.parse(sql_query)[0]
    where_clause = None

    # Look for the WHERE clause in the parsed SQL statement
    for token in parsed.tokens:
        if isinstance(token, sqlparse.sql.Where):
            where_clause = token
            break

    # If a WHERE clause is found, process the conditions
    if where_clause:
        conditions = []
        for token in where_clause.tokens:
            if isinstance(token, sqlparse.sql.Comparison):
                left = str(token.left)
                matches = re.findall(r"(\w+\.\w+)", left)

                # If no matches are found, continue to the next token
                if matches is None:
                    continue
                elif len(matches) == 1:
                    for match in matches:
                        column_name = match.split(".")[1]
                        table_name = match.split(".")[0]
                        # Create a SELECT statement for the column
                        left = f"SELECT {column_name} FROM {table_name};"

                # Append the condition with the left operand, operator, and right operand
                conditions.append([left, str(token.token_next(0)), str(token.right).replace("'", "")])

            elif isinstance(token, sqlparse.sql.IdentifierList):
                # Handle multiple conditions - this needs more sophistication for complex cases
                print("Warning: Multiple conditions or other complex WHERE clauses are not handled yet.")
                # You could expand this block for more sophisticated handling

        return conditions

    # If no WHERE clause found, return an empty list
    return []



conditions2 = extract_where_conditions_sqlparse(sql2)
print(f"The original list is {conditions2}")
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
    copy_list=conditions_list
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

# print(conditions2[0][0])
# print(conditions2[0][1])
# print(conditions2[0][2])

new_list=execute_queries_on_conditions(conditions2)
print(f"The new list is {new_list}")

def write_list_to_text_file(new_list, filename="output.txt"):
    """
    Writes the list of conditions (new_list) to a text file.

    Args:
    - new_list (list of lists): The list to write to the text file.
    - filename (str): The name of the text file to write the list into.
    """
    with open(filename, "w") as file:
        # Iterate through the list of lists
        for sublist in new_list:
            # Write each sublist as a string in the file
            file.write(str(sublist) + "\n")

# Example usage
new_list = execute_queries_on_conditions(conditions2)
write_list_to_text_file(new_list)

print("-----------------------------------------------------------------------------------")

def retrieve_values_from_text_file(filename="output.txt"):
    """
    Retrieves the conditions and their semantic meanings from the text file.

    Args:
    - filename (str): The name of the text file to read from.

    Returns:
    - result_list (list of lists): The parsed list of semantic expressions.
    """
    result_list = []
    
    with open(filename, "r") as file:
        # Read the file line by line
        for line in file:
            # Convert the string representation of each sublist back into a list
            sublist = eval(line.strip())  # Using eval to safely interpret the string as a list
            result_list.append(sublist)

    return result_list

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
            
            # Determine which part of the list is the string and which is the list, comparing them against on another
            # Cases where both are different not yet covered
            if type(outer_list[0]) == str:
                temp_string = outer_list[0]
                temp_list = outer_list[-1]
            else:
                temp_string = outer_list[-1]
                temp_list = outer_list[0] 

            print(f"temp_string: {temp_string}")
            print(f"temp_list: {temp_list}")

            # Compare the string with the items in the list using gemini_json
            same_meaning_list = []
            seen_items = set()  # To track items we've already added
            
            # Iterate over the items in temp_list and compare with temp_string
            for item in temp_list:
                # If item is identical to itself, skip
                if temp_string in item or item in seen_items:
                    continue
                
                #Actual logic, this is where the semantic binding occurs
                prompt = f"Does '{temp_string}' and '{item}' have the same semantic meaning?"
                response = gemini_json(prompt, response_type=bool)

                # If the response is True, add the item to the list
                if response:
                    same_meaning_list.append(item)
                    seen_items.add(item)  # Track this item as already processed
            
            # If there are any items that have the same meaning, add temp_string and the matching items to the result list
            if same_meaning_list:
                result_list.append([temp_string] + same_meaning_list)
    
    return result_list

# Example usage
retrieved_list = retrieve_values_from_text_file("output.txt")
print(f"The retrieved list is {type(retrieved_list[0][0])}")
semantic_list=compare_semantics_in_list(retrieved_list)
print(f"The semantics list is {semantic_list}")

# Build the list of semantic pairs as a string
semantic_rows = ''.join(f"{i}\n" for i in semantic_list)

# Use the result in the f-string
response = ask_gemini(
    f"Modify the SQL query {sql2} based on the assumption that the following expressions in each row have the same meaning:\n{semantic_rows}"
)

sql_query = extract(response, start_marker="```sql",end_marker="```" )
print(f"The final query is {sql_query}")
query_database(sql_query)



# def extract_where_conditions_sqlparse(sql_query):
#     """
#     Extracts WHERE clause conditions using sqlparse. More robust than simple string parsing.
#     """
#     # Parse the SQL query and extract the first statement
#     parsed = sqlparse.parse(sql_query)[0]
#     where_clause = None

#     # Look for the WHERE clause in the parsed SQL statement
#     for token in parsed.tokens:
#         if isinstance(token, sqlparse.sql.Where):
#             where_clause = token
#             break

#     # If a WHERE clause is found, process the conditions
#     if where_clause:
#         conditions = []
#         for token in where_clause.tokens:
#             if isinstance(token, sqlparse.sql.Comparison):
#                 left = str(token.left)
#                 matches = re.findall(r"(\w+\.\w+)", left)

#                 # If no matches are found, continue to the next token
#                 if matches is None:
#                     continue
#                 elif len(matches) == 1:
#                     for match in matches:
#                         column_name = match.split(".")[1]
#                         table_name = match.split(".")[0]
#                         # Create a SELECT statement for the column
#                         left = f"SELECT {column_name} FROM {table_name};"

#                 # Append the condition with the left operand, operator, and right operand
#                 conditions.append([left, str(token.token_next(0)), str(token.right).replace("'", "")])

#             elif isinstance(token, sqlparse.sql.IdentifierList):
#                 # Handle multiple conditions - this needs more sophistication for complex cases
#                 print("Warning: Multiple conditions or other complex WHERE clauses are not handled yet.")
#                 # You could expand this block for more sophisticated handling

#         return conditions

#     # If no WHERE clause found, return an empty list
#     return []

# sql2 = """
# SELECT name, shares
# FROM shareowner1row
# INNER JOIN animalowner1row ON shareowner1row.id = animalowner1row.owner_id
# WHERE animalowner1row.category = 'dog' animalowner1row.animalname = 'diego';
# """
# conditions2 = extract_where_conditions_sqlparse(sql2)
# print(f"The original list is {conditions2}")
# def execute_queries_on_conditions(conditions_list):
#     """
#     Executes `query_database` for each item in the list of conditions
#     that contains both 'SELECT' and 'FROM' in the string.
#     If a condition contains both 'SELECT' and 'FROM', it replaces the
#     condition in the original list with the result of `query_database`.
    
#     Args:
#     - conditions_list (list of lists): List of conditions to check.
    
#     Returns:
#     - The modified list
#     """
#     copy_list=conditions_list
#     # Iterate over each item in the list of conditions
#     for outer_index, list_outer in enumerate(copy_list):
#         for inner_index, item in enumerate(list_outer):
            
#             # Check if the condition contains both "SELECT" and "FROM"
#             if isinstance(item, str) and 'SELECT' in item and 'FROM' in item:
#                 # Execute the query if it contains the correct keywords
#                 query_result = query_database(item,False)
                
#                 # Replace the condition with the query result
#                 copy_list[outer_index][inner_index] = query_result
#     return copy_list

# # print(conditions2[0][0])
# # print(conditions2[0][1])
# # print(conditions2[0][2])

# new_list=execute_queries_on_conditions(conditions2)
# print(f"The new list is {new_list}")

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

# # Example usage
# new_list = execute_queries_on_conditions(conditions2)
# write_list_to_text_file(new_list)






# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
#Here the results from the 18th November end




# def extract_column_queries(sql_query):
#   """Extracts SELECT queries for each column with a dot (.) in the SQL query.

#   Args:
#     sql_query: The SQL query string.

#   Returns:
#     list: A list of SELECT queries for each column with a dot.
#   """

#   column_queries = {}
#   matches = re.findall(r"(\w+\.\w+)", sql_query)
#   for match in matches:
#     column_name = match.split(".")[1]
#     table_name = match.split(".")[0]
#     column_queries[f"{table_name}.{column_name}"]=f"SELECT {column_name} FROM {table_name};"
#   return column_queries



# # Example usage:
# sql_query = """
# SELECT name, shares
# FROM shareowner1row
# INNER JOIN animalowner1row ON shareowner1row.id = animalowner1row.owner_id
# WHERE animalowner1row.category = 'dog';
# """

# #Trying to manually extract the necessary rows and columns
# column_queries = extract_column_queries(sql_query)
# print(f"Column Queries: {column_queries}")

# #Put unique values into the dictionary  
# for key,value in column_queries.items():
#     query_database(value,True)
#     column_queries[key]=query_database(value)

# print(f"Column Queries: {column_queries}")

# def extract_words_around_equals(sql_query):
#     """Extracts words left and right of '=' signs in an SQL query.

#     Args:
#         sql_query: The SQL query string.

#     Returns:
#         list: A list of lists, where each inner list contains the words left and right of an '='.
#     """

#     #How then translate the matches to a soft binding?????ẞ
#     words_around_equals = []
#     matches = re.findall(r"(\w+\.\w+)\s*=\s*(\w+\.\w+)", sql_query)
#     for match in matches:
#         print(match[0])
#         words_around_equals.append([match[0], match[1]])
#     return words_around_equals

# words = extract_words_around_equals(sql_query)
# print(f"Words around equals signs: {words}")