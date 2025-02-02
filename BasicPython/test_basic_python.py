import unittest
from basic_python import sort

class TestSortFunction(unittest.TestCase):
    def test_sort_empty_list(self):
        self.assertEqual(sort([]), [])

    def test_sort_single_element_list(self):
        self.assertEqual(sort([1]), [1])

    def test_sort_sorted_list(self):
        self.assertEqual(sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_sort_unsorted_list(self):
        self.assertEqual(sort([5, 3, 1, 4, 2]), [1, 2, 3, 4, 5])

    def test_sort_reverse_sorted_list(self):
        self.assertEqual(sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_sort_list_with_duplicates(self):
        self.assertEqual(sort([3, 1, 2, 3, 1]), [1, 1, 2, 3, 3])

if __name__ == '__main__':
    unittest.main()