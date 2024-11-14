#Updated pipeline after discussion with Eleonora
import psycopg2
import re
import os
from database import query_database
from extractor import extract
from other_gemini import ask_gemini, ask_gemini_boolean

def get_context(tables):
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    combined_context=""
    for t in tables:
        context_text = ""
        
        # Define file paths for content and context
        context_file_path = os.path.join(current_directory, 'saved_info', f'{t}_context.txt')

        # Check if content and context files already exist
        if os.path.exists(context_file_path):
            with open(context_file_path, 'r') as context_file:
                context_text = context_file.read()
        else:
            # SQL queries for schema (context) and table data (content)
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
            allrows = f'''SELECT * FROM {t};'''
            
            # Fetch data from the database
            cond = query_database(unique, False)            
            with open(context_file_path, 'w') as context_file:
                context_file.write(f"The name of the table is {t} \n {str(cond)}")
            context_text = f"The name of the table is {t} \n {str(cond)}"

        # Append each table's context and content to the main text
        combined_context += f"{context_text}\n"


    #print(f"The combined descriptive text is:\n {combined_text}")
    print("--------------------")
    
    # Final combination of descriptive texts, with inter-table relationships
    '''final_text = ask_gemini(
        f"Combine and describe the relationships between the following tables if necessary. {combined_text}"
    )'''

    return combined_context  # Return the combined descriptive text for all tables

def binding_sql_pipeline(query, tables):
    # Generate context by writing or reading tables' info
    context = get_context(tables)
    #print(f"The context is {context}")
    print(f"The query is {query}")

    #Get response
    response=ask_gemini(f"Write a new query in natural text, according to this. Input:'Find out what Peter's height is.' Output: 'Peter's height is [number]'. Input:'{query}'. Output:")
    print(f"The new query is: {response}")

    print(f"The context is {context}")
    #Get SQL query
    response = ask_gemini(f"Convert the following query to SQL: {query}. The strucutre of the database is the following: {context}.")
    print(f"The response query is:\n {response}")
    sql_query = extract(response, start_marker="```sql",end_marker="```" )
    print(f"The SQL query is: {sql_query}")

    nec_cols=ask_gemini(f"You are given this SQL query: {sql_query}. List all columns and tables  with their full name needed to execute this query in an enumerated way. Check again if these are all the columns needed to execute the query. Keep it short.")
    print(f"The necessary columns are: {nec_cols}")

    distinct_sql_text=ask_gemini(f"For each of those mentioned columns, write a SQL query to retrieve all distinct values. Return as many queries as there are columns. {nec_cols}")
    distinct_sql_text = extract(distinct_sql_text, start_marker="SELECT",end_marker=";",multiple=True, inclusive=True)
    print(f"The distinct SQL queries are: {distinct_sql_text}")

    final_query=sql_query
    for i in distinct_sql_text:
        dist_values=query_database(i,printing= True)
        response=ask_gemini(f"For the following query {i} the distinct values are: {dist_values} the following. The goal of the final query is that {response}. If you think it is necessary modfiy the query, to achieve the mentioned goal do it.The query is {sql_query}. Do you need to modify the query? If yes, provide the modified query.")
        extracted=extract(response, start_marker="```sql",end_marker="```" )
        if extracted==None:
            print("No query was extracted")
        else:
            final_query=extracted
            print(f"THe final query is: {final_query}")
    print(f"The final query is: {final_query}")
    #print(f"SQL answer is: {query_database(sql_query, True)}")

    # #Convert SQL to human language, don't use query execution plam
    # instructions = ask_gemini(f'''Verbalize this SQL query as instructions for an LLM: {sql_query} to natural language without any syntax. Write those instructions in an enumerated way. Only mention if there is a selection, projection, or join.''')

    # print(f"The instructions are: \n {instructions}")
    # # Find the first occurrence of a number followed by a dot
    # match = re.search(r'\d+\.', instructions)
    # if match:
    #     start_index = match.start()
    #     # Extract the instructions after the first match
    #     individual_instructions = re.split(r'\d+\.', instructions[start_index:])
    #     # Remove any empty strings
    #     individual_instructions = [instruction.strip() for instruction in individual_instructions if instruction.strip()]
    # else:
    #     print("No instructions found")

    # print(individual_instructions)

    # individual_queries=[]
    # for i in individual_instructions:
    #     response = ask_gemini(f"Write a SQL query to retrieve all distinct values for each column from all tables mentioned in  {i}")
    #     query = extract(response, start_marker="```sql",end_marker="```" )
    #     dist_values = query_database(query, False)
    #     print(f"The distinct values are {dist_values}")
    #     individual_queries.append(query)
    # print(individual_queries)
    
    # -----------------------------------------------------
    
    # #Get the procedure
    # explain_query="EXPLAIN " + sql_query
    # #print(f"The execution plan is: {query_database(explain_query, True)}")
    # execution_plan = query_database(explain_query, False)
    # #print(f"The execution plan is: {execution_plan}")

    # #print(ask_gemini(f"Give me the order of execution for this SQL query: {sql_query}"))
    # order=ask_gemini(f"Identify the order of operations, exclusively mention selection-projection-join: {execution_plan} \n {sql_query}, Keep it short.")
    # #print(f"The order is {order}")

    # #Output with the SQL queries 
    # sql_queries=ask_gemini(f"Write a series of SQL queries to execute the following operations: {order}.")
    # print(f"The SQL queries are: {sql_queries}")

    # iso_queries=extract(sql_queries, start_marker="SELECT",end_marker=";", multiple=True, inclusive=True)
    # print(f"The isolated SQL queries are: {iso_queries}")
    # print(f"The SQL queries are: {sql_queries}")

    # print(f"There are so many queries: {len(iso_queries)}")
    # intent_queries=[]
    # print("The iso_query is: ", iso_queries[0])
    # for i in iso_queries:
    #     intent = ask_gemini(f"Write the intent of this query in natural language in a short sentence. {i}")
    #     intent_queries.append(f"{i}\n -- {intent}")
    # #intent=ask_gemini(f"Identify the intent of each query in natural language: {sql_queries}. Keep it short.")
    # #print(f"The intent is {intent}")
    # print(f"The intent queries are: {intent_queries}")


    

# Example usage
#query = "Find all songs by the artist who released the album Reputation in 2017."
#logic_sql_pipeline(query, ["songs", "artists", "albums"])

binding_sql_pipeline(f'''Get the names and the amount of shares of all people owning a dog.''',['shareowner', 'animalowner'])