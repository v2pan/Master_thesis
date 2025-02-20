#Written for testing purposes finding weaknesses in the code
import unittest
import os
from unittest.mock import patch, MagicMock
import warnings

# Import your modules (replace with your actual paths)
from Main.row_calculus_pipeline import row_calculus_pipeline, get_relevant_tables, get_context, extract_where_conditions_sqlparse, execute_queries_on_conditions, compare_semantics_in_list, initial_query 
from Utilities.database import query_database, QueryExecutionError

import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#Load test JSON
def load_json_from_relative_path(relative_path):
    """Loads a JSON file from a relative path.

    Args:
        relative_path: The relative path to the JSON file (e.g., "data/my_data.json").

    Returns:
        A Python dictionary representing the JSON data, or None if an error occurs.
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
        json_file_path = os.path.join(script_dir, relative_path)  # Construct the absolute path
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON data in {json_file_path}")
        return None
# Example usage:
relative_path_to_json = "temporary/Test_creation"  # Adjust this to your file's relative path
test_cases = load_json_from_relative_path(relative_path_to_json)

class TestRowCalculusPipeline(unittest.TestCase):
    relative_path_to_json = "temporary/Test_creation"  # Adjust this to your file's relative path
    
    # def setUp(self):
    #     """Load test cases before running each test method"""
    #     self.test_cases = load_json_from_relative_path(self.relative_path_to_json)

    def test_get_tables(self):
        """Tests table retrieval, generating a plot for each calculus expression."""
        results = []  # List to store individual results

        for i in test_cases:
            if i["pipeline"] == "row_calculus_pipeline":
                try:
                    tables = get_relevant_tables(i["calculus"])
                    correct = len(set(tables) & set(i["tables"])) #Correctly retrieved tables
                    incorrect = len(set(i['tables']) - set(tables)) + max(0,len(tables) - len(i["tables"]))  #Incorrectly retrieved (missing or extra)
                    results.append(
                        {
                            "Calculus": i["calculus"],
                            "Correct": correct,
                            "Incorrect": incorrect,
                        }
                    )
                except Exception as e:
                    print(f"Error processing test case {i}: {e}")
                    results.append(
                        {
                            "Calculus": i["calculus"],
                            "Correct": 0,
                            "Incorrect": 1,  # Mark as incorrect if an error occurred
                        }
                    )
        # Reshape data for Seaborn
        results_df = pd.DataFrame(results)
        results_df = results_df.melt(id_vars=["Calculus"], var_name="Category", value_name="Count")
        print(results_df)

        plt.figure(figsize=(12, 6))
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        sns.barplot(x="Calculus", y="Count", hue="Category", data=results_df[results_df["Category"] == "Correct"], palette="Greens", legend=False) # added hue and legend=False
        plt.xticks(rotation=45, ha="right")
        plt.title("Correct")
        plt.show()


    # def test_initial_query(self):
        
    #     """Test the initial query to get the context"""
    #     for i in test_cases:
    #         if i["pipeline"]=="row_calculus_pipeline":
    #             tables=i['tables']
    #             context=get_context(tables)
    #             initial_query_result, _ = initial_query(i['calculus'],context)

    #             try:
    #                 query_database(initial_query_result)
    #             except QueryExecutionError:
    #                 self.assertAlmostEqual(i['initial_result'], "QueryExecutionError")


if __name__ == '__main__':
    unittest.main()




# def test_get_tables(self):
    
#     """Test a simple query to retrieve the currect amount of tables"""

#     for i in test_cases:
#         count_warnings=0
#         if i["pipeline"]=="row_calculus_pipeline":
#             tables=get_relevant_tables(i["calculus"])

#             #Assert true that not fewer tables are retrieved than necessary
#             self.assertTrue(len(tables)>= i['tables_num'])

#             #Assert that recall is 100%
#             all(item in tables for item in i["tables"] )
#             # Warning for extra tables, not critical but can be problematic
#             if len(tables) > i['tables_num']:
#                 warnings.warn(f"NOT critical: More tables than necessary ({len(tables)} instead of {i['tables_num']}) for calculus: {i['calculus']}", UserWarning)
#                 count_warnings+=1
#     if count_warnings>0:
#             print(f"The percent of instances where there were more tables retrieved than necessary is: {100*count_warnings/len(test_cases)}%")


# test_cases = [
#     {
#         "calculus":'''∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)''',
#         "answer":{(2, 'Giovanni', '11'), (1, 'Peter', 'ten')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 1,
#         "tables":['doctors'],
#         "initial_result" : "QueryExecutionError"
        
#     },
#     {   "calculus":'''∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog'))''',
#         "answer":{(2, 'Vladi', 10, 2, 'diego', 'chat')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2,
#         "tables":['shareowner', 'animalowner']
#     },
#     {
#         "calculus":'''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )''',
#         "answer":{(1, '1', 'one', 'Joachim', 1, 'Julia'), (2, 'many', 'two', 'Dieter', 2, 'Petra')},
#         "pipeline":"join_pipeline",
#         "tables_num": 2,
#         "tables":['children_table', 'fathers', 'mothers']
#     },
#     {
#         "calculus":'''∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))''',
#         "answer":{(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2,
#         "tables":['tennis_players', 'tournaments']
#     },
#     {
#         "calculus":'''∃id (children_table(id, >1) ∧ fathers(id, _))''',
#         "answer":{(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')},
#         "pipeline":"combined_pipeline",
#         "tables_num": 2,
#         "tables":['children_table', 'fathers']
#     },
# ]

#Old manual input
#Calculus and the expected result
# test_cases = [
#     {
#         "calculus":'''∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)''',
#         "answer":{(2, 'Giovanni', '11'), (1, 'Peter', 'ten')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 1,
        
#     },
#     {
#         "calculus":'''∃id ∃patients_pd (doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12)''',
#         "answer":{(1, 'Peter', 'ten')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 1
#     },
#     {
#         "calculus":'''∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog'))''',
#         "answer":{(1, 'Pierre', 20, 1, 'bill', 'chien')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))''',
#         "answer":{(3, 'Diego', 15, 3, 'chris', 'dog'), (4, 'Marcel', 11, 4, 'juan', 'perro'), (1, 'Pierre', 20, 1, 'bill', 'chien')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {   "calculus":'''∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog'))''',
#         "answer":{(2, 'Vladi', 10, 2, 'diego', 'chat')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z))''',
#         "answer":{(0, 4, 'zero', 'Gerhard'), (1, 1, 'one', 'Joachim'), (2,'many', 'two', 'Dieter')},
#         "pipeline":"join_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )''',
#         "answer":{(1, '1', 'one', 'Joachim', 1, 'Julia'), (2, 'many', 'two', 'Dieter', 2, 'Petra')},
#         "pipeline":"join_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))''',
#         "answer":{(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))''',
#         "answer":{('surviver1000', '1 million', 1, 'surviver1000', True), ('makeuptutorial', '1000 thousand', 3, 'makeuptutorial', False), ('surviver1000', '1 million', 2, 'surviver1000', True), ('princess', 'one thousand', 3, 'princess', True)},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃id (children_table(id, >1) ∧ fathers(id, _))''',
#         "answer":{(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')},
#         "pipeline":"combined_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''ARTISTS(a,,), ALBUMS(,a,"Reputation",2017),SONGS(,a2,song_name,),ALBUMS(a2,a,)''',
#         "answer":{(1, 1, 'Reputation', '2017', 1, 'Taylor Swift', 'English', 1, 1, 'Delicate', '3:52'), (2, 2, 'Reputation', '2017', 2, 'Reputation Artist', 'English', 2, 2, 'New Year’s Day', '3:55')},
#         "pipeline":"combined_pipeline",
#         "tables_num": 3
#     },
#     {
#         "calculus":'''∃d weather(d, city, temperature, rainfall) ∧ website_visits(d, page, visits)''',
#         "answer":{('2023 10 26', 'London', 12, 0, '2023 October 26', 'about', 500), ('2023 10 26', 'London', 12, 0, '2023 October 26', 'homepage', 1000), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'about', 500), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'homepage', 1000), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'contact', 200), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'homepage', 1200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'contact', 200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'homepage', 1200)},
#         "pipeline":"join_pipeline",
#         "tables_num": 2
#     }
# ]