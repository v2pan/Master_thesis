import re
from database import query_database
def extract_column_queries(sql_query):
  """Extracts SELECT queries for each column with a dot (.) in the SQL query.

  Args:
    sql_query: The SQL query string.

  Returns:
    list: A list of SELECT queries for each column with a dot.
  """

  column_queries = {}
  matches = re.findall(r"(\w+\.\w+)", sql_query)
  for match in matches:
    column_name = match.split(".")[1]
    table_name = match.split(".")[0]
    column_queries[f"{table_name}.{column_name}"]=f"SELECT {column_name} FROM {table_name};"
  return column_queries



# Example usage:
sql_query = """
SELECT name, shares
FROM shareowner1row
INNER JOIN animalowner1row ON shareowner1row.id = animalowner1row.owner_id
WHERE animalowner1row.category = 'dog';
"""

column_queries = extract_column_queries(sql_query)
print(f"Column Queries: {column_queries}")

#Put unique values into the dictionary  
for key,value in column_queries.items():
    query_database(value,True)
    column_queries[key]=query_database(value)

print(f"Column Queries: {column_queries}")

def extract_column_pairs(sql_query):
    """Extracts pairs of relations from an SQL query, where each pair is on one side of an '='.

    Args:
        sql_query: The SQL query string.

    Returns:
        list: A list of tuples, where each tuple represents a pair of relations.
    """

    pairs = []
    matches = re.findall(r"(\w+\.\w+)\s*=\s*(\w+\.\w+)", sql_query)
    for match in matches:
        pairs.append((match.group(1), match.group(2)))
    return pairs

column_pairs = extract_column_pairs(sql_query)
print(f"Column Pairs: {column_pairs}")

