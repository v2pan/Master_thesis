
# test_cases = [
#     {
#         "calculus":'''∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)''',
#         "answer":{(2, 'Giovanni', '11'), (1, 'Peter', 'ten')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 1,
#         "tables":['doctors'],
#         "initial_result" : "QueryExecutionError"
        
#     },
#     {   "calculus":'''∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog'))''',
#         "answer":{(2, 'Vladi', 10, 2, 'diego', 'chat')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2,
#         "tables":['shareowner', 'animalowner']
#     },
#     {
#         "calculus":'''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )''',
#         "answer":{(1, '1', 'one', 'Joachim', 1, 'Julia'), (2, 'many', 'two', 'Dieter', 2, 'Petra')},
#         "pipeline":"join_pipeline",
#         "tables_num": 2,
#         "tables":['children_table', 'fathers', 'mothers']
#     },
#     {
#         "calculus":'''∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))''',
#         "answer":{(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2,
#         "tables":['tennis_players', 'tournaments']
#     },
#     {
#         "calculus":'''∃id (children_table(id, >1) ∧ fathers(id, _))''',
#         "answer":{(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')},
#         "pipeline":"combined_pipeline",
#         "tables_num": 2,
#         "tables":['children_table', 'fathers']
#     },
# ]

#Old manual input
#Calculus and the expected result
# test_cases = [
#     {
#         "calculus":'''∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)''',
#         "answer":{(2, 'Giovanni', '11'), (1, 'Peter', 'ten')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 1,
        
#     },
#     {
#         "calculus":'''∃id ∃patients_pd (doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12)''',
#         "answer":{(1, 'Peter', 'ten')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 1
#     },
#     {
#         "calculus":'''∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog'))''',
#         "answer":{(1, 'Pierre', 20, 1, 'bill', 'chien')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))''',
#         "answer":{(3, 'Diego', 15, 3, 'chris', 'dog'), (4, 'Marcel', 11, 4, 'juan', 'perro'), (1, 'Pierre', 20, 1, 'bill', 'chien')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {   "calculus":'''∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog'))''',
#         "answer":{(2, 'Vladi', 10, 2, 'diego', 'chat')},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z))''',
#         "answer":{(0, 4, 'zero', 'Gerhard'), (1, 1, 'one', 'Joachim'), (2,'many', 'two', 'Dieter')},
#         "pipeline":"join_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )''',
#         "answer":{(1, '1', 'one', 'Joachim', 1, 'Julia'), (2, 'many', 'two', 'Dieter', 2, 'Petra')},
#         "pipeline":"join_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))''',
#         "answer":{(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))''',
#         "answer":{('surviver1000', '1 million', 1, 'surviver1000', True), ('makeuptutorial', '1000 thousand', 3, 'makeuptutorial', False), ('surviver1000', '1 million', 2, 'surviver1000', True), ('princess', 'one thousand', 3, 'princess', True)},
#         "pipeline":"row_calculus_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''∃id (children_table(id, >1) ∧ fathers(id, _))''',
#         "answer":{(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')},
#         "pipeline":"combined_pipeline",
#         "tables_num": 2
#     },
#     {
#         "calculus":'''ARTISTS(a,,), ALBUMS(,a,"Reputation",2017),SONGS(,a2,song_name,),ALBUMS(a2,a,)''',
#         "answer":{(1, 1, 'Reputation', '2017', 1, 'Taylor Swift', 'English', 1, 1, 'Delicate', '3:52'), (2, 2, 'Reputation', '2017', 2, 'Reputation Artist', 'English', 2, 2, 'New Year’s Day', '3:55')},
#         "pipeline":"combined_pipeline",
#         "tables_num": 3
#     },
#     {
#         "calculus":'''∃d weather(d, city, temperature, rainfall) ∧ website_visits(d, page, visits)''',
#         "answer":{('2023 10 26', 'London', 12, 0, '2023 October 26', 'about', 500), ('2023 10 26', 'London', 12, 0, '2023 October 26', 'homepage', 1000), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'about', 500), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'homepage', 1000), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'contact', 200), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'homepage', 1200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'contact', 200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'homepage', 1200)},
#         "pipeline":"join_pipeline",
#         "tables_num": 2
#     }
# ]