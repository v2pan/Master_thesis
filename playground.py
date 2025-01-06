import matplotlib.pyplot as plt

error_total = [{'initial_result': 0, 'semantic_list': 2, 'wrong_result': 0, 'correct_results': 0},
              {'initial_result': 0, 'semantic_list': 0, 'wrong_result': 0, 'correct_results': 2}]

num_plots = len(error_total)
num_cols = 2  # Adjust number of columns as needed
num_rows = (num_plots + num_cols - 1) // num_cols

fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 4 * num_rows))
axes = axes.flatten()

for i, error_cnt in enumerate(error_total):
    queries = list(error_cnt.keys())
    counts = list(error_cnt.values())
    total_counts = sum(counts)
    if total_counts > 0: #Avoid division by zero
        probs = [count / total_counts for count in counts]
    else:
        probs = [0] * len(queries) #All probabilities are 0 if total_counts is 0

    axes[i].bar(queries, probs)
    axes[i].set_xlabel("Result Type")
    axes[i].set_ylabel("Probability")
    axes[i].set_title(f"Data Point {i+1}")
    # axes[i].tick_params(axis='x', rotation=45, ha="right") #Rotate x-axis labels


# Remove extra subplots if necessary
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()