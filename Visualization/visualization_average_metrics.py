import matplotlib.pyplot as plt
from Evaluation.evaluation import calculate_average_metrics

def visualize_results(acc, prec, rec, f1):
    """Visualizes the results in a bar plot."""

    results = {
    "Average Accuracy": acc,
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
        plt.text(metrics[i], score + 0.02, f"{metrics[i]} \n {score:.2f}", ha='center', fontsize=10)  #Adjusted font size


    plt.tight_layout()  # Prevents labels from overlapping

    

    save_path="saved_plots/average_metrics_gemini_1_5_soft.png"
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


#visualize_results(acc, prec, rec, f1)