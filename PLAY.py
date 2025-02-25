from Utilities.database import query_database
from Utilities.llm import ask_llm, llm_json

semantic_list=('chien','dog', 'perro')
print(type(semantic_list))
word="dog"

semantic_list=semantic_list-word
print(semantic_list)