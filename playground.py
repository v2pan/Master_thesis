import os
import json

path_query_error= os.path.join(os.getcwd(), "saved_json", "error_query_list")
with open(path_query_error, 'r') as f:
            query_error_dic = json.load(f)

tmp_dic={"Hello": {"a": 1, "b": 2, "c": 3}}
for key,value in tmp_dic.items():
        query_error_dic[key]=value

print(query_error_dic)


