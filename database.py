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

            # Check for warnings (method depends on your database library)
            try:
                warnings = cursor.fetchwarnings()  # For mysql.connector
                if warnings:
                    print("Database Warnings:")
                    for warning in warnings:
                        print(f"- {warning.msg}")  # Print warning messages
            except Exception as e:

                try:
                    rows = cursor.fetchall()
                except Exception as e:
                    rows = None  # Set rows to None if fetchall fails

                if printing:
                    print(f"The final answer to the query is {rows}")
        except Exception as e:
            print(f"An error occurred when executing the query: {e}")
            rows = None
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return rows

    except Exception as e:
        print(f"An error occurred when accessing the database: {e}")
        return None  # Return None to indicate a broader error
