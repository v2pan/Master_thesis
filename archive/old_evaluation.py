#OLD Version

#Calculus and the expected result
# test_cases = [
#     (
#         '''∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)''',
#         {(2, 'Giovanni', '11'), (1, 'Peter', 'ten')},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃id ∃patients_pd (doctors(id, 'Peter', patients_pd) ∧ patients_pd < 12)''',
#         {(1, 'Peter', 'ten')},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃id ∃shares ∃name (shareowner1row(id, name, shares) ∧ animalowner1row(id, _, 'dog'))''',
#         {(1, 'Pierre', 20, 1, 'bill', 'chien')},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃id ∃shares ∃name (shareowner(id, name, shares) ∧ animalowner(id, _, 'dog'))''',
#         {(3, 'Diego', 15, 3, 'chris', 'dog'), (4, 'Marcel', 11, 4, 'juan', 'perro'), (1, 'Pierre', 20, 1, 'bill', 'chien')},
#         "row_calculus_pipeline"
#     ),
#     (   '''∃id ∃shares ∃name(shareowner(id, name, shares) ∧ ¬animalowner(id, _, 'dog'))''',
#         {(2, 'Vladi', 10, 2, 'diego', 'chat')},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃x ∃y ∃z (children_table(x, y) ∧ fathers(x, z))''',
#         {(0, 4, 'zero', 'Gerhard'), (1, 1, 'one', 'Joachim'), (2,'many', 'two', 'Dieter')},
#         "join_pipeline"
#     ),
#     (
#         '''∃id (children_table(id, ) ∧ fathers(id, _) ∧ mothers(id, _) )''',
#         {(1, '1', 'one', 'Joachim', 1, 'Julia'), (2, 'many', 'two', 'Dieter', 2, 'Petra')},
#         "join_pipeline"
#     ),
#     (
#         '''∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))''',
#         {(4, 'Michael', '18.01.1997', 4, 'Berlin Open', 4.0), (3, 'Xi', 'January 1986', 3, 'Warsaw Open', 3.0), (3, 'Xi', 'January 1986', 3, 'Osaka Open', 0.5)},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))''',
#         {('surviver1000', '1 million', 1, 'surviver1000', True), ('makeuptutorial', '1000 thousand', 3, 'makeuptutorial', False), ('surviver1000', '1 million', 2, 'surviver1000', True), ('princess', 'one thousand', 3, 'princess', True)},
#         "row_calculus_pipeline"
#     ),
#     (
#         '''∃id (children_table(id, >1) ∧ fathers(id, _))''',
#         {(0, '4', 'zero', 'Gerhard'), (2, 'many', 'two', 'Dieter')},
#         "combined_pipeline"
#     ),
#     (
#         '''ARTISTS(a,,), ALBUMS(,a,"Reputation",2017),SONGS(,a2,song_name,),ALBUMS(a2,a,)''',
#         {(1, 1, 'Reputation', '2017', 1, 'Taylor Swift', 'English', 1, 1, 'Delicate', '3:52'), (2, 2, 'Reputation', '2017', 2, 'Reputation Artist', 'English', 2, 2, 'New Year’s Day', '3:55')},
#         "combined_pipeline"
#     ),
#     (
#     '''∃d weather(d, city, temperature, rainfall) ∧ website_visits(d, page, visits)''',
#     {('2023 10 26', 'London', 12, 0, '2023 October 26', 'about', 500), ('2023 10 26', 'London', 12, 0, '2023 October 26', 'homepage', 1000), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'about', 500), ('2023 10 26', 'New York', 15, 2, '2023 October 26', 'homepage', 1000), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'contact', 200), ('2023 10 27', 'London', 10, 5, '2023 October 27', 'homepage', 1200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'contact', 200), ('2023 10 27', 'New York', 13, 1, '2023 October 27', 'homepage', 1200)}
#     ,"join_pipeline"
#     )

    

# ]