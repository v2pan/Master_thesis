from join_pipeline import join_pipeline
from row_calculus_pipeline import row_calculus_pipeline

#Combination of both pipeline, adjustment was necessary
def combined_pipeline(calculus):
    sql_query = join_pipeline(calculus,return_query=True)
    result=row_calculus_pipeline(sql_query)
    print(result)
    return result


