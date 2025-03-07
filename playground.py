from Main.combined_pipeline import combined_pipeline
from Main.combined_pipeline import combined_pipeline
from Evaluation.test_evaluation import evaluate_results
from Utilities.database import query_database

def create_and_populate_table(dataframe, table_name):
    try:
        # Clean table name (optional)
        table_name = table_name.replace(" ", "_")

        # Drop table if it exists
        delete_table_query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        query_database(delete_table_query, printing=False)

        # Convert all data to string format
        dataframe = dataframe.astype(str)

        # Create table with a single column
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (Aggregate TEXT);"
        query_database(create_table_query, printing=False)
        print(f"Table '{table_name}' created successfully.")

        # Insert data into table
        values = []
        for _, row in dataframe.iterrows():
            row_values = "\n".join(row.astype(str))  # Concatenate row values with newline separator
            values.append(f"('{row_values.replace("'", "''")}')")  # Escape single quotes for SQL

        if values:
            insert_query = f"INSERT INTO {table_name} VALUES {', '.join(values)};"
            query_database(insert_query, printing=False)
            print(f"Table '{table_name}' populated successfully.")
        else:
            print("No data to insert.")

    except Exception as e:
        print(f"An error occurred: {e}")


import pandas
import numpy
import re
path="Data/itunes_amazon_raw_data/labeled_data.csv"

#Do
data=pandas.read_csv(path, skiprows=5, encoding='unicode_escape')
left_table=data.iloc[[0],4:10]
create_and_populate_table(left_table, "left_table")