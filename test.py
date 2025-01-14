#Testing whether test class works correctly
import unittest
import os
from unittest.mock import patch, MagicMock
import warnings

from evaluation import test_cases
from test_evaluation import initial_query_transform,  compare_lists_of_lists, load_data, error_logic, comparison_logic



class TestEvaluationPipeline(unittest.TestCase):

    def test_compare_lists_of_two_lists1(self):
        list1 = [[1,2,3],[4,5,6],[7,8,9]]
        list2 = [[1,3, 2],[4,5,6],[7,9,8]]
        self.assertTrue(compare_lists_of_lists(list1, list2))

        list1 = [{1,2,3},{4,5,6},{7,8,9}]
        list2 = [[1,3, 2],[4,5,6],[7,9,8]]
        # list1=process_list(list1)
        # list2 = process_list(list2)
        self.assertTrue(compare_lists_of_lists(list1, list2))
    
    def test_comparison_logic_initial_join(self):
        result_dic= {
        "calculus": "∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))",
        "initial_sql_query_join": "SELECT * FROM influencers INNER JOIN followers ON influencers.media_name = followers.following WHERE influencers.clicks > 500;",
        "semantic_list_join": [
            {
                "makeuptutorial": [
                    "makeuptutorial"
                ],
                "outsideguy": [],
                "surviver1000": [
                    "surviver1000",
                    "surviver10"
                ],
                "princess": [
                    "princess"
                ]
            }
        ],
        "result_join": "SELECT *\nFROM influencers\nINNER JOIN followers ON influencers.media_name = CASE followers.following\n    WHEN 'makeuptutorial' THEN 'makeuptutorial'\n    WHEN 'surviver1000' THEN 'surviver1000'\n    WHEN 'princess' THEN 'princess'\n    END\nWHERE influencers.clicks > 500;",
        "initial_sql_query_where": "SELECT * FROM influencers INNER JOIN followers ON influencers.media_name = followers.following WHERE influencers.clicks > 500;",
        "semantic_list_where": [
            [
                [
                    "1000 thousand"
                ],
                [
                    "1 million"
                ],
                [
                    "one thousand"
                ],
                "WHERE influencers.clicks > 500;"
            ]
        ],
        "result_where": [
            [
                "surviver1000",
                "1 million",
                1,
                "surviver1000",
                True
            ],
            [
                "makeuptutorial",
                "1000 thousand",
                3,
                "makeuptutorial",
                False
            ],
            [
                "surviver1000",
                "1 million",
                2,
                "surviver1000",
                True
            ],
            [
                "princess",
                "one thousand",
                3,
                "princess",
                True
            ]
        ],
        "output": [
            [
                "surviver1000",
                "1 million",
                1,
                "surviver1000",
                True
            ],
            [
                "makeuptutorial",
                "1000 thousand",
                3,
                "makeuptutorial",
                False
            ],
            [
                "surviver1000",
                "1 million",
                2,
                "surviver1000",
                True
            ]
        ]
        }

        target_instance= {
        "calculus": "∃m ∃f ∃i (influencers(m, f) ∧ f > 500 ∧ followers(i, m, z))",
        "initial_sql_query_join": "SELECT * FROM influencers INNER JOIN followers ON influencers.media_name = followers.following WHERE influencers.clicks > 500;",
        "semantic_list_join": [
            {
                "makeuptutorial": [
                    "makeuptutorial"
                ],
                "outsideguy": [],
                "surviver1000": [
                    "surviver1000",
                    "surviver1000"
                ],
                "princess": [
                    "princess"
                ]
            }
        ],
        "result_join": "SELECT *\nFROM influencers\nINNER JOIN followers ON influencers.media_name = CASE followers.following\n    WHEN 'makeuptutorial' THEN 'makeuptutorial'\n    WHEN 'surviver1000' THEN 'surviver1000'\n    WHEN 'princess' THEN 'princess'\n    END\nWHERE influencers.clicks > 500;",
        "initial_sql_query_where": "SELECT * FROM influencers INNER JOIN followers ON influencers.media_name = followers.following WHERE influencers.clicks > 500;",
        "semantic_list_where": [
            [
                [
                    "1000 thousand"
                ],
                [
                    "1 million"
                ],
                [
                    "one thousand"
                ],
                "WHERE influencers.clicks > 500;"
            ]
        ],
        "result_where": [
            [
                "surviver1000",
                "1 million",
                1,
                "surviver1000",
                True
            ],
            [
                "makeuptutorial",
                "1000 thousand",
                3,
                "makeuptutorial",
                False
            ],
            [
                "surviver1000",
                "1 million",
                2,
                "surviver1000",
                True
            ],
            [
                "princess",
                "one thousand",
                3,
                "princess",
                True
            ]
        ],
        "output": [
            [
                "surviver1000",
                "1 million",
                1,
                "surviver1000",
                True
            ],
            [
                "makeuptutorial",
                "1000 thousand",
                3,
                "makeuptutorial",
                False
            ],
            [
                "surviver1000",
                "1 million",
                2,
                "surviver1000",
                True
            ],
            [
                "princess",
                "one thousand",
                3,
                "princess",
                True
            ]
        ]
        }
        error_result= comparison_logic(result_dic, target_instance)
        error_supposed={"initial_sql_query_join": 0, "semantic_list_join": 1, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 0, "result_where": 0,  "correct_results": 0}
        self.assertEqual(error_result,error_supposed )

    def test_comparison_logic_initial_join(self):
        result_dic={"calculus": "∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))",
        "initial_sql_query_join": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = '18.01.1997';",
        "semantic_list_join": [
            {}
        ],
        "result_join": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "initial_sql_query_where": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "semantic_list_where": [
            [
                [
                    "January 1986"
                ],
                [
                    "18.01.1997"
                ],
                "WHERE tennis_players.born = 'January';"
            ]
        ],
        "result_where": [
            [
                4,
                "Michael",
                "18.01.1997",
                4,
                "Berlin Open",
                4.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Warsaw Open",
                3.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Osaka Open",
                0.5
            ]
        ],
        "output": [
            [
                4,
                "Michael",
                "18.01.1997",
                4,
                "Berlin Open",
                4.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Warsaw Open",
                3.0
            ]
        ]
        }

        target_instance={"calculus": "∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))",
        "initial_sql_query_join": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "semantic_list_join": [
            {}
        ],
        "result_join": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "initial_sql_query_where": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "semantic_list_where": [
            [
                [
                    "January 1986"
                ],
                [
                    "18.01.1997"
                ],
                "WHERE tennis_players.born = 'January';"
            ]
        ],
        "result_where": [
            [
                4,
                "Michael",
                "18.01.1997",
                4,
                "Berlin Open",
                4.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Warsaw Open",
                3.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Osaka Open",
                0.5
            ]
        ],
        "output": [
            [
                4,
                "Michael",
                "18.01.1997",
                4,
                "Berlin Open",
                4.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Warsaw Open",
                3.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Osaka Open",
                0.5
            ]
        ]
        }

        error_result= comparison_logic(result_dic, target_instance)
        error_supposed={"initial_sql_query_join": 1, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 0, "result_where": 0,  "correct_results": 0}
        self.assertEqual(error_result,error_supposed )

    def test_comparison_logic_result_join(self):
        result_dic={"calculus": "∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))",
        "initial_sql_query_join": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "semantic_list_join": [
            {}
        ],
        "result_join": "SELECT *  FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = '18.01.1997';",
        "initial_sql_query_where": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "semantic_list_where": [
            [
                [
                    "January 1986"
                ],
                [
                    "18.01.1997"
                ],
                "WHERE tennis_players.born = 'January';"
            ]
        ],
        "result_where": [
            [
                4,
                "Michael",
                "18.01.1997",
                4,
                "Berlin Open",
                4.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Warsaw Open",
                3.0
            ]
        ],
        "output": [
            [
                4,
                "Michael",
                "18.01.1997",
                4,
                "Berlin Open",
                4.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Warsaw Open",
                3.0
            ]
        ]
        }

        target_instance={"calculus": "∃id (tennis_players(id, _, 'January') ∧ tournaments(id, name, price_money))",
        "initial_sql_query_join": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "semantic_list_join": [
            {}
        ],
        "result_join": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "initial_sql_query_where": "SELECT * FROM tennis_players INNER JOIN tournaments ON tennis_players.id = tournaments.winner_id WHERE tennis_players.born = 'January';",
        "semantic_list_where": [
            [
                [
                    "January 1986"
                ],
                [
                    "18.01.1997"
                ],
                "WHERE tennis_players.born = 'January';"
            ]
        ],
        "result_where": [
            [
                4,
                "Michael",
                "18.01.1997",
                4,
                "Berlin Open",
                4.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Warsaw Open",
                3.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Osaka Open",
                0.5
            ]
        ],
        "output": [
            [
                4,
                "Michael",
                "18.01.1997",
                4,
                "Berlin Open",
                4.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Warsaw Open",
                3.0
            ],
            [
                3,
                "Xi",
                "January 1986",
                3,
                "Osaka Open",
                0.5
            ]
        ]
        }

        error_result= comparison_logic(result_dic, target_instance)
        error_supposed={"initial_sql_query_join": 0, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 0, "result_where": 1,  "correct_results": 0}
        self.assertEqual(error_result,error_supposed )
        

    
    def test_comparison_logic_same(self):
        
        result_dic={
        "calculus": "∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)",
        "initial_sql_query_join": None,
        "semantic_list_join": None,
        "result_join": None,
        "initial_sql_query_where": "SELECT *  FROM doctors WHERE doctors.patients_pd < 12;",
        "semantic_list_where": [
            [
                [
                    "ten"
                ],
                [
                    "11"
                ],
                "WHERE doctors.patients_pd < 12;"
            ]
        ],
        "result_where": [
            [
                1,
                "Peter",
                "ten"
            ],
            [
                2,
                "Giovanni",
                "11"
            ]
        ],
        "output": [
            [
                1,
                "Peter",
                "ten"
            ],
            [
                2,
                "Giovanni",
                "11"
            ]
        ]
        }

        target_instance={
        "calculus": "∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)",
        "initial_sql_query_join": None,
        "semantic_list_join": None,
        "result_join": None,
        "initial_sql_query_where": "SELECT *  FROM doctors WHERE doctors.patients_pd < 12;",
        "semantic_list_where": [
            [
                [
                    "ten"
                ],
                [
                    "11"
                ],
                "WHERE doctors.patients_pd < 12;"
            ]
        ],
        "result_where": [
            [
                1,
                "Peter",
                "ten"
            ],
            [
                2,
                "Giovanni",
                "11"
            ]
        ],
        "output": [
            [
                1,
                "Peter",
                "ten"
            ],
            [
                2,
                "Giovanni",
                "11"
            ]
        ]
        }
        error_result= comparison_logic(result_dic, target_instance)
        error_supposed={"initial_sql_query_join": 0, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 0, "result_where": 0,  "correct_results": 1}
        self.assertEqual(error_result,error_supposed )

    def test_comparison_logic_fail_list_where(self):
        
            result_dic={
            "calculus": "∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)",
            "initial_sql_query_join": None,
            "semantic_list_join": None,
            "result_join": None,
            "initial_sql_query_where": "SELECT *  FROM doctors WHERE doctors.patients_pd < 12;",
            "semantic_list_where": [
                [
                    [
                        "ten"
                    ],
                    [
                        "11"
                    ],
                    [
                        "fourty"
                    ],
                    "WHERE doctors.patients_pd < 12;"
                ]
            ],
            "result_where": [
                [
                    1,
                    "Peter",
                    "ten"
                ],
                [
                    2,
                    "Giovanni",
                    "11"
                ]
            ],
            "output": [
                [
                    1,
                    "Peter",
                    "ten"
                ],
                [
                    2,
                    "Giovanni",
                    "11"
                ]
            ]
            }

            target_instance={
            "calculus": "∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)",
            "initial_sql_query_join": None,
            "semantic_list_join": None,
            "result_join": None,
            "initial_sql_query_where": "SELECT *  FROM doctors WHERE doctors.patients_pd < 12;",
            "semantic_list_where": [
                [
                    [
                        "ten"
                    ],
                    [
                        "11"
                    ],
                    "WHERE doctors.patients_pd < 12;"
                ]
            ],
            "result_where": [
                [
                    1,
                    "Peter",
                    "ten"
                ],
                [
                    2,
                    "Giovanni",
                    "11"
                ]
            ],
            "output": [
                [
                    1,
                    "Peter",
                    "ten"
                ],
                [
                    2,
                    "Giovanni",
                    "11"
                ],
                 [
                    3,
                    "XXXX",
                    "XXX"
                ]
            ]
            }
            error_result= comparison_logic(result_dic, target_instance)
            error_supposed={"initial_sql_query_join": 0, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 0, "semantic_list_where": 1, "result_where": 0,  "correct_results": 0}
            self.assertEqual(error_result,error_supposed )

    def test_comparison_logic_fail_initial_where(self):
        
            result_dic={
            "calculus": "∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)",
            "initial_sql_query_join": None,
            "semantic_list_join": None,
            "result_join": None,
            "initial_sql_query_where": "SELECT * FROM doctors WHERE doctors.patients_pd = 'ten' ;",
            "semantic_list_where": [
                [
                    [
                        "ten"
                    ],
                    [
                        "11"
                    ],
                    [
                        "fourty"
                    ],
                    "WHERE doctors.patients_pd < 12;"
                ]
            ],
            "result_where": [
                [
                    1,
                    "Peter",
                    "ten"
                ],
                [
                    2,
                    "Giovanni",
                    "11"
                ]
            ],
            "output": [
                [
                    1,
                    "Peter",
                    "ten"
                ],
                [
                    2,
                    "Giovanni",
                    "11"
                ]
            ]
            }

            target_instance={
            "calculus": "∃id ∃name ∃patients_pd (doctors(id, name, patients_pd) ∧ patients_pd < 12)",
            "initial_sql_query_join": None,
            "semantic_list_join": None,
            "result_join": None,
            "initial_sql_query_where": "SELECT *  FROM doctors WHERE doctors.patients_pd < 12;",
            "semantic_list_where": [
                [
                    [
                        "ten"
                    ],
                    [
                        "11"
                    ],
                    "WHERE doctors.patients_pd < 12;"
                ]
            ],
            "result_where": [
                [
                    1,
                    "Peter",
                    "ten"
                ],
                [
                    2,
                    "Giovanni",
                    "11"
                ]
            ],
            "output": [
                [
                    1,
                    "Peter",
                    "ten"
                ],
                [
                    2,
                    "Giovanni",
                    "11"
                ],
                [
                    3,
                    "XXX",
                    "XX"
                ]
            ]
            }
            error_result= comparison_logic(result_dic, target_instance)
            error_supposed={"initial_sql_query_join": 0, "semantic_list_join": 0, "result_join": 0, "initial_sql_query_where": 1, "semantic_list_where": 0, "result_where": 0,  "correct_results": 0}
            self.assertEqual(error_result,error_supposed )
    


        
    
    


if __name__ == '__main__':
    unittest.main()

