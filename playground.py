import sqlparse

def analyze_sql_query(sql_query):
    """
    Analyzes an SQL query to detect WHERE and JOIN conditions.

    Args:
        sql_query: The SQL query string.

    Returns:
        A dictionary containing boolean flags for WHERE and JOIN conditions, 
        and lists of their respective tokens (if found).  Returns an error 
        message if sqlparse fails to parse the query.
    """
    try:
        parsed = sqlparse.parse(sql_query)[0]
    except IndexError:
        return "Error: sqlparse failed to parse the query. Check for syntax errors."

    where_clause = None
    where_conditions = []
    join_conditions = []
    for token in parsed.tokens:
        if isinstance(token, sqlparse.sql.Where):
            where_conditions.append(token) 

        if isinstance(token, sqlparse.sql.Comparison):
            # Extract the condition from the JOIN clause (this part is tricky and may need refinement 
            # depending on the complexity of JOIN conditions).
            join_conditions.append(token)


    return {
        "where_conditions": where_conditions,
        "join_conditions": join_conditions,
    }

# Example usage
sql_query1 = "SELECT * FROM users WHERE age > 25 AND city = 'New York';"
sql_query2 = "SELECT * FROM users INNER JOIN orders ON users.id = orders.user_id;"
sql_query3 = "SELECT * FROM users WHERE age > 25;"
sql_query4 = "SELECT * FROM products JOIN categories ON products.category_id = categories.id WHERE price > 100;"
sql_query5 = "Invalid SQL Query" # Example of an invalid query.


result1 = analyze_sql_query(sql_query1)
result2 = analyze_sql_query(sql_query2)
result3 = analyze_sql_query(sql_query3)
result4 = analyze_sql_query(sql_query4)
result5 = analyze_sql_query(sql_query5)


print(f"Query 1: {result1}")
print(f"Query 2: {result2}")
print(f"Query 3: {result3}")
print(f"Query 4: {result4}")
print(f"Query 5: {result5}")