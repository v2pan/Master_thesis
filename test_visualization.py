import os
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import pandas as pd

from test_evaluation import visualize_errors

path_error_total= os.path.join(os.getcwd(), "saved_json", "error_total")
path_queries_list= os.path.join(os.getcwd(), "saved_json", "queries_list")
path_categorization= os.path.join(os.getcwd(), "saved_json", "categorization")

with open(path_error_total, 'r') as f:
            error_total = json.load(f)
with open(path_queries_list, 'r') as f:
            queries_list = json.load(f)
with open(path_categorization, 'r') as f:
            categorization = json.load(f)


def visualize_errors_category(error_total, queries_list, categorization):
    num_categories = len(categorization)
    rows = int(math.sqrt(num_categories))
    cols = math.ceil(num_categories / rows)

    fig, axes = plt.subplots(rows, cols, figsize=(8, 8)) #Reduced figsize
    axes = axes.ravel()

    for i, category in enumerate(categorization):
        ax = axes[i]
        colors = ['red', 'red', 'red', 'red', 'red', 'red', 'blue']
        categories_all = error_total[0].keys()
        width = 0.35
        x = np.arange(len(categories_all))
        total_counts_per_category = np.zeros(len(categories_all))

        for k in range(len(error_total)):
            error_cnt = error_total[k]
            if queries_list[k] in categorization[category]:
                for l, cat in enumerate(categories_all):
                    total_counts_per_category[l] += error_cnt[cat]

        total_counts = np.sum(total_counts_per_category)
        if total_counts > 0:
            probs = total_counts_per_category / total_counts
        else:
            probs = np.zeros(len(categories_all))

        total_dic = {
            "categories": list(categories_all),
            "probabilities": list(probs),
            "total_counts": list(total_counts_per_category)
        }

        total_dic = pd.DataFrame(total_dic) 
        # Define a mapping from categories to numbers
        category_mapping = {category: idx for idx, category in enumerate(total_dic['categories'], start=1)}
        # Replace categories with their numeric mapping
        total_dic['categories_numeric'] = total_dic['categories'].map(category_mapping)


        sns.barplot(x='categories_numeric', y='total_counts', data=total_dic, ax=ax, palette=colors)
        ax.set_title(f"Error Counts for: {category}", fontsize=10) #Smaller fontsize
        ax.tick_params(axis='x', rotation=0, labelsize=8) #Smaller fontsize
        ax.tick_params(axis='y', labelsize=8) #Smaller fontsize
        ax.set_xlabel("Error Type", fontsize=9) #Smaller fontsize
        ax.set_ylabel("Total Count", fontsize=9) #Smaller fontsize
        plt.tight_layout()
        # colors = sns.color_palette("tab10", len(category_mapping))  # Generate colors based on the number of categories
        # handles = [
        #     plt.Rectangle((0, 0), 1, 1, color=colors[idx - 1], label=category) 
        #     for category, idx in category_mapping.items()
        # ]
        # ax.legend(handles=handles, title="Category Mapping", bbox_to_anchor=(1.05, 1), loc='upper left')


    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Add a legend outside the subplots
    # Add a legend outside the subplots
    handles = [plt.Rectangle((0, 0), 1, 1, color=color, label=f"{category}") for category, color in zip(categorization, colors)]
    fig.legend(handles=handles, title="Category Mapping", bbox_to_anchor=(1.05, 1), loc='upper left')

    filepath_total_fig = os.path.join(os.getcwd(), "saved_plots", "total_plot_category.png")
    fig.savefig(filepath_total_fig, dpi=300, bbox_inches='tight')
    plt.show()

visualize_errors_category(error_total, queries_list, categorization)