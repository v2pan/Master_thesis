import os
import json

from test_evaluation import visualize_errors

path_error_total= os.path.join(os.getcwd(), "saved_json", "error_total")
path_queries_list= os.path.join(os.getcwd(), "saved_json", "queries_list")

with open(path_error_total, 'r') as f:
            error_total = json.load(f)
with open(path_queries_list, 'r') as f:
            queries_list = json.load(f)

visualize_errors(error_total, queries_list)
    