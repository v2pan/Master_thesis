import os
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import pandas as pd



# def visualize_errors(error_total, queries_list):
#     #FINAL EVALUATION PLOT

#     #PATHs for saving plots and dictionaries
#     #path_ind_dic= os.path.join(os.getcwd(), "saved_json", "individual_results")
#     #path_total_dic= os.path.join(os.getcwd(), "saved_json", "total_results")
#     #filepath_total_fig=filepath = os.path.join(os.getcwd(), "saved_plots", "total_probs")
    

#     num_plots = len(error_total)
#     num_cols = 2  # Adjust number of columns as needed
#     num_rows = (num_plots + num_cols - 1) // num_cols

#     fig, axes = plt.subplots(num_rows, num_cols, figsize=(10, 4 * num_rows))
#     axes = axes.flatten()

#     #Create a list of dictionaries to also save the data, in order to replot it etc.
#     dic_list=[]
#     colors = ['red', 'red', 'red', 'red', 'red', 'red', 'blue'] # Define colors for the bars

#     for i, error_cnt in enumerate(error_total):
#         error_spots = list(error_cnt.keys())
#         counts = list(error_cnt.values())
#         total_counts = sum(counts)
#         if total_counts > 0: #Avoid division by zero
#             probs = [count / total_counts for count in counts]
#         else:
#             probs = [0] * len(queries) #All probabilities are 0 if total_counts is 0

#         title_part1, title_part2 = split_title_at_space(queries_list[i])

#         #Create dictionary and append data
#         tmp_dic={
#             "calculus" : queries_list[i],
#             "errors" : error_spots,
#             "error_counts" : counts,
#             "probabilities" : probs
#         }

#         sns.barplot(x='errors', y='error_counts', data=tmp_dic, ax=axes[i], palette=colors).set_title(f"{title_part1}\n{title_part2}")
#         axes[i].tick_params(axis='x', rotation=30)
#         #Append to dictionary list
#         dic_list.append(tmp_dic)


#     # Remove extra subplots if necessary
#     for j in range(i + 1, len(axes)):
#         fig.delaxes(axes[j])

#     filepath_individual_plot=filepath = os.path.join(os.getcwd(), "saved_plots", "individual_probs")
#     #Individual plot
#     plt.tight_layout()
#     plt.suptitle(f"Counts of Result Types for {RUNS} Runs")
#     plt.subplots_adjust(top=0.85)
#     fig.savefig(filepath_individual_plot, dpi=300, bbox_inches='tight')  # Save the figure with higher resolution

#     plt.show()

#     # TOTAL PLOT overl all distinct values
#     fig_total, ax_total = plt.subplots(figsize=(10, 6))
#     categories = error_total[0].keys()  # Assuming all dictionaries have the same keys
#     width = 0.35

#     x = np.arange(len(categories))
#     total_counts_per_category = np.zeros(len(categories))

#     for error_cnt in error_total:
#         for i, cat in enumerate(categories):
#             total_counts_per_category[i] += error_cnt[cat]

#     total_counts = np.sum(total_counts_per_category)
#     if total_counts > 0:
#         probs = total_counts_per_category / total_counts
#     else:
#         probs = np.zeros(len(categories))

#     #Create total dictionary
#     total_dic={
#             "categories" : list(categories),
#             "probabilities" : list(probs),
#             "total_counts" : list(total_counts_per_category)
#         }
    
#     #Save the two dictionaires
#     with open(path_ind_dic, 'w', encoding="utf-8") as f:
#         json.dump(dic_list, f, indent=4, ensure_ascii=False )
#     with open(path_total_dic, 'w', encoding='utf-8') as f:
#         json.dump(total_dic, f, indent=4, ensure_ascii=False)

#     sns.barplot(x='categories', y='total_counts', data=total_dic, ax=ax_total, palette=colors).set_title(f"Total Probabilities of Result Types")
#     plt.xticks(rotation=30)
#     plt.tight_layout()
#     fig_total.savefig(filepath_total_fig, dpi=300, bbox_inches='tight')  # Save the figure with higher resolution
#     plt.show()

#Load the necessary categorization
path_categorization= os.path.join(os.getcwd(), "saved_json", "categorization")
with open(path_categorization, 'r') as f:
            categorization = json.load(f)

#New dic data structure
path_query_error= os.path.join(os.getcwd(), "saved_json", "error_query_list_gemini_2_0")
with open(path_query_error, 'r') as f:
            query_error_dic = json.load(f)

def visualize_errors_category(query_error_dic, categorization):
    num_categories = len(categorization)
    rows = int(math.sqrt(num_categories))
    cols = math.ceil(num_categories / rows)

    #Axes for the subplots
    fig, axes = plt.subplots(rows, cols, figsize=(8, 8)) #Reduced figsize
    axes = axes.ravel()

    control_counter=0
    for i, category in enumerate(categorization):
        ax = axes[i]
        colors = ['red', 'red', 'red', 'red', 'red', 'red', 'blue']

        #Get all the categories
        l=0
        categories_all=None
        for key,values in query_error_dic.items():
            if l==1:
                break
            categories_all=list(values.keys())
            l+=1

        #Define metrics
        width = 0.35
        x = np.arange(len(categories_all))
        total_counts_per_category = np.zeros(len(categories_all))

        #Sort the results by category
        for key,value in query_error_dic.items():
            if key in categorization[category]:
                tmp_count=0
                for v in value.values():
                    total_counts_per_category[tmp_count] += v
                    tmp_count+=1
       
        #Defien a total_dic with the appropriate results
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

        control_counter += sum(total_dic["total_counts"])

        total_dic = pd.DataFrame(total_dic) 
        # Define a mapping from categories to numbers
        category_mapping = {category: idx for idx, category in enumerate(total_dic['categories'], start=1)}
        # Create the reverse mapping for legend labels
        reverse_mapping = {v: k for k, v in category_mapping.items()}
        # Replace categories with their numeric mapping
        total_dic['categories_numeric'] = total_dic['categories'].map(category_mapping)

        handles = [plt.Rectangle((0, 0), 1, 1, color=color, label=f"{key}={value}") 
           for (key, value), color in zip(category_mapping.items(), colors)]
        #Deprecated
        #sns.barplot(x='categories_numeric', y='total_counts', data=total_dic, ax=ax, palette=colors)
        #sns.barplot(x='categories_numeric', y='total_counts', data=total_dic, ax=ax, hue='categories_numeric', palette=colors, legend=False)
        ax.bar(total_dic["categories_numeric"], total_dic["total_counts"], color=colors)
        ax.set_title(f"Error Counts for: \n {category}", fontsize=10) #Smaller fontsize
        ax.tick_params(axis='x', rotation=0, labelsize=8) #Smaller fontsize
        ax.tick_params(axis='y', labelsize=8) #Smaller fontsize
        ax.set_xlabel("Error Type", fontsize=9) #Smaller fontsize
        ax.set_ylabel("Total Count", fontsize=9) #Smaller fontsize
        # colors = ['red'] * 6 + ['blue'] # make sure this is defined before the code, and matches the number of categories
        # handles = [plt.Rectangle((0, 0), 1, 1, color=color, label=label) for label, color in zip(category_mapping.keys(), colors)]
        # ax.legend(handles=handles, title='Category Mapping', bbox_to_anchor=(1.05, 1))
        plt.tight_layout()
        # colors = sns.color_palette("tab10", len(category_mapping))  # Generate colors based on the number of categories
        # handles = [
        #     plt.Rectangle((0, 0), 1, 1, color=colors[idx - 1], label=category) 
        #     for category, idx in category_mapping.items()
        # ]
        # ax.legend(handles=handles, title="Category Mapping", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Remove any extra axes that we didn't use
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Add a legend outside the subplots
    # handles = [plt.Rectangle((0, 0), 1, 1, color=color, label=f"{key}={value}") 
    #        for (key, value), color in zip(category_mapping.items(), colors)]
    # fig.legend(
    #     #handles=handles,
    #     #labels=labels,
    #     title="Category Mapping", bbox_to_anchor=(1.05, 1), loc='lower left')

    #Give title, then save and show the plot
    title = " || ".join([f"{key} : {value}" for key, value in category_mapping.items()])
    parts = title.split(" || ")
    title = " || ".join(parts[:3] + ["\n"] + parts[3:])
    fig.suptitle(f"{title}") #Smaller fontsize
    plt.tight_layout()
    filepath_total_fig = os.path.join(os.getcwd(), "saved_plots", "total_plot_category_gemini_2_0.png")
    fig.savefig(filepath_total_fig, dpi=300, bbox_inches='tight')
    print("Total plot saved to 'saved_plots' folder.")
    plt.show()
    print("The total counter is: ", control_counter)


visualize_errors_category(query_error_dic, categorization)