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
usage_metadata_total = {
            "prompt_token_count": 0,
            "candidates_token_count": 0,
            "total_token_count": 0,
            "total_calls": 0
        }

#Function to update metadata
def update_metadata(metadata):
    """
    Updates the usage metadata with the values from the input metadata dictionary.

    Args:
    - metadata (dict): The metadata dictionary to update the usage metadata with.
    """
    global usage_metadata_total
    usage_metadata_total["prompt_token_count"] += metadata["prompt_token_count"]
    usage_metadata_total["candidates_token_count"] += metadata["candidates_token_count"]
    usage_metadata_total["total_token_count"] += metadata["total_token_count"]
    usage_metadata_total["total_calls"] += 1


#Automatic retrieval of relevant tables from the database
retries = 4
def get_relevant_tables(calculus ):
    """
    Retrieves relevant tables from a database, handling retries and potential errors.

    Args:
        calculus: The expression to check against.
        retries: The number of retry attempts if tables cannot be found.

    Returns:
        A list of relevant table names if found, otherwise None.
    """
    #Get information on all tables in the database
    prompt = """SELECT table_name 
               FROM information_schema.tables
               WHERE table_schema = 'public' AND table_type = 'BASE TABLE';"""
    retries = 4
    count = 0
    while count < retries:
        try:
            #Get all tables
            result = query_database(prompt, printing=False)  

            # Extract table names:
            table_names = [row[0] for row in result]

            #Prompt construction for LLM to access relevance
            input_prompt = f"Return a list of length {len(table_names)} one answer for each question. \n"
            for table_name in table_names:
                input_prompt += f"Does table '{table_name}' occur in the expression '{calculus}'?  \n"

            #Three attempts to get correct amount of answer for the LLM
            attemps=4
            while attemps>0:
                #Extracting relevant tables by asking LLM boolean calls
                categories = gemini_json(prompt=input_prompt, response_type=list[bool])

                if len(table_names)!=len(categories):
                    print("Error: Tables do not have the same length.")
                    attemps-=1
                else:
                    break

            relevant_tables = [table_names[i] for i, is_relevant in enumerate(categories) if is_relevant]
            
            return relevant_tables  #Return tables if successfully found

        except Exception as e:  # Catch potential errors (e.g., database connection issues)
            count += 1
            print(f"Attempt {count+1}/{retries} failed: {e}. Retrying...")

    #If maximun is exceeded
    print(f"Exceeded maximum retries ({retries}). Could not find relevant tables.")
    return None

#Function to get the context of each table like constraints, schema, column names etc.
def get_context(tables):
    """
    Retrieves schema information (column names, data types, nullability, constraints) for specified tables from a database.

    Args:
        tables: A list of table names (strings).

    Returns:
        A string containing the combined schema information for all tables.  Information for each table is separated by newline characters.  If context for a table already exists in a file (see below), it reads the file content. Otherwise, it queries the database and saves that information.
    
    Notes:
        This function assumes the existence of a `query_database` function (not shown here) that takes an SQL query and a boolean value as input and returns the query result.
        The function expects files named "<table_name>_context.txt" in a subdirectory "saved_info" in the same directory as the script.  It will save context information to these files if the files do not exist.
    """
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

    return combined_context  # Return the combined descriptive text for all tables

#Retrieve the context from the saved JSON files
def get_context_json(tables):
    """
    Retrieves schema information for specified tables from JSON files.

    Args:
        tables: A list of table names (strings).

    Returns:
        A string containing the combined schema information for all tables. The information for each table is separated by newline characters.  If a JSON file for a table is not found, a message indicating that the data is not available will be included in the output string.  Returns an empty string if no tables are provided.

    Notes:
        This function expects JSON files named "<table_name>.json" in a subdirectory "saved_json" relative to the location of this script.  The content of each JSON file should represent the schema information for the corresponding table.  Error handling is minimal; it only prints a message if a file is not found but continues to process other tables.
    """
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


