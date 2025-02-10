from database import query_database

print(query_database('''
SELECT airportname, city, shortname
FROM airport
LEFT JOIN airport_transl ON airport.airportname=airport_transl.fullname
LEFT JOIN airport_abrev ON airport_abrev.name=airport_transl.shortname;
'''))