import psycopg2
from gemini import post_gemini
import re
import os

from database import query_database



    

def first_pipe(goal, tables, context=None, iteration_count=0):
    # Stop if the recursion has reached the maximum allowed iterations
    if iteration_count >= 5:
        print("Maximum recursion limit of 5 reached. Stopping further attempts.")
        return

    # Compute context only if it hasn't been passed to the function
    if context is None:
        context = {}  # Initialize an empty dictionary
        for t in tables:
            unique = f'''SELECT DISTINCT jsonb_each_text(to_jsonb({t})) FROM {t};'''
            context[t] = query_database(unique, False)  # Use context[t] for assignment
        print(f"The context is {context}")


    # Generate the SQL query based on the given context and goal
    temp = post_gemini(
        f"{goal}. The columns with the unique values are given by {context}. Errors in the database or the expression can occur.",
        True
    )
    #print(f"The SQL expression is {temp}")

    # Execute the generated SQL query
    result = query_database(temp)
    print(f"The result is {result}") # First object of first list

    # Handle errors and recursive call if necessary
    if not result:
        print("An error occurred when executing the query")
        # Pass context, goal, and increment iteration count to avoid recomputation
        first_pipe(
            f'''Modify the following query: {temp}, such that no error occurs. The context is {context}. {goal}. Write the query in the right language. Make sure it is a valid SQL query.''',
            tables,
            context,
            iteration_count + 1
        )

def write_tables_text(query, tables):
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    text = ""

    for t in tables:
        newtext = ""
        file_path = os.path.join(current_directory, 'saved_info', f'{t}.txt')

        # Check if the file already exists
        if os.path.exists(file_path):
            # Read the content from the existing file
            with open(file_path, 'r') as file:
                newtext = file.read()
        else:
            # Query the database for schema and data if file doesn't exist
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
                    tc.table_name = '{t}'  -- Use single quotes around the table name
            ) AS constraints 
            ON c.column_name = constraints.column_name
            WHERE 
                c.table_name = '{t}';  -- Use single quotes around the table name
            '''
            allrows = f'''SELECT * FROM {t}'''
            
            # Fetch data from the database
            cond = query_database(unique, False)
            rws = query_database(allrows, False)
            
            # Concatenate `cond` and `rws` results
            newtext = f"{str(cond)}\n{str(rws)}"

            #Post it to the LLM to get context
            newtext = post_gemini(f''' Convert the following database entries into a descriptive text. {newtext}.''')
            
            # Write to the text file only if it doesn't already exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(newtext)

        # Append the result for the current table to the main text
        text += newtext + "\n"
    
    print(f"The text is {text}")
    print(f"--------------------")
    text=post_gemini(f'''Combine the different tables into on if necessary. For example if one line states the "Carsten with id 1 has Euros. " and "Julius, with id 10 is the child of person with id 1". One can follow "Carsten with id 1, who has the child Julius with id 10, has 1 euros."\n   {text}''')
    #print(connections)
    return text  # Return combined text for all tables

def text_pipeline(query, tables):
    # Generate context by writing or reading tables' info
    context = write_tables_text(query, tables)
    print(f"The context is {context}")

    # Generate an initial answer based on the context
    answer = post_gemini(f"{query}. Give me the answer in descriptive text {context}. Assume reasonable linkages between the tables. In this case, it is between user_id and id. Keep it very brief.")
    print(f"The answer is {answer}")
 
    # Interactive loop to continue or finish
    while True:
        # Ask the user if they are finished
        user_response = input("Are you finished? (Type 'end' to terminate or 'again' to continue): ").strip().lower()
        
        if user_response == "end":
            print("Process terminated.")
            break
        elif user_response == "again":
            # Get additional directions from the user
            additional_query = input("Please provide additional directions: ")
            
            # Use the initial answer and context with new directions
            answer = post_gemini(f"{additional_query}. Current context: {context}. Current answer {answer}. Give me the answer in descriptive text. Only give the answer in descriptive text. Keep it very brief.")
            print(f"Updated answer based on additional directions: {answer}")
        else:
            print("Invalid input. Please type 'finished' or 'not'.")

#text_pipeline("Give me the names and amount the shares of all the people having a dog.", ['animalowner','shareowner'])

text_pipeline(f'''Find all songs by the artist who released the album Reputation in 2017."''',['songs', 'albums','artists'])
