import os
from Utilities.database import query_database
from Utilities.extractor import extract
from Utilities.llm import ask_llm, llm_json, QUERY, CATEGORY
from Utilities.database import query_database




def get_context(tables):
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    combined_context=""
    for t in tables:
        context_text = ""
        
        # Define file paths for content and context
        context_file_path = os.path.join(current_directory, 'saved_info', f'{t}_context.txt')

        # Check if content and context files already exist
        if os.path.exists(context_file_path):
            with open(context_file_path, 'r') as context_file:
                context_text = context_file.read()
        else:
            # SQL queries for schema (context) and table data (content)
            unique = f'''SELECT 
                c.column_name,
                c.is_nullable,
                c.data_type,
                constraints.constraint_type
            FROM 
                information_schema.columns c
            LEFT JOIN (
                SELECT 
                    kcu.column_name,
                    tc.constraint_type
                FROM 
                    information_schema.table_constraints tc
                JOIN 
                    information_schema.key_column_usage kcu
                ON 
                    tc.constraint_name = kcu.constraint_name
                WHERE 
                    tc.table_name = '{t}'
            ) AS constraints 
            ON c.column_name = constraints.column_name
            WHERE 
                c.table_name = '{t}';
            '''
            allrows = f'''SELECT * FROM {t};'''
            
            # Fetch data from the database
            cond = query_database(unique, False)            
            with open(context_file_path, 'w') as context_file:
                context_file.write(f"The name of the table is {t} \n {str(cond)}")
            context_text = f"The name of the table is {t} \n {str(cond)}"

        # Append each table's context and content to the main text
        combined_context += f"{context_text}\n"


    #print(f"The combined descriptive text is:\n {combined_text}")
    print("--------------------")
    
    # Final combination of descriptive texts, with inter-table relationships
    '''final_text = ask_llm(
        f"Combine and describe the relationships between the following tables if necessary. {combined_text}"
    )'''

    return combined_context  # Return the combined descriptive text for all tables

