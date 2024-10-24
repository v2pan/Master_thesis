import psycopg2
from gemini import post_gemini
import re

# Database connection parameters
DB_NAME = "postgres"
DB_USER = "postgres"  # Replace this with your PostgreSQL username if different
DB_PASSWORD = "postgres"      # Modify, if necessary
DB_HOST = "localhost"
DB_PORT = "5432"

def query_database(query, printing=True):
    # Connect to PostgreSQL database
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = connection.cursor()
        
        # Example query
        #cursor.execute("SELECT shares FROM shares WHERE name='Vlad'")
        
        if not query:
            raise ValueError("Query is empty or None")
        try:
            cursor.execute(query)
        except Exception as e:
            return None
    
        rows = cursor.fetchall()
        if printing:
            print(f"The final answer to the query is {rows}")
    
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return rows
        
    except Exception as e:
        print(f"An error occurred, when accessing the database: {e}")

#query_database(post_gemini('''Convert to a SQL query:$\Pi_{shares}(\sigma_{name='Vlad'}(totalshares))$''', True))

#Two step process that checks whether result makes sense
#Query: Get the shares of someone named Vladi (actually Vlad)
def get_shares():
    #text= query_database('SELECT DISTINCT name FROM totalshares')
    text=query_database('''SELECT DISTINCT jsonb_each_text(to_jsonb(totalshares))
FROM totalshares;''')

    temp=post_gemini(f'''Convert to a SQL query: $\\Pi_{{shares}}(\\sigma_{{name='Vladi'}}(totalshares))$
   "''', True)

    #temp=post_gemini(f'''Are you sure that this query {temp} is right cosidering all the distinct values for the column "name" : {text}. Give out a corrected version''', True)
    result=post_gemini(f'''Are you sure that this query {temp} is right cosidering all the distinct values for the columns are {text}
    Change the SQL query only if some variable is very similar, otherwise not, otherwise give out the originialinput query''', True)
    try:
        print(f"The result is {query_database(result)}")
    except Exception:
        print("Result was empty")
        print(f"The exception is {query_database( temp)}")

#get_shares()

def shares_join(query,tables):
    context = {}  
    for t in tables:
        unique = f'''SELECT DISTINCT jsonb_each_text(to_jsonb({t})) FROM {t};'''
        context[t] = query_database(unique, False)  # Use context[t] for assignment
    print(context)
    temp=post_gemini(query, True)
    print(f"The query is {temp}")
    result=query_database(temp)
    if not result:
        print("An error occured when executing the query")
        shares_join(f'''Modify the following query: {temp}, such that no error occurs, when joining, especially when column names are similar. THe context of the columns with there unique values is {context}''', tables)
    



#shares_join(f'''Convert to a SQL query: $\Pi_{{shares}}(totalshares \bowtie_{{name=name}} totalnation)$"''', ['totalshares', 'totalnation'])
#shares_join(f'''Convert to a SQL query: $\Pi_{{name}}(\sigma_{{category='dog'}}(totalanimal))$"''', ['totalanimal'])

def first_pipe(query, tables, context=None, goal=None, iteration_count=0):
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

    # Compute goal only if it hasn't been passed to the function
    if goal is None:
        goal = post_gemini(f"What is the goal of the query? {query} 1 or 2 sentences, please.")
        print(f"The goal is {goal}")

    # Generate the SQL query based on the given context and goal
    temp = post_gemini(
        f"Create the SQL query for this expression {query}. The columns with the unique values are given by {context}. The goal of the query is {goal}. Errors in the database or the expression can occur.",
        True
    )
    print(f"The SQL expression is {temp}")

    # Execute the generated SQL query
    result = query_database(temp)
    print(f"The result is {result}") # First object of first list

    # Handle errors and recursive call if necessary
    if not result:
        print("An error occurred when executing the query")
        # Pass context, goal, and increment iteration count to avoid recomputation
        first_pipe(
            f'''Modify the following query: {temp}, such that no error occurs. The context is {context}. The goal is {goal}. Write the query in the right language.''',
            tables,
            context,
            goal,
            iteration_count + 1
        )


rel_algebras=[[f'''Convert to a SQL query:$\Pi_{{shares}}(\sigma_{{name='Влади'}}(totalshares))$''',['totalshares']],
              [f'''Convert to a SQL query: $\Pi_{{shares}}(totalshares \bowtie_{{name=name}} totalnation)$"''',['totalshares', 'totalnation']],
                [f'''Convert to a SQL query: $\Pi_{{name}}(\sigma_{{category='dog'}}(totalanimal))$"''',['totalanimal']]
]
first_pipe(rel_algebras[2][0], rel_algebras[2][1])

#query_database('SELECT T1.shares FROM totalshares T1 INNER JOIN totalnation T2  ON T1.name LIKE T2.id;')
#first_pipe(f'''Convert to a SQL query $\Pi_{{shares}}(totalshares \bowtie _{{name=id}} (\sigma_{{nationality='Germany'}}totalnation))$''', ['totalshares', 'totalnation'])