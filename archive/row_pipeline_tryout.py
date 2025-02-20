import os
from Utilities.database import query_database
from Utilities.extractor import extract
from Utilities.llm import ask_llm, llm_json, QUERY, CATEGORY




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
    '''final_text = ask_llm(
        f"Combine and describe the relationships between the following tables if necessary. {combined_text}"
    )'''

    return combined_context  # Return the combined descriptive text for all tables

def logic_sql_pipeline(query, tables):
    # Generate context by writing or reading tables' info
    context = get_context(tables)
    #print(f"The context is {context}")
    print(f"The query is {query}")

    #Get response
    response=ask_llm(f"Write a new query in natural text, according to this. Input:'FInd out what Peter's heighr is.' Output: 'Peter's height is [number]'. Input:'{query}'. Output:")
    print(f"The new query is: {response}")

    #print(f"The context is {context}")
    #Get SQL query
    response = ask_llm(f"Convert the following query to SQL. Write this query without using the AS: : {query}. The structure of the database is the following: {context}. ")
    #print(f"The response query is:\n {response}")
    sql_query = extract(response, start_marker="```sql",end_marker="```" )
    print(f"The SQL query is: {sql_query}")

    response=ask_llm(f"If there exists the keyword 'AS' in that query, remove it and all the aliases. The query is: {sql_query}")
    sql_query = extract(response, start_marker="```sql",end_marker="```" )
    print(f"The SQL query is: {sql_query}")
# Example usage
#query = "Find all songs by the artist who released the album Reputation in 2017."
#logic_sql_pipeline(query, ["songs", "artists", "albums"])

logic_sql_pipeline(f'''Get the names and the amount of shares of all people owning a dog.''',['shareowner1row', 'animalowner1row'])
#logic_sql_pipeline(f'''Get the names and the amount of shares of all people owning a dog, who's name is diego''',['shareowner1row', 'animalowner1row'])