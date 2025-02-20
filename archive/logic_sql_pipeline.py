import psycopg2
import re
import os
from Utilities.database import query_database
from Utilities.extractor import extract
from Utilities.llm import ask_llm

def write_tables_text( tables):
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    combined_text = ""
    combined_context=""

    for t in tables:
        content_text = ""
        context_text = ""
        
        # Define file paths for content and context
        content_file_path = os.path.join(current_directory, 'saved_info', f'{t}_content.txt')
        context_file_path = os.path.join(current_directory, 'saved_info', f'{t}_context.txt')

        # Check if content and context files already exist
        if os.path.exists(content_file_path) and os.path.exists(context_file_path):
            # Read the content from the existing files
            with open(content_file_path, 'r') as content_file:
                content_text = content_file.read()
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
            rws = query_database(allrows, False)

            #print(f"Unique: {cond}")
            #print(f"Rows: {rws}")
            
            # Convert cond and rws into descriptive text
#             content_text = ask_llm(f'''Convert database information: {str(cond)} {rws}
#             Convert every row entry into key value pairs, however maintain the characteristics of the columns. If input is Unique: [('owner_id', 'NO', 'integer', 'PRIMARY KEY'), ('animalname', 'YES', 'text', None), ('category', 'YES', 'text', None)]
# Rows: [(1, 'bill', 'dog'), (2, 'diego', 'cat')]". The output should be: '[
#   {{"owner_id": 1, "animalname": "bill", "category": "dog"}},
#   {{"owner_id": 2, "animalname": "diego", "category": "cat"}}
# ]''')
            # Convert cond and rws into descriptive text
            content_text = ask_llm(f'''Convert database information: {str(cond)} {rws}
            Make it into a descriptive text only if the actual data. If input is Unique: [('owner_id', 'NO', 'integer', 'PRIMARY KEY'), ('animalname', 'YES', 'text', None), ('category', 'YES', 'text', None)]
Rows: [(1, 'bill', 'dog'), (2, 'diego', 'cat')]". The output should be: The animal with the owner_id 1 has the animalname "bill" and is a dog. The animal with the owner_id 2 has the animalname "diego" and is a cat. ''')
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(content_file_path), exist_ok=True)
            
            # Write content and context to respective files if they don't exist
            with open(content_file_path, 'w') as content_file:
                #content_file.write(f'''{t}\n{str(cond)} \n{rws}''')
                content_file.write(content_text)
            with open(context_file_path, 'w') as context_file:
                context_file.write(f"The name of the table is {t} \n {str(cond)}")
            context_text = f"The name of the table is {t} \n {str(cond)}"

        # Append each table's context and content to the main text
        combined_text += f"{content_text}\n"
        combined_context += f"{context_text}\n"


    #print(f"The combined descriptive text is:\n {combined_text}")
    print("--------------------")
    
    # Final combination of descriptive texts, with inter-table relationships
    '''final_text = ask_llm(
        f"Combine and describe the relationships between the following tables if necessary. {combined_text}"
    )'''
    final_text = combined_text

    return final_text, combined_context  # Return the combined descriptive text for all tables

def logic_sql_pipeline(query, tables):
    # Generate context by writing or reading tables' info
    content, context = write_tables_text(tables)
    #print(f"The context is {context}")
    print(f"The query is {query}")

    #Get response
    response=ask_llm(f"Write a new query in natural text, according to this. Input:'FInd out what Peter's heighr is.' Output: 'Peter's height is [number]'. Input:'{query}'. Output:")
    print(f"The new query is: {response}")

    print(f"The context is {context}")
    #Get SQL query
    response = ask_llm(f"Convert the following query to SQL: {query}. The strucutre of the database is the following: {context}.")
    print(f"The response query is:\n {response}")
    sql_query = extract(response, start_marker="```sql",end_marker="```" )
    print(f"The SQL query is: {sql_query}")
    print(f"SQL answer is: {query_database(sql_query, True)}")

    #Convert SQL to human language
    instructions = ask_llm(f'''Verbalize this SQL query as instructions for an LLM: {sql_query} to natural language without any syntax. Write those instructions in an ordered way.''')

    print(f"The instructions are {instructions}")
    output=ask_llm(f"Perform the following instructions: {instructions} on the content {content}. Finally, answer the query: {query}. In each step write an explanation which information you used and whay you concluded like a great teacher.")
    print(f"The output is {output}")

    

# Example usage
#query = "Find all songs by the artist who released the album Reputation in 2017."
#logic_sql_pipeline(query, ["songs", "artists", "albums"])

logic_sql_pipeline(f'''Get the names and the amount of shares of all people owning a dog.''',['shareowner', 'animalowner'])