def logic_sql_pipeline(query, tables):
    # Generate context by writing or reading tables' info
    context = get_context(tables)
    #print(f"The context is {context}")
    print(f"The query is {query}")

    #Get response
    response=ask_llm(f"Write a new query in natural text, according to this. Input:'FInd out what Peter's heighr is.' Output: 'Peter's height is [number]'. Input:'{query}'. Output:")
    print(f"The new query is: {response}")

    #print(f"The context is {context}")
    #Get SQL query
    response = ask_llm(f"Convert the following query to SQL: {query}. Don't rename any of the tables in the query. The structure of the database is the following: {context}.")
    #print(f"The response query is:\n {response}")
    sql_query = extract(response, start_marker="```sql",end_marker="```" )
    print(f"The SQL query is: {sql_query}")

    #Initiate list for working with filtering conditions
    num_filter=llm_json(f"How many filters are applied to this query? Filters are expressed trhough the filtering procedure. {sql_query}",response_type=int)
    print(f"The number of filters is {num_filter}")
    filter_input = QUERY(query="SELECT region FROM customerdetails") 
    input_prompt=f'''For each applied filter. The number of applied filters should be {num_filter}, give me the an executable SQL query to identify the values for the columns on which a filtering operation is performed. Make sure to retrieve every filtering opearation seperately
                        Input:  
                        SELECT T1.product, T1.price
                        FROM salesdata AS T1
                        INNER JOIN customerdetails AS T2 ON T1.customer_id = T2.id
                        WHERE T2.region = 'west';

                        Output:
                        {filter_input}

                        Input: 
                        {sql_query}
                        Output:
                        '''
    # Filtering list
    queries=llm_json(prompt=input_prompt,response_type=list[QUERY])
    #print("The query is  ",queries[0]['query'])

    #For the category
    category_input = CATEGORY(category="west") 
    input_prompt=f'''For each filtering operation, give me the an executable SQL query to identify the values for the columns on which a filtering operation is performed.
                        Input:  
                        SELECT T1.product, T1.price
                        FROM salesdata AS T1
                        INNER JOIN customerdetails AS T2 ON T1.customer_id = T2.id
                        WHERE T2.region = 'west';

                        Output:
                        {category_input}

                        Return the category relevant to this query in the same order: {queries}
                        Input: 
                        {sql_query}
                        Output:
                        '''
    categories=llm_json(prompt=input_prompt,response_type=list[CATEGORY])
    #print("The query is  ",categories[0])
    
    #Make sure that the right ones are added together
    # Combine the lists into a new list of dictionaries
    combined_list = [
        {"query": query["query"], "category": category["category"]}
        for query, category in zip(queries, categories)
    ]

    print(combined_list[0]['query'])
    print(combined_list[0]['category'])

    updated_query=sql_query
    for i in combined_list:
        category=i['category']
        candidates=query_database(i['query'],False)
        print(f"The candidates are {candidates}")
        prompt=f"Return a list with the answer to the following questions. Considere for mismatches, different language and spellind differences [ "
        for i in candidates:
            prompt+=f"[Does {i} and {category} have the same semantic meaning?,"
        boolean_vector=llm_json(prompt,response_type=list[bool])
        print(f"The boolean vector is {boolean_vector}")
        candidates_with_true_boolean = [
            candidate 
            for candidate, is_true in zip(candidates, boolean_vector) 
            if is_true == True  # Correct: Check if is_true is equal to True
        ]
        print(f"The candidates with true boolean are {candidates_with_true_boolean}")

        response=ask_llm(f"Update the query {updated_query} with the information from the filtering opeartion. In the filtering opeation now also include via an or-statement the following values {candidates_with_true_boolean}")
        print("The response is ",response)
        test=extract(response, start_marker="```sql",end_marker="```" )
        if test == None:
            pass
        else:
            updated_query=test
        print(f"The updated query is {updated_query}")
        result=query_database(updated_query, True)
        print(f"The result is {result}")
    
    # print(f"The candidates are {candidates}")

    # #Create boolean vector for the modification of the query
    # category=filter_instances['category']
    # 

    # 
    # print("The vector is ",boolean_vector)
    # response=ask_llm(f"First let's deal with Filtering operation. Is there any in this query. If yes, give me the filtering operation in combination with the relevant table as a SQL query. If no, write 'No filtering operation'. Input: {sql_query}")
    # print(f"The response is {response}")
    # filter=extract(response, start_marker="```sql",end_marker="```" )
    # print(f"The filter applied is {filter}")
    # general_statement=ask_llm(f"Give me the following query without a 'WHERE' clause. Input: {sql_query}")
    # general_statement=extract(general_statement, start_marker="```sql",end_marker="```" )
    # print(f"The general statement is {general_statement}")
    # general_statement=ask_llm(f"Give me the following query without a 'WHERE' clause. Input: {sql_query}")
    # intent=ask_llm(f"Formulate the intent of this filtering operation {filter} for this query {sql_query} in one sentence.")
    # print(f"The intent is  {intent}. ")
    # table_wothout_filter=ask_llm(f"Give me the sql query name without the filtering condition.  {filter}")
    # table_wothout_filter=extract(table_wothout_filter,start_marker="```sql",end_marker="```")
    # print(f"The table without the filter is {table_wothout_filter} ")

    # rows=query_database(table_wothout_filter, False)
    # print("The rows are ",rows)
    
    # updated_filter=ask_llm(f"First think about this filter_query {filter}. What could be its motivation. Now consider the retrieved rows  {rows} Keep in mind, that semantic mismatches could occur. Do you think I should modify the filter_query to match the intent of it? ive out the modified query but only if it makes sense. Be brief.")
    # updated_filter=extract(updated_filter,start_marker="```sql",end_marker="```")
    # print(f"The updated filter is {updated_filter}")

    # filter_query=ask_llm(f"Combine the filter_query {updated_filter} with the initial query {sql_query} to get the final query. Give out the final query.")
    # filter_query=extract(filter_query,start_marker="```sql",end_marker="```")
    # print(f"The final query is {filter_query}")
    # query_database(filter_query, True)

    # sql_filter=ask_llm(f"Give me SQL query to retrieve the rows from the table needed  for this {filter}. From this {sql_query} with that intent {intent},")
    # sql_filter=extract(sql_filter,start_marker="```sql",end_marker="```")
    # print(f"The SQL filter is {sql_filter} ")
    # #Convert SQL to human language
    # subqueries = ask_llm(f'''If possible, rewrite this query such, that complicated statements are written into subqueries .Make sure both queries return the same result. Input: {sql_query}''')
    # subqueries= extract(subqueries, start_marker="```sql",end_marker="```" )
    # print(f"The subqueries are {subqueries}")

    # ordered_subqueries = ask_llm(f'''Give me a order of the queries such that I can execute them in a specific order please! Input: {subqueries}''')
    # print(f"The ordered subqueries are {ordered_subqueries}")
    # list_subqueries = extract(ordered_subqueries, start_marker="```sql",end_marker="```", multiple=True )
    # print(f"The list of subqueries are {list_subqueries}")

    # #Convert SQL to human language
    # instructions = ask_llm(f'''Verbalize this SQL query as instructions for an LLM: {sql_query} to natural language without any syntax. Write those instructions in an ordered way.''')

    # print(f"The instructions are {instructions}")
    # output=ask_llm(f"Perform the following instructions: {instructions} on the content {content}. Finally, answer the query: {query}. In each step write an explanation which information you used and whay you concluded like a great teacher.")
    # print(f"The output is {output}")

    

# Example usage
#query = "Find all songs by the artist who released the album Reputation in 2017."
#logic_sql_pipeline(query, ["songs", "artists", "albums"])

#logic_sql_pipeline(f'''Get the names and the amount of shares of all people owning a dog.''',['shareowner1row', 'animalowner1row'])
logic_sql_pipeline(f'''Get the names and the amount of shares of all people owning a dog, who's name is diego''',['shareowner1row', 'animalowner1row'])