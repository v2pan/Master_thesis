from evaluation import evaluate_results

output=[('princess', 'one thousand', '24.12.2022', '1000'), ('makeuptutorial', '1000 thousand', '17.01.2011', '1000000'), ('surviver1000', '1 million', '17.01.2011', '1000000')]
result={('surviver1000', '1 million', '22.11.2014', 12), ('makeuptutorial', '1000 thousand', '17.01.2011 ', 1000000), ('princess ', 'one thousand', '24.12.2022', 1000)}

accuracy, precision, recall, f1_score = evaluate_results(result, output)

print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1 Score: {f1_score}")

