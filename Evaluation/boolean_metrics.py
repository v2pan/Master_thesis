from Utilities.llm import ask_llm, llm_json, RessourceError
import time
from Evaluation.evaluation import evaluate_results
import numpy as np
import matplotlib.pyplot as plt
import json
import math

models = ["gemini-2.0-flash", "gemini-1.5-flash"]
reasons = ["direct", "CoT"]

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

    return accuracy,precision, recall, f1_score

def write_boolean_metrics(metrics, filename = "metrics/boolean_metrics.txt"):
    """Writes all individual metrics to a text file."""
    if metrics:
        try:
            with open(filename, "w") as f:
                for reason in metrics.keys():
                    for model in metrics[reason].keys():
                        f.write(f"--- Average Metrics for {reason} and {model} ---\n")
                        for i,m in enumerate(metrics[reason][model]):
                            accuracy, precision, recall, f1,= m
                            f.write(f"Run {i+1}:\n")
                            f.write(f"  Accuracy: {accuracy:.4f}\n")
                            f.write(f"  Precision: {precision:.4f}\n")
                            f.write(f"  Recall: {recall:.4f}\n")
                            f.write(f"  F1-score: {f1:.4f}\n")
                            f.write("\n")
                        f.write("\n--- Overall Metrics ---\n")
                        accuracy_mean = np.mean(metrics[reason][model], axis=0)[0]
                        precision_mean = np.mean(metrics[reason][model], axis=0)[1]
                        recall_mean = np.mean(metrics[reason][model], axis=0)[2]
                        f1_score_mean = np.mean(metrics[reason][model], axis=0)[3]
                        f.write(f"Mean Accuracy: {accuracy_mean:.4f}\n")
                        f.write(f"Mean Precision: {precision_mean:.4f}\n")
                        f.write(f"Mean Recall: {recall_mean:.4f}\n")
                        f.write(f"Mean F1-score: {f1_score_mean:.4f}\n")
                        f.write("\n")
                        f.write("-----------------------------\n")
                        f.write("\n")
                    print(f"Metrics written to '{filename}'")
        except OSError as e:
            print(f"Error writing metrics to file: {e}")
    else:
        print("No metrics to write to file.")

def create_boolean():
    #Influencers
    prompts=["Answer the following questions with True or False. Reason you thinking, especially considering the units, converting units to another and then answering the question.  \n '1000 thousand'  is greater than '500' \n '50'  is greater than '500' \n '1 million'  is greater than '500' \n 'one thousand'  is greater than '500' \n",
            "Answer the following questions with True or False. Reason you thinking, especially considering the units, converting units to another and then answering the question.  \n '200 °F'  is greater than '200 °C' \n '400 °F'  is greater than '200 °C' \n '350 °F'  is greater than '200 °C' \n '200 °F'  is greater than '200 °C' \n",
            #"Answer the following questions with True or False. Reason you thinking, especially considering the units, converting units to another and then answering the question.  \n '12.00 per dozen'  is smaller than '55' \n '10.00 per dozen'  is smaller than '55' \n '12.00 per dozen'   is smaller than '55' \n '15.00 per dozen'  is smaller than '55' ",
            "Answer the following questions with True or False. Reason you thinking, especially considering the units, converting units to another and then answering the question.  \n '5 dozen'  is greater than '90' \n '8 dozen'  is greater than '90' \n '7 dozen'  is greater than '90' \n '3 dozen'  is greater than '90' \n",
            "Answer the following questions with True or False. Reason you thinking, especially considering the units, converting units to another and then answering the question.  \n '200 °F'  is greater than '180 °C' \n '400 °F'  is greater than '180 °C' \n '350 °F'  is greater than '180 °C' \n '200 °F'  is greater than '180 °C' \n"
            ]
    true_responses=[[True, False, True, True], [False, True, False, False], [False, True, False, False], [False, True, False, False]]

    comparisons=[" > 500", " > 200 °C", " > 90", " > 180 °C"]



    num_tries = 3
    results = {}
    metrics = {}
    for i in range(len(prompts)):
        prompt=prompts[i]
        comparison=comparisons[i]
        true_response=true_responses[i]
        results[comparison] = {}
        metrics[comparison] = {}
        for reason in reasons:
            results[comparison][reason] = {}
            metrics[comparison][reason] = {}
            for model in models:
                results[comparison][reason][model] = []
                metrics[comparison][reason][model] = []
                for i in range(num_tries):
                    #response = llm_json(prompt, response_type=list[bool])
                    try:
                        response=[]
                        if reason=="CoT":
                            while len(response)!=len(true_response):
                                answer=ask_llm(prompt, model=model)
                                response = llm_json(f"For this question \n{prompt} \n The following asnwer was given {answer}. Return the necessary answer whether this question is true or False", response_type=list[bool], model=model)  # Expect a list of booleans back

                        elif reason=="direct":
                            while len(response)!=len(true_response):
                                response = llm_json(f"For this question \n{prompt} \n  Return the necessary answer whether this question is true or False", response_type=list[bool], model=model)  # Expect a list of booleans back
                        
                        results[comparison][reason][model].append(response)

                        accuracy, precision, recall, f1 = calculate_metrics(true_response, response)


                        metrics[comparison][reason][model].append([ accuracy, precision, recall, f1 ])
                    except RessourceError as e:
                        print(f"Error: {e}")
                        time.sleep(60)
    
    with open("saved_json/boolean_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
    
    write_boolean_metrics(metrics)

# def visualize_boolean_metrics():
    
#     with open("saved_json/boolean_metrics.json", "r") as f:
#         metrics=json.load(f)
    

#     for com in metrics.keys():
#         reasons=list(metrics[com].keys())
#         models=list(metrics[com][reasons[0]].keys())
#         fig, axes = plt.subplots(len(reasons), len(models), figsize=(10, 5 * len(models)))  # Adjust figure size
#         for l, reason in enumerate(reasons):
#             for i, model in enumerate(models):
#                     mean_scores = np.mean(metrics[com][reason][model], axis=0)
#                     ax = axes[l][i]

#                     ax.bar(["Accuracy", "Precision", "Recall", "F1-score"], mean_scores)
#                     ax.set_ylabel("Mean Score")
#                     ax.set_title(f"{model} + {reason}")
#                     ax.set_ylim(0, 1)  # Ensure scores are within 0-1 range
#                     ax.set_xticks(range(len(mean_scores)))
#                     ax.set_xticklabels(["Accuracy", "Precision", "Recall", "F1-score"], rotation=45, ha="right")  #X-Axis Labels

#         fig.suptitle(f"Mean Metrics for {com}", fontsize=16)
#         plt.tight_layout()  # Adjust subplot parameters for better spacing
#         plt.show()

def visualize_boolean_metrics():
    
    with open("saved_json/boolean_metrics.json", "r") as f:
        metrics=json.load(f)
    
    x_axis_count=0
    for com in metrics.keys():
        x_axis_count=0
        for l, reason in enumerate(metrics[com].keys()):
            for i in range(len(metrics[com][reason])):
                x_axis_count+=1
    
    fig, axes = plt.subplots(len(metrics.keys()), x_axis_count, figsize=(10, 2 * x_axis_count), constrained_layout=True) 

    kpi_reason={}
    kpi_model={}

    for c, com in enumerate(metrics.keys()):
        reasons=list(metrics[com].keys())
        models=list(metrics[com][reasons[0]].keys())
        # Adjust figure size
        count=0
        for l, reason in enumerate(reasons):
            kpi_reason[reason]=[]
            for i, model in enumerate(models):
                    
                    if model not in kpi_model.keys():
                        kpi_model[model]=[]
                    
                    mean_scores = np.mean(metrics[com][reason][model], axis=0)
                    ax = axes[c][count]

                    ax.bar(["Acc", "Precision", "Recall", "F1-score"], mean_scores)
                    ax.set_ylabel("Mean Score")

                    
                    ax.set_title(f"{model} - {reason} - {com}")
                    ax.set_ylim(0, 1)  # Ensure scores are within 0-1 range
                    #ax.set_xticks(range(len(mean_scores)))
                    #ax.set_xticklabels(["Accuracy", "Precision", "Recall", "F1-score"], rotation=0, ha="right")  #X-Axis Labels

                    #Update counter
                    count+=1    

                    #Append to mean values
                    kpi_reason[reason].append(mean_scores)    
                    kpi_model[model].append(mean_scores)          
            plt.tight_layout()      

        # plt.tight_layout()  # Adjust subplot parameters for better spacing
    
    fig.savefig("saved_plots/boolean_metrics.png", dpi=300, bbox_inches='tight')
    plt.show()   

    for reason in   kpi_reason.keys():
        print(f"The mean values for {reason} are {np.mean(  kpi_reason[reason], axis=0)}")


    for model in  kpi_model.keys():
        print(f"The mean values for {model} are {np.mean( kpi_model[model], axis=0)}")








if __name__=="__main__":
    visualize_boolean_metrics()