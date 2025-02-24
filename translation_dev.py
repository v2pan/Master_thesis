from Utilities.database import query_database
from Utilities.llm import ask_llm, llm_json

semantic_list=[[('chien',), ('dog',), ('perro',), "WHERE animalowner.category = 'dog';"]]

def tranlsation_based_approach(semantic_list: list):
    for sublist in semantic_list:

        
        # Create the translation table if it doesn't exist
        create_table_prompt = '''CREATE TABLE IF NOT EXISTS translation_table (
            word TEXT NOT NULL,
            synonym TEXT NOT NULL
        );'''
        query_database(create_table_prompt)  # Execute the table creation query
        
        # Prepare the INSERT query to populate the table
        population_prompt = "INSERT INTO translation_table (word, synonym) VALUES "
        values = []
        
        # Loop through the dictionary and create the values part of the query
        for semantic in sublist[:-1]:
            for word in semantic[0]:
                values.append(f"('{word}', '{semantic[1]}')")
        
        if values:
            population_prompt += ', '.join(values) + ';'
            query_database(population_prompt)  # Execute the insert query
        else:
            print("No values to insert.")
        
    print("Table created and populated successfully.")