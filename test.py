from database import query_database

query_database('''SELECT doctors.id, doctors.name, doctors.patients_pd 
FROM doctors 
WHERE doctors.patients_pd = '11' OR doctors.patients_pd = 'ten';''')