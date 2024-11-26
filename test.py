from other_gemini import gemini_json
from database import query_database

def get_relevant_tables (calculus):

    prompt='''SELECT table_name 
    FROM information_schema.tables
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';'''
    result=query_database(prompt,printing=False) #Result is a list 

    #Extract the pure names
    count=0
    for i in result:
        result[count]=i[0]
        count+=1
    print(result)

    input_prompt = f""
    for i in result:
        #Only one entrance in each list -> is the name itself without any quotes
        input_prompt+=f"Does table '{i}' occur in the expression '{calculus}?  \n"
    categories=gemini_json(prompt=input_prompt,response_type=list[bool])
    relevant_tables = [result[i] for i, is_relevant in enumerate(categories) if is_relevant]
    return relevant_tables


calculus='''∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog'))'''
print(get_relevant_tables(calculus))