#Function to extract WHERE conditions from SQL query
def extract_where_conditions_sqlparse(sql_query):
    """
    Extracts WHERE clause conditions from an SQL query string, processing comparisons and handling potential errors.

    Args:
        sql_query: The SQL query string to parse.

    Returns:
        A list of lists, where each inner list represents a WHERE clause condition and contains:
            - The left operand (as an SQL SELECT statement if it's a column reference, otherwise the original string).
            - The comparison operator.
            - The entire WHERE clause string
            - The right operand (as an SQL SELECT statement if it's a column reference, otherwise the original string, with quotes removed if it's a literal).

        Returns an empty list if no WHERE clause is found or if an error occurs during parsing.  Prints a warning if a complex IdentifierList is encountered in the WHERE clause.
    """
    try:
        parsed = sqlparse.parse(sql_query)[0]
        where_clause = None
        #Iterate over all tokens
        for token in parsed.tokens:
            if isinstance(token, sqlparse.sql.Where): #Check if is a WHERE clause
                where_clause = token
                break

        if where_clause:
            conditions = [] # List to store conditions of WHERE clause
            for token in where_clause.tokens:
                where_clause_str = str(where_clause).strip()
                if isinstance(token, sqlparse.sql.Comparison):
                    left = str(token.left).strip() #Left part
                    right = str(token.right).strip() #Right part
                    operator = str(token.token_next(0)).strip() #Operator

                    #Process Left Operand to SQL query
                    left_is_column = re.fullmatch(r'\w+\.\w+', left)  
                    if left_is_column:
                        table_name, column_name = left.split('.')
                        left = f"SELECT {column_name} FROM {table_name};"
                    
                    # Process Right Operand to SQL query
                    right_is_column = re.fullmatch(r'\w+\.\w+', right) # More robust column check
                    if right_is_column:
                        table_name, column_name = right.split('.')
                        right = f"SELECT {column_name} FROM {table_name};"
                    else:
                        #Handle literal values (remove quotes)
                        right = right.replace("'", "")

                    print(where_clause.get_name)
                    #Add to list of conditions
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
            goal,temp_meta=ask_gemini(f'''Write out the goal for this clause in natural language. Focus on the
                            semantic meaning. {outer_list[-2]}. Be brief.
                            Input: 'WHERE person.id <> 2'
                            Output: Retrieve instances where the id of the person is not 2
                            Input : {outer_list[-2]}
                            Output:
                            ''', True, max_token=100)
            print(f"The goal is {goal}")
            update_metadata(temp_meta)
            #Ask LLM to generate a phrase for the comparison
            phrase,temp_meta=ask_gemini(f'''Write the output out in natural languge and ignore possible numbers
                              Input: (2, <Comparison '<' at 0x75D1C85F0A00>)
                              Output: is smaller than
                              Input: (2, <Comparison '!=' at 0x75D1C85F0A00>)
                              Output: has a different meaning than
                              Input: (2, <Comparison '<>' at 0x75D1C85F0A00>)
                              Output: has a different meaning than
                              Input: (2, <Comparison '=' at 0x75D1C85F0A00>)
                              Output: has the same meaning as (also in antoher language) or is the same as
                              Input:{condition}.
                              Output:''',True, max_token=100)
            
            #Update the metadata
            update_metadata(temp_meta)
            print(f"The phrase is:\n {phrase}. ")

            print(f"temp_string: {temp_string}")
            print(f"temp_list: {temp_list}")

            # Compare the string with the items in the list using gemini_json
            soft_binding_list = []
            #

            #Final prompt with list
            total_prompt=f"Answer the following questions with True or False. \n"
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
            response = gemini_json(total_prompt, response_type=list[bool])

            #Check if response has same length
            if len(response)!=len(temp_list):
                print("Error")
                print("The response and the temp_list have different lengths")
                print(f"The response is {response}")
                print(f"The temp_list is {temp_list}")
                break

            #Retrieve the relevant items
            relevant_items = [temp_list[i] for i, is_relevant in enumerate(response) if is_relevant]
            for i in relevant_items:
                soft_binding_list.append(i)

            #Add the where clause
            soft_binding_list.append(outer_list[-2]) 
            # If there are any items that have the same meaning, add temp_string and the matching items to the result list
            if soft_binding_list:
                result_list.append(soft_binding_list)
    
    return result_list


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
    response, temp_meta = ask_gemini(f"Convert the following query to SQL. Write this query without using the AS: : {query}. Do not use subqueries, but instead use INNER JOINS. Don't rename any of the tables in the query. For every colum reference the respective table. Do not use the Keyword CAST. Select all rows by starting with 'SELECT * '  The structure of the database is the following: {context}.", True,max_token=1000)
    
    #Update the metadata
    update_metadata(temp_meta)

    #Extract the SQL query from the response
    sql_query = extract(response, start_marker="```sql",end_marker="```" )
    print(f"The SQL query is: {sql_query}")

    #INNER LOGIC: Analyze SQL query, retrieve necessary items to retrieve, compare them using the LLM
    conditions = extract_where_conditions_sqlparse(sql_query)
    query_results = execute_queries_on_conditions(conditions)
    semantic_list=compare_semantics_in_list(query_results)
    print(f"The semantics list is {semantic_list}")

    # Build the list of semantic pairs as a string
    semantic_rows = ''.join(f"{i}\n" for i in semantic_list)

    #Prompt asking LLM to integrate binding
    final_prompt=f'''Write an updated SQL query like this, only using equalities. Only return the updated query. USE only the binding variables like written in bidning. If there is a CASE statement leave it intact, only change the WHERE clause, nothing else. Always end with a ';'.
        Input: sql:SELECT name, hair FROM person WHERE person.bodypart='eyes'; binding :[('ojos',), ('augen',), 'WHERE person.bodypart ='eyes';']
        Output: SELECT name, hair FROM person WHERE person.bodypart = 'ojos' OR person.bodypart = 'augen';
        Input: sql:SELECT e.name, d.name AS department_name, CASE WHEN e.salary > 50000 THEN 'High' WHEN e.salary > 30000 THEN 'Medium' ELSE 'Low' END AS salary_status FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.id = 1; binding: [(1,), (2,), 'WHERE d.id =']
        Output: SELECT e.name, d.name AS department_name, CASE WHEN e.salary > 50000 THEN 'High' WHEN e.salary > 30000 THEN 'Medium' ELSE 'Low' END AS salary_status FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.id = 1 OR d.id = 2;
        Input: SELECT * FROM animals WHERE animal.legs<5 and animal.category='insect'; binding: [['three' , 'four', '2', "WHERE animal.legs<5 and animal.category='insect';"], ['INSECTS', "WHERE animal.legs<5 and animal.category='insect';"]]
        Output: SELECT * FROM animals WHERE animal.some_column IN ('three', 'four', '2') AND animal.category = 'INSECTS';
        Input: sql:{sql_query}; binding: {semantic_rows}
        Output:'''
    print(f"The final prompt is {final_prompt}")

    # Try to modify the query with our chosen binding
    response,temp_meta = ask_gemini(final_prompt,True, max_token=1000)
    #Update the metadata
    update_metadata(temp_meta)

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
        result=query_database(sql_query)
    #Print total usage
    print(usage_metadata_total)
    #Return result
    if result:
        return result

#Shareowner and Animalowner examples with equality
# calculus='''{name, shares | ∃id (SHAREOWNER1ROW(id, name, shares) ∧ ANIMALOWNER1ROW(id , _, 'dog'))}'''
# row_calculus_pipeline(calculus, ['shareowner1row', 'animalowner1row'])
# calculus='''{name, shares | ∃id (SHAREOWNER(id, name, shares) ∧ ANIMALOWNER(id , _, 'dog'))}'''
# row_calculus_pipeline(calculus)

#Negation example
# calculus = '''{name, shares | ∃id (SHAREOWNER(id, name, shares) ∧ ¬ANIMALOWNER(id, _, 'dog'))}'''
# row_calculus_pipeline(calculus, ['shareowner', 'animalowner'])

#Doctors example with inequality
# calculus='''{id, name, patients_pd | doctors(id, name, patients_pd) ∧ patients_pd < 12}'''
# row_calculus_pipeline(calculus)
# -> Right Answer: [(1, 'Peter', 'ten'), (2, 'Giovanni','11')]

#Doctors example with inequality and two WHERE clauses/ Now two WHERE clauses do not work
# calculus='''{id, name, patients_pd | doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12}'''
# row_calculus_pipeline(calculus)
#row_calculus_pipeline(calculus, ['doctors'])
# -> Right Answer: [(1, 'Peter', 'ten')]

#Swift Example
# calculus='''ARTISTS(a,_,_), ALBUMS(_,a,"Reputation",2017),SONGS(_,a2,song_name,_),ALBUMS(a2,a,_)'''
# row_calculus_pipeline(calculus, ['artists', 'albums', 'songs'])

# calculus='''∃id ∃shares ∃name (SHAREOWNER1ROW(id, name, shares) ∧ ANIMALOWNER1ROW(id, _, 'dog') ∧ Result(name, shares))'''
# row_calculus_pipeline(calculus, ['shareowner1row', 'animalowner1row'])

# calculus='''∃id ∃shares ∃name (SHAREOWNER(id, name, shares) ∧ ANIMALOWNER(id, _, 'dog'))'''
# row_calculus_pipeline(calculus, ['shareowner', 'animalowner'])

# calculus='''∃id (childre_table(id, _) ∧ fathers(id, _))'''
# row_calculus_pipeline(calculus)

# calculus='''∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))'''
# row_calculus_pipeline(calculus)