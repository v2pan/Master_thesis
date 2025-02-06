from other_gemini import ask_gemini, gemini_json
from evaluation import evaluate_results
import numpy as np
import matplotlib.pyplot as plt


def calculate_metrics(actual, predicted):
    """
    Calculates accuracy, precision, recall, and F1-score.

    Args:
        actual: A list or numpy array of true labels (e.g., [True, False, False, True]).
        predicted: A list or numpy array of predicted labels (e.g., [True, False, False, True]).

    Returns:
        A dictionary containing the calculated metrics (accuracy, precision, recall, F1-score).
        Returns None if input lists are not the same length or contain non-boolean values.
    """

    if len(actual) != len(predicted):
        print("Error: Input lists must have the same length.")
        return None

    if not all(isinstance(val, bool) for val in actual) or not all(isinstance(val, bool) for val in predicted):
        print("Error: Input lists must contain only boolean values.")
        return None


    # Calculate TP, FP, FN, TN
    tp, fp, fn, tn = 0, 0, 0, 0
    for i in range(len(actual)):

        if not isinstance(actual[i], bool) or not isinstance(predicted[i], bool):
            print("Error: Input lists must contain only boolean values.")
            return None
        else:
            if actual[i] == True and predicted[i] == True:
                tp += 1
            elif actual[i] == False and predicted[i] == True:
                fp += 1
            elif actual[i] == True and predicted[i] == False:
                fn += 1
            elif actual[i] == False and predicted[i] == False:
                tn += 1


    # Calculate metrics
    accuracy = (tp + tn) / len(actual)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0  # Handle divide-by-zero
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0  # Handle divide-by-zero
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0  # Handle divide-by-zero

    return accuracy,precision, recall, f1_score,
    




prompt='''Answer the following questions with True or False. 
The questions are 
 \n '400 °C'  is greater than '200 °C' \n
'100 °C'  is greater than '200 °C' \n 
'50 °C'  is greater than '200 °C' \n
 '800 °F'  is greater than '200 °C' \n'''
prompt="Answer the following questions with True or False. Reason you thinking and write out important considerations for this comparison.  \n '200 °F'  is greater than '200 °C' \n '400 °F'  is greater than '200 °C' \n '350 °F'  is greater than '200 °C' \n '200 °F'  is greater than '200 °C' \n"

true_reponse=[False, True, False, False]

models = ["gemini-2.0-flash", "gemini-1.5-flash"]
num_tries = 3

results = {}
metrics = {}
for model in models:
    results[model] = []
    metrics[model] = []
    for i in range(num_tries):
        #response = gemini_json(prompt, response_type=list[bool])

        answer=ask_gemini(prompt, model=model)
        response = gemini_json(f"For this question \n{prompt} \n The following asnwer was given {answer}. Return the necessary answer whether this question is true or False", response_type=list[bool], model=model)  # Expect a list of booleans back

        results[model].append(response)

        accuracy, precision, recall, f1 = calculate_metrics(true_reponse, response)


        metrics[model].append([ accuracy, precision, recall, f1 ])


# models = ["gemini-2.0-flash", "gemini-1.5-flash"]
# metrics={'gemini-2.0-flash':[[1.0, 1.0, 1.0, 1.0], [0.75, 0, 0.0, 0], [1.0, 1.0, 1.0, 1.0]] , 'gemini-1.5-flash': [[0.75, 0.5, 1.0, 0.6666666666666666], [0.5, 0.0, 0.0, 0], [1.0, 1.0, 1.0, 1.0]]}
fig, axes = plt.subplots(1, len(models), figsize=(10, 5 * len(models)))  # Adjust figure size

for i, model in enumerate(models):
        mean_scores = np.mean(metrics[model], axis=0)
        ax = axes[i]

        ax.bar(["Accuracy", "Precision", "Recall", "F1-score"], mean_scores)
        ax.set_ylabel("Mean Score")
        ax.set_title(model)
        ax.set_ylim(0, 1)  # Ensure scores are within 0-1 range
        ax.set_xticks(range(len(mean_scores)))
        ax.set_xticklabels(["Accuracy", "Precision", "Recall", "F1-score"], rotation=45, ha="right")  #X-Axis Labels

plt.tight_layout()  # Adjust subplot parameters for better spacing
plt.show()



# # Print the results in a table format
# print("| Try |", end="")
# for model in models:
#     print(f" {model} |", end="")
# # print()
# # print("|---|---|---|")
# # for i in range(num_tries):
# #     print(f"| {i+1} | {results[models[0]][i]} | {results[models[1]][i]} |")
# # print()
# print("| Metrics | Accuracy | Precision | Recall | F1-score»", end="")
# for i in range(num_tries):
#     print(f"| {i+1} | {metrics[models[0]][i]} | {metrics[models[1]][i]} |")

# # for model in models:
# #     print(f"| {model } | Mean Accuracy | Mean Precision | Mean Recall | Mean F1-score»", end="")
# #     print(np.mean(metrics[models[0]],axis=0))