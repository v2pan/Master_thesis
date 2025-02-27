from Main.combined_pipeline import combined_pipeline
from Utilities.database import query_database
from Evaluation.evaluation import test_cases, evaluate_results

# combined_pipeline('''∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z))''')
data=[(1, 'Pierre', 20, 1, 'bill', 'chien', 'chien'), (3, 'Diego', 15, 3, 'chris', 'dog', 'dog'), (4, 'Marcel', 11, 4, 'juan', 'perro', 'perro')]
target=[[3, 'Diego', 15, 3, 'chris', 'dog'], [4, 'Marcel', 11, 4, 'juan', 'perro'], [1, 'Pierre', 20, 1, 'bill', 'chien']]

#[tuple(i) for i in target_instance["output"]]
print(evaluate_results([tuple(i) for i in target], data,boolean=True))