#Testing whether test class works correctly
import unittest
import os
from unittest.mock import patch, MagicMock
import warnings

from evaluation import test_cases
from test_evaluation import initial_query_transform, process_list, compare_lists_of_lists, load_data, error_logic



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


if __name__ == '__main__':
    unittest.main()

