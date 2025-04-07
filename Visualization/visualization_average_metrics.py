import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Evaluation.evaluation import calculate_average_metrics

def visualize_results(acc, prec, rec, f1 , path):
    """Visualizes the results in a bar plot."""

    results = {
    #"Average Accuracy": acc,
    "Average Precision": prec,
    "Average Recall": rec,
    "Average F1-score": f1
    }

    # Extract data
    metrics = list(results.keys())
    scores = list(results.values())

    # Create the bar plot
    plt.figure(figsize=(10, 6))  # Adjust figure size as needed
    plt.bar(metrics, scores)
    plt.xlabel("Metric")
    plt.ylabel("Score")
    plt.title("Average Scores")
    plt.ylim(0, 1)  # Set y-axis limits
    plt.xticks(rotation=445, ha="right")  # Rotate x-axis labels
    plt.gca().set_xticklabels([])

    # Add labels to the bars (metrics on top)
    for i, score in enumerate(scores):
        plt.text(metrics[i], score + 0.02, f"{metrics[i]} \n {score:.2f}", ha='center', fontsize=16)  #Adjusted font size


    plt.tight_layout()  # Prevents labels from overlapping

    

    save_path=path
    # Save the figure
    try:
        plt.savefig(save_path, dpi=300)  # Higher dpi for better quality
        print(f"Figure saved to {save_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")

    plt.show()


# Example usage (replace with your results)

# acc=
# prec=
# rec=
# f1=


visualize_results(0.4, 0.18, 0.18, 0.18, path="saved_plots/new_average_metrics_gemini_2_0_hard.png")

# configs=[ [0.4, 0.54, 0.46, 0.48,"saved_plots/new_average_metrics_gemini_1_5_soft.png"],
#  [0.4, 0.18, 0.14, 0.16,"saved_plots/new_average_metrics_gemini_1_5_hard.png"],
#  [0.4, 0.71, 0.68, 0.69,"saved_plots/new_average_metrics_gemini_2_0_soft.png"],
#  [0.4, 0.17, 0.22, 0.19,"saved_plots/new_average_metrics_gemini_2_0_hard.png"]]

# for i in range(len(configs)):
#     prec=configs[i][1]
#     rec=configs[i][2]
#     f1=configs[i][3]
#     path=configs[i][4]
#     visualize_results(0.4, prec, rec, f1, path)