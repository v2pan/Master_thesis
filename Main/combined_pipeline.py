import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Main.join_pipeline import join_pipeline
from Main.row_calculus_pipeline import row_calculus_pipeline, get_relevant_tables, get_context, initial_query
from Utilities.extractor import extract
import sqlparse
from Utilities.database import query_database, QueryExecutionError
from Utilities.llm import RessourceError, add_metadata
import time
from Utilities.remove_duplicate_rows import remove_duplicate_rows
from Main.row_calculus_aux_pipeline import row_calculus_pipeline
from Main.join_pipeline_aux import join_pipeline

retry_delay = 60
#Analyze whether JOIN or WHERE clause appear, retrieve the relevant ones
def analyze_sql_query(sql_query):
    """
    Analyzes an SQL query to detect WHERE and JOIN conditions.

    Args:
        sql_query: The SQL query string.

    Returns:
        A dictionary containing boolean flags for WHERE and JOIN conditions, 
        and lists of their respective tokens (if found).  Returns an error 
        message if sqlparse fails to parse the query.
    """
    try:
        parsed = sqlparse.parse(sql_query)[0]
    except IndexError:
        return "Error: sqlparse failed to parse the query. Check for syntax errors."

    where_clause = None
    where_conditions = []
    join_conditions = []
    for token in parsed.tokens:
        if isinstance(token, sqlparse.sql.Where):
            where_conditions.append(token) 

        if isinstance(token, sqlparse.sql.Comparison):
            # Extract the condition from the JOIN clause (this part is tricky and may need refinement 
            # depending on the complexity of JOIN conditions).
            join_conditions.append(token)


    return  where_conditions, join_conditions


TOTAL_DIC = {}

#Combination of both pipeline, adjustment was necessary
def combined_pipeline(query, evaluation=False, aux=False, initial_sql_query=None, threshold=None, two_step=None): 

    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    if aux==False:
        from Main.join_pipeline import join_pipeline
        from Main.row_calculus_pipeline import row_calculus_pipeline
    elif aux==True:
        from Main.join_pipeline_aux import join_pipeline
        from Main.row_calculus_aux_pipeline import row_calculus_pipeline
        

    #Metadata to keep track of use 
    global TOTAL_DIC  # Declare it as global to modify it
    TOTAL_DIC.clear()

    global usage_metadata_total
    usage_metadata_total = {
                "prompt_token_count": 0,
                "candidates_token_count": 0,
                "total_token_count": 0,
                "total_calls": 0
            }
    

    total_count=0
    total_retries=4

    if "SELECT" in query:
        initial_sql_query=query
    
    elif initial_sql_query is None:
        while total_count<total_retries:
            #Get context
            count=0
            while count<total_retries:
                tables, temp_meta = get_relevant_tables(query, return_metadata=True)
                usage_metadata_total=add_metadata(temp_meta, usage_metadata_total)
                if tables is not None:
                    break
                else:
                    count+=1

            if tables is None:
                return None
            
            print(f"The relevant tables are {tables}")
            context = get_context(tables)

            #Optional, if were to use JSON files
            #Gets context by reading JSON files
            #context= get_context_json(tables)

            print(f"The context is {context}")
            print(f"The query is {query}")

            #Used for predicate calculus, selecting all rows
            response, temp_meta = initial_query(query,context)
            
            #Update the metadata
            add_metadata(temp_meta, usage_metadata_total)

            #Extract the SQL query from the response
            initial_sql_query = extract(response, start_marker="```sql",end_marker="```" )
            print(f"The SQL query is: {initial_sql_query}")

            #Check whether the SQL query is invalid
            try:
                initial_query_result=query_database(initial_sql_query)
            except QueryExecutionError as e:
                initial_query_result=f"{e}"
                initial_query_result=initial_query_result.split('\n')[0]
                if "column" in initial_query_result.lower() and "not exists" in initial_query_result.lower():
                    total_count+=1
                else: 
                    break

    else: 
        try:
            initial_query_result=query_database(initial_sql_query)
        except QueryExecutionError as e:
            #raise Exception("The initial SQL query is invalid")
            print("The initial SQL query is invalid")


    #Now analyze the SQL query for WHERE and JOIN conditions
    where_conditions, join_conditions = analyze_sql_query(initial_sql_query)

    print("--------------------------------------")
    
    output_query=None

    if not evaluation:
        
        #First Problematic Join
        if join_conditions and where_conditions:
            print(f"The \n{initial_sql_query}\n has a JOIN clause.")
            output_query, temp_meta=join_pipeline(initial_sql_query, forward=True, return_metadata=True)
            add_metadata(temp_meta, usage_metadata_total)
            output, temp_meta=row_calculus_pipeline(output_query, return_metadata=True)
            add_metadata(temp_meta, usage_metadata_total)

        #Then WHERE clause
        elif where_conditions:
            print(f"The \n”{initial_sql_query}\n has a WHERE clause.")
            output, temp_meta=row_calculus_pipeline(initial_sql_query, return_metadata=True, threshold=threshold, two_step=two_step)
            add_metadata(temp_meta, usage_metadata_total)
        
        elif join_conditions:
            print(f"The \n{initial_sql_query}\n has a JOIN clause.")
            # output, temp_meta=join_pipeline(initial_sql_query, return_metadata=True)
            output, temp_meta=join_pipeline(initial_sql_query, return_metadata=True, threshold= threshold, two_step=two_step)
            add_metadata(temp_meta, usage_metadata_total)
        else:
            print(f"The \n{initial_sql_query}\n has no WHERE or JOIN clause.")
            
        
        print(f"The output is {output}")
        print(f"The metadata is {usage_metadata_total}")
        return remove_duplicate_rows(output,TOTAL_DIC), usage_metadata_total
    
    else:
        #Initialize with None values
        initial_sql_query_where, semantic_list_where, result_where = None, None, None
        initial_sql_query_join, semantic_list_join, result_join = None, None, None
        output=None

        if join_conditions and where_conditions:
            print(f"The \n{initial_sql_query}\n has a JOIN clause.")
            initial_sql_query_join, semantic_list_join, result_join, temp_meta=join_pipeline(initial_sql_query, return_query=False, forward=True, evaluation=True,  return_metadata=True)
            add_metadata(temp_meta, usage_metadata_total)
            max_retries = 3  # Set the maximum number of retries
            retry_count = 0
            while retry_count < max_retries:
                try:
                    initial_sql_query_where, semantic_list_where, result_where, temp_meta = row_calculus_pipeline(result_join, evaluation=True, return_metadata=True)
                    add_metadata(temp_meta, usage_metadata_total)
                    break  # Exit the loop if successful
                except RessourceError:
                    retry_count += 1
                    print(f"Sleeping for {retry_delay} seconds (attempt {retry_count}/{max_retries})")
                    time.sleep(retry_delay)
                except TypeError:
                    print("TypeError has occured")

            if retry_count == max_retries:
                print("Maximum retries exceeded.  Giving up.")
            output=result_where

        #Then WHERE clause
        elif where_conditions:
            print(f"The \n”{initial_sql_query}\n has a WHERE clause.")
            initial_sql_query_where, semantic_list_where, result_where, temp_meta=row_calculus_pipeline(initial_sql_query, evaluation=True, return_metadata=True)
            add_metadata(temp_meta, usage_metadata_total)
            output=result_where
        
        elif join_conditions:
            print(f"The \n{initial_sql_query}\n has a JOIN clause.")
            initial_sql_query_join, semantic_list_join, result_join, temp_meta=join_pipeline(initial_sql_query, evaluation=True, return_metadata=True)
            add_metadata(temp_meta, usage_metadata_total)
            output=result_join
        
        else:
            print(f"The \n{initial_sql_query}\n has no WHERE or JOIN clause.")
            
        
        print(f"The modified query is {output_query}")
        print(f"The metadata is {usage_metadata_total}")
        
        #Correct this for this analysis please
        if result_where is not None:
            result_where = remove_duplicate_rows(result_where,TOTAL_DIC)
        if result_join is not None:
            result_join = remove_duplicate_rows(result_join,TOTAL_DIC)
        return initial_sql_query_join, semantic_list_join, result_join, initial_sql_query_where, semantic_list_where, result_where, remove_duplicate_rows(output,TOTAL_DIC), usage_metadata_total


def hard_pipeline(query):
    #Metadata to keep track of use 

    global usage_metadata_total
    usage_metadata_total = {
                "prompt_token_count": 0,
                "candidates_token_count": 0,
                "total_token_count": 0,
                "total_calls": 0
            }
    

    total_count=0
    total_retries=4

    while total_count<total_retries:
        #Get context
        count=0
        while count<total_retries:
            tables, temp_meta = get_relevant_tables(query, return_metadata=True)
            usage_metadata_total=add_metadata(temp_meta, usage_metadata_total)
            if tables is not None:
                break
            else:
                count+=1

        if tables is None:
            return None
        
        print(f"The relevant tables are {tables}")
        context = get_context(tables)

        #Optional, if were to use JSON files
        #Gets context by reading JSON files
        #context= get_context_json(tables)

        print(f"The context is {context}")
        print(f"The query is {query}")

        #Used for predicate calculus, selecting all rows
        response, temp_meta = initial_query(query,context)
        
        #Update the metadata
        add_metadata(temp_meta, usage_metadata_total)

        #Extract the SQL query from the response
        initial_sql_query = extract(response, start_marker="```sql",end_marker="```" )
        print(f"The SQL query is: {initial_sql_query}")

        #Check whether the SQL query is invalid
        try:
            initial_query_result=query_database(initial_sql_query)
        except QueryExecutionError as e:
            initial_query_result=[]
        return initial_query_result, temp_meta




