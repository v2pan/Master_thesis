from database import query_database , QueryExecutionError

sql="SELECT *FROM shareowner1row LEFT JOIN animalowner ON shareowner1row.id = animalowner.owner_id WHERE animalowner.category <> 'dog' OR animalowner.category IS NULL;"
try:
    query_database(sql)
except QueryExecutionError as e:
    print(f"{e}")

