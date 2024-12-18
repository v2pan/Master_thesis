from database import query_database , QueryExecutionError

sql='''SELECT * 
FROM doctors
WHERE doctors.patients_pd < 12;'''
try:
    query_database(sql)
except QueryExecutionError as e:
    print(f"{e}")

