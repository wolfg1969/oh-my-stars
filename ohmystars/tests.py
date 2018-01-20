import unittest

from index import update_inverted_index

__author__ = 'guoyong'


class IndexTest(unittest.TestCase):

    def setUp(self):
        self.index = {
            'python': []
        }

    def test_update_inverted_index_empty(self):
        update_inverted_index(self.index, 'python', 1, 2, 3)
        self.assertEqual([1, 2, 3], self.index.get('python'))

    def test_update_inverted_index_duplicate_item(self):
        update_inverted_index(self.index, 'python', 1, 2, 3)
        update_inverted_index(self.index, 'python', 3)
        self.assertEqual([1, 2, 3], self.index.get('python'))

    def test_update_inverted_index_sorted(self):
        update_inverted_index(self.index, 'python', 3, 1, 2)
        self.assertEqual([1, 2, 3], self.index.get('python'))

