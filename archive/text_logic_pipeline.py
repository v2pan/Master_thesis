import psycopg2
from archive.gemini import post_gemini
import re
import os
from database import query_database

from other_gemini import ask_gemini


    
def write_tables_text( tables):
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    combined_text = ""
    combined_context=""

    for t in tables:
        content_text = ""
        
        # Define file paths for content and context
        content_file_path = os.path.join(current_directory, 'saved_info', f'{t}_content.txt')
        context_file_path = os.path.join(current_directory, 'saved_info', f'{t}_context.txt')

        # Check if content and context files already exist
        if os.path.exists(content_file_path) and os.path.exists(context_file_path):
            # Read the content from the existing files
            with open(content_file_path, 'r') as content_file:
                content_text = content_file.read()
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
            content_text = ask_gemini(f'''Convert database information: {str(cond)} {rws}
            Make it into a descriptive text only if the actual data. If input is Unique: [('owner_id', 'NO', 'integer', 'PRIMARY KEY'), ('animalname', 'YES', 'text', None), ('category', 'YES', 'text', None)]
Rows: [(1, 'bill', 'dog'), (2, 'diego', 'cat')]". The output should be: The animal with the owner_id 1 has the animalname "bill" and is a dog. The animal with the owner_id 2 has the animalname "diego" and is a cat. ''')
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(content_file_path), exist_ok=True)
            
            # Write content and context to respective files if they don't exist
            with open(content_file_path, 'w') as content_file:
                content_file.write(content_text)


        # Append each table's context and content to the main text
        combined_text += f"{content_text}\n"
        


    #print(f"The combined descriptive text is:\n {combined_text}")
    print("--------------------")
    
    # Final combination of descriptive texts, with inter-table relationships
    '''final_text = ask_gemini(
        f"Combine and describe the relationships between the following tables if necessary. {combined_text}"
    )'''
    final_text = combined_text

    return final_text  # Return the combined descriptive text for all tables

def text_logic_pipeline(query, tables):
    # Generate context by writing or reading tables' info
    context = write_tables_text(tables)
    print(f"The context is {context}")

    #Logic for updating the query
    #response = ask_gemini(f"What could be erroneous about this question? {query}. Is it logical and does it exclude certain cases.  Enclose the updated question, not the procedure, in natural language in §-+ and §-+ .")
    print(f"The query is {query}")
    response=ask_gemini(f"Change this query to the following format. Input:'What is Peter's height'? Output: Peter's height is [number].This is the query is transform {query}.")
    # Extract the refined query or handle if reattempting is needed
    query=response
    #query = extract(response, query)
    print(f"The new query is: {query}")

    # Generate an initial answer based on the context
    answer = ask_gemini(f" {context} Assume reasonable linkages {query}")


    #answer = ask_gemini(f"{query}. Give me the answer in descriptive text {context}. Assume reasonable linkages between the tables. If the input is: Person with id 1 with name Peter has the dog with id 1. Dog wiht id 1 has four legs. Who are the owners of animals with fours legs. Then output should be: Peter. Don't provide procedures, provide an answer.")
    print(f"The answer is {answer}")
 
    # # Interactive loop to continue or finish
    # while True:
    #     # Ask the user if they are finished
    #     user_response = input("Are you finished? (Type 'end' to terminate or 'again' to continue): ").strip().lower()
        
    #     if user_response == "end":
    #         print("Process terminated.")
    #         break
    #     elif user_response == "again":
    #         # Get additional directions from the user
    #         additional_query = input("Please provide additional directions: ")
            
    #         # Use the initial answer and context with new directions
    #         answer = ask_gemini(f"{additional_query}. Current context: {context}. Current answer {answer}. Give me the answer in descriptive text. Only give the answer in descriptive text. Keep it very brief.")
    #         print(f"Updated answer based on additional directions: {answer}")
    #     else:
    #         print("Invalid input. Please type 'finished' or 'not'.")

# Used to extract answer enclosed with some rare markers
def extract(response, query,start_marker="§-+",end_marker="§-+"):
    # Markers for identifying the updated query

    # Find the start and end of the new query in the response
    start_index = response.find(start_marker)
    end_index = response.find(end_marker, start_index + len(start_marker))

    # Extract the modified query if it exists
    if start_index != -1 and end_index != -1:
        new_query = response[start_index + len(start_marker):end_index].strip()
    else:
        print("Could not extract an updated query. Reattempting to obtain a more accurate query...")
        # Re-attempt to obtain a refined query
        reattempted_response = ask_gemini(f"Can you provide a more accurate version of the query? {query}. Please enclose the updated query in natural language in {start_marker} and {end_marker}.")
        # Attempt extraction again with reattempted response
        start_index = reattempted_response.find(start_marker)
        end_index = reattempted_response.find(end_marker, start_index + len(start_marker))
        
        if start_index != -1 and end_index != -1:
            new_query = reattempted_response[start_index + len(start_marker):end_index].strip()
        else:
            # If extraction still fails, fallback to the original query
            new_query = query
            print("No refined query was provided. Using the original query.")
    
    return new_query

# Example usage
query = "Find all songs by the artist who released the album Reputation in 2017."
text_logic_pipeline(query, ["songs", "artists", "albums"])

