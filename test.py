# import google.generativeai as genai

# with open("api_key.txt", "r") as file:
#     api_key = file.read().strip()  # Read the file and remove any surrounding whitespace
# genai.configure(api_key=api_key)

# model = genai.GenerativeModel("gemini-1.5-flash")
# chat = model.start_chat(
#     history=[
#         {"role": "user", "parts": "Hello. I am Vladimir"},
#         {"role": "model", "parts": "Hello Vladimir. What would you like to know?"},
#     ]
# )
# response = chat.send_message("I have 2 dogs in my house.", stream=False)
# for chunk in response:
#     print(chunk.text)
#     print("_" * 80)
# response = chat.send_message("What is my name?", stream=False)
# for chunk in response:
#     print(chunk.text)
#     print("_" * 80)

# print(chat.history)

import sqlparse
import re

def extract_where_conditions_sqlparse(sql_query):
    """
    Extracts WHERE clause conditions, handling both left and right operands.  More robust than simple string parsing.
    """
    try:
        parsed = sqlparse.parse(sql_query)[0]
        where_clause = None
        for token in parsed.tokens:
            if isinstance(token, sqlparse.sql.Where):
                where_clause = token
                break

        if where_clause:
            conditions = []
            for token in where_clause.tokens:
                where_clause_str = str(where_clause).strip()
                if isinstance(token, sqlparse.sql.Comparison):
                    left = str(token.left).strip()
                    right = str(token.right).strip()
                    operator = str(token.token_next(0)).strip()

                    #Process Left Operand
                    left_is_column = re.fullmatch(r'\w+\.\w+', left)  # More robust column check
                    if left_is_column:
                        table_name, column_name = left.split('.')
                        left = f"SELECT {column_name} FROM {table_name};"
                    
                    # Process Right Operand
                    right_is_column = re.fullmatch(r'\w+\.\w+', right) # More robust column check
                    if right_is_column:
                        table_name, column_name = right.split('.')
                        right = f"SELECT {column_name} FROM {table_name};"
                    else:
                        #Handle literal values (remove quotes)
                        right = right.replace("'", "")

                    print(where_clause.get_name)
                    conditions.append([left, operator,where_clause_str, right])
                elif isinstance(token, sqlparse.sql.IdentifierList):
                    print("Warning: Complex IdentifierList in WHERE clause not fully handled.")

            return conditions
        else:
            return [] #No WHERE clause found.
    except (IndexError, sqlparse.exceptions.ParseException) as e:
        print(f"Error parsing SQL query: {e}")
        return [] #Return empty list on parse error.

sql_query2 = "SELECT * FROM doctors  WHERE doctors.name = 'Peter' OR doctors.patients_pd > 100 AND city = 'London';"
conditions2 = extract_where_conditions_sqlparse(sql_query2)
print(conditions2)