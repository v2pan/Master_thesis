import psycopg2
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