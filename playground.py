from database import query_database, QueryExecutionError

sql_query="SELECT * FROM doctors WHERE doctors.patients_pd < 12;"
try:
    result=query_database(sql_query)
    print(result)
except QueryExecutionError as e:
    error_message = e.args[0] if e.args else "No error message provided"
    print(f"Error: {error_message}")