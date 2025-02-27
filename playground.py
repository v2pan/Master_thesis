from Evaluation.test_evaluation import compare_lists_of_lists, process_list_where

target = [[('Peter',), "WHERE doctors.name = 'Peter' AND doctors.patients_pd < 12;"],[('ten',), ('11',), "WHERE doctors.name = 'Peter' AND doctors.patients_pd < 12;"] ]
data = [[('Peter',), "WHERE doctors.name = 'Peter' AND doctors.patients_pd < 12;"],[ ('ten',), ('11',), "WHERE doctors.name = 'Peter' AND doctors.patients_pd < 12;"] ]
target_list=process_list_where(target)
data_list=process_list_where(data)
print(compare_lists_of_lists(target_list, data_list))