import psycopg2
# Database connection parameters
DB_NAME = "postgres"
DB_USER = "postgres"  # Replace this with your PostgreSQL username if different
DB_PASSWORD = "postgres"      # Modify, if necessary
DB_HOST = "localhost"
#DB_PORT = "5432"
DB_PORT = "5433" #For Postgres17

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
            connection.commit()
        except Exception as e:
            return None
    
        try:
            rows = cursor.fetchall()
        except Exception as e:
            rows = None  # Set rows to None if fetchall fails
        if printing:
            print(f"The final answer to the query is {rows}")
    
        
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return rows
        
    except Exception as e:
        print(f"An error occurred, when accessing the database: {e}")

# name='Hans'
# shares=23
# query=f"INSERT INTO totalshares (name, shares) VALUES ('{name}','{shares}')"
# query_database(query)
# query_database("SELECT * FROM totalshares")
#query_database("SELECT * FROM totalshares")

# result=query_database("SELECT embedding FROM documents LIMIT 1")
# print(type(result))

# emedding=str([3,1,2])
# query_database(f"SELECT embedding <-> '{emedding}' AS distance FROM items;")

#query_database("SELECT embedding <-> '[3,1,2]' AS distance FROM items;")