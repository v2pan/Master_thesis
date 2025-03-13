from Main.combined_pipeline import combined_pipeline
from Utilities.database import query_database

'Women/Swimwear/Two-Piece'
'Beauty/Makeup/Face'
unique_categories='Women/Swimwear/Two-Piece'
pipeline_query=f"SELECT * FROM mercari_data WHERE mercari_data.name='{unique_categories}'"
actual,meta=combined_pipeline(query=None,initial_sql_query=pipeline_query,aux=True)
actual=query_database(f"SELECT * FROM mercari_data JOIN wheremercari_datanamenewvspinkbikinitop_comparison_newvspinkbik ON mercari_data.name=wheremercari_datanamenewvspinkbikinitop_comparison_newvspinkbik.synonym WHERE wheremercari_datanamenewvspinkbikinitop_comparison_newvspinkbik.word='{unique_categories}'")
print(actual)
expected_query=f"SELECT * FROM mercari_data WHERE mercari_data.category='{unique_categories}'"
expected=query_database(expected_query)
from Evaluation.test_evaluation import evaluate_results
accuracy, precision ,recall ,f1_score =evaluate_results(expected, actual)
print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1_score}")