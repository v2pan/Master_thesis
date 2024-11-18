import sqlparse
from sqlparse.sql import Token, Identifier, Where, Parenthesis

def transform_in_to_join(query):
    """
    Transform a SQL query with an IN subquery into an equivalent query using INNER JOIN.

    Args:
        query (str): The original SQL query.

    Returns:
        str: The transformed SQL query with INNER JOIN.
    """
    # Parse the SQL query
    parsed = sqlparse.parse(query)[0]

    # Initialize variables for main table, subquery, and conditions
    outer_table = None
    subquery = None
    where_clause = None

    # Iterate through tokens to find the FROM clause and WHERE clause
    for token in parsed.tokens:
        if token.ttype is None and isinstance(token, Identifier):
            if outer_table is None:  # First table after FROM
                outer_table = token.get_real_name()

        if isinstance(token, Where):
            where_clause = token
            for sub_token in token.tokens:
                if isinstance(sub_token, Parenthesis):  # Subquery inside WHERE
                    subquery = sub_token
                    break

    if not (outer_table and subquery):
        raise ValueError("Could not extract the required parts of the query.")

    # Parse the subquery
    subquery_tokens = sqlparse.parse(subquery.value.strip('()'))[0]
    subquery_table = None
    subquery_conditions = []

    # Extract subquery details
    for token in subquery_tokens.tokens:
        if token.ttype is None and isinstance(token, Identifier):
            if subquery_table is None:  # First table after FROM in subquery
                subquery_table = token.get_real_name()
        elif isinstance(token, Where):
            # Extract conditions from WHERE clause of subquery
            subquery_conditions = [
                str(sub_token).strip()
                for sub_token in token.tokens
                if sub_token.ttype is None or sub_token.ttype == Token.Text
            ]

    if not subquery_table:
        raise ValueError("Could not extract the table name from the subquery.")

    # Construct the JOIN condition
    join_condition = f"{outer_table}.id = {subquery_table}.owner_id"
    where_conditions = ' '.join(subquery_conditions).replace('WHERE', '')

    # Build the JOIN query
    join_query = (
        f"SELECT name, shares\n"
        f"FROM {outer_table}\n"
        f"INNER JOIN {subquery_table} ON {join_condition}\n"
        f"WHERE {where_conditions};"
    )

    return join_query

# Original query
original_query = """
SELECT name, shares
FROM shareowner1row
WHERE id IN (
    SELECT owner_id
    FROM animalowner1row
    WHERE category = 'dog' AND animalname = 'bill'
);
"""

# Transform the query
try:
    transformed_query = transform_in_to_join(original_query)
    print(transformed_query)
except ValueError as e:
    print(f"Error: {e}")



# Example response:
# **Emphasizing the Dried Aspect:**
# * Everlasting Blooms
# * Dried & Delightful
# * The Petal Preserve
# ...

# chat = model.start_chat(
#     history=[
#         {"role": "user", "parts": "Hi my name is Bob"},
#         {"role": "model", "parts": "Hi Bob!"},
#     ]
# )
# # Call `count_tokens` to get the input token count (`total_tokens`).
# print(model.count_tokens(chat.history))
# # ( total_tokens: 10 )

# response = chat.send_message(
#     "In one sentence, explain how a computer works to a young child."
# )

# print(response.text)
# print(response.usage_metadata)
# from google.generativeai.types.content_types import to_contents
# # You can call `count_tokens` on the combined history and content of the next turn.
# print(model.count_tokens(chat.history + to_contents("What is the meaning of life?")))

