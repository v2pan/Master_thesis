# import os
# from test_evaluation import load_data
# from evaluation import evaluate_results
# import time
# start=time.time()
# filepath = os.path.join(os.getcwd(), "temporary", "total_test")
# loaded_dictionary = load_data(filepath)

# target_value="∃date weather(date, city, temperature, rainfall) ∧ website_visits(date, page, visits)"
# #target_value="∃item bakery_sales(item,_,_) ∧ oven_temperature(item, >200 °C)"
# for i in loaded_dictionary:
#     if i["calculus"]==target_value:
#         target_instance = i

# list_output=[]
# output=target_instance["output"]
# for i in output:
#     list_output.append(tuple(i))
# output=list_output
# pipeline_output=[('2023 10 26', 'London', 12, 0, '2023 October 26', 'about', 500), ('2023 10 26', 'London', 12, 0, '2023 October 26', 'homepage', 1000), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'about', 500), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'homepage', 1000), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'contact', 200), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'homepage', 1200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'contact', 200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'homepage', 1200)]
# # set_output=set()
# # for i in output:
# #     set_output.add(set(i))
# accuracy, precision, recall, f1_score=evaluate_results(output,pipeline_output)
# print(precision)
# end=time.time()
# print(f"Time taken: {end-start} seconds")

import numpy as np
times = [1,2,4]
print(round(np.mean(times),2))