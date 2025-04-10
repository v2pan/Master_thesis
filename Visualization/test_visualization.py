import os
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
import pandas as pd


#Load the necessary categorization
path_categorization= os.path.join(os.getcwd(), "saved_json", "categorization")
with open(path_categorization, 'r') as f:
    categorization = json.load(f)

#New dic data structure
path_query_error= os.path.join(os.getcwd(), "saved_json", "error_query_list_gemini-1.5-flash_tranlsation")
with open(path_query_error, 'r') as f:
    query_error_dic = json.load(f)

# Get all categories
l = 0
categories_all = None
for key, values in query_error_dic.items():
    if l == 1:
        break
    categories_all = list(values.keys())
    l += 1

# Initialize an array or list to store the overall total counts across all categories
total_counts_all_categories = np.zeros(len(categories_all))

def visualize_errors_category(query_error_dic, categorization, total_counts_all_categories=None):
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

        # #Categorization
        # Add the current total counts to the overall total
        

        #Sort the results by category
        for key,value in query_error_dic.items():
            if key in categorization[category]:
                tmp_count=0
                for v in value.values():
                    total_counts_per_category[tmp_count] += v
                    tmp_count+=1
            
        total_counts_all_categories += total_counts_per_category
        # Add to the total category
        # categorization["total"] = np.zeros(len(categories_all))
        # if category != "total":            
        #     for i, count in enumerate(total_counts_per_category):
        #         categorization["total"][i] += count  # Update total category
       
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

    
    ax = axes[-1]
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

    # #Categorization
    # Add the current total counts to the overall total
    

    #Sort the results by category
    for key,value in query_error_dic.items():
        if key in categorization[category]:
            tmp_count=0
            for v in value.values():
                total_counts_per_category[tmp_count] += v
                tmp_count+=1
        
    total_counts_all_categories += total_counts_per_category
    # Add to the total category
    # categorization["total"] = np.zeros(len(categories_all))
    # if category != "total":            
    #     for i, count in enumerate(total_counts_per_category):
    #         categorization["total"][i] += count  # Update total category
    
    #Defien a total_dic with the appropriate results
    total_counts = np.sum(total_counts_per_category)
    if total_counts > 0:
        probs = total_counts_per_category / total_counts
    else:
        probs = np.zeros(len(categories_all))

    total_dic = {
        "categories": list(categories_all),
        "probabilities": list(probs),
        "total_counts": list(total_counts_all_categories)
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
    ax.set_title(f"Total Error Counts", fontsize=10) #Smaller fontsize
    ax.tick_params(axis='x', rotation=0, labelsize=8) #Smaller fontsize
    ax.tick_params(axis='y', labelsize=8) #Smaller fontsize
    ax.set_xlabel("Error Type", fontsize=9) #Smaller fontsize
    ax.set_ylabel("Total Count", fontsize=9) #Smaller fontsize
    # colors = ['red'] * 6 + ['blue'] # make sure this is defined before the code, and matches the number of categories
    # handles = [plt.Rectangle((0, 0), 1, 1, color=color, label=label) for label, color in zip(category_mapping.keys(), colors)]
    # ax.legend(handles=handles, title='Category Mapping', bbox_to_anchor=(1.05, 1))
    plt.tight_layout()
        
    # # Remove any extra axes that we didn't 
    # print(total_counts_all_categories)
    # for j in range(i + 1, len(axes)):
    #     fig.delaxes(axes[j])

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
    filepath_total_fig = os.path.join(os.getcwd(), "saved_plots", "new_error_query_list_gemini-1.5-flash_tranlsation.png")
    fig.savefig(filepath_total_fig, dpi=300, bbox_inches='tight')
    print("Total plot saved to 'saved_plots' folder.")
    plt.show()
    print("The total counter is: ", control_counter)


visualize_errors_category(query_error_dic, categorization, total_counts_all_categories)