import unittest
from collections import OrderedDict
from deep_sorter import different_type_sorter


class TestSorter(unittest.TestCase):

    def test_multiple_lists(self):
        data = [[2, 'z', 'x', 3, 'w'], ['a', 1, 'b', 25]]
        exp_data = [[1, 25, 'a', 'b'], [2, 3, 'w', 'x', 'z']]
        self.assertEqual(different_type_sorter(data), exp_data)

    def test_multiple_dicts(self):
        data = [{1: {'A': 2}}, {4: 3}, {2: 3}]
        exp_data = [OrderedDict([(1, OrderedDict([('A', 2)]))]),
                    OrderedDict([(2, 3)]), OrderedDict([(4, 3)])]
        self.assertEqual(different_type_sorter(data), exp_data)

    def test_dicts_with_str_keys(self):
        data = [{'c': [2, 1]}, {'a': {'z': 0, 'y': [2, 1]}}]
        exp_data = [OrderedDict([('a', OrderedDict([('y', [1, 2]),
                    ('z', 0)]))]), OrderedDict([('c', [1, 2])])]
        self.assertEqual(different_type_sorter(data), exp_data)

    def test_dicts_with_int_keys(self):
        data = [{1: [2, 1]}, {2: {'z': 0, 'y': [2, 1]}}]
        exp_data = [OrderedDict([(1, [1, 2])]),
                    OrderedDict([(2, OrderedDict([('y', [1, 2]),
                                ('z', 0)]))])]
        self.assertEqual(different_type_sorter(data), exp_data)

    def test_complex_data(self):
        data = [1, '0', [{'c': [2, 1]},
                {'a': {'z': 0, 'y': [2, 1]}}, 0], 0, '1']
        exp_data = [0, 1, '0', '1',
                    [0, OrderedDict([('a',
                     OrderedDict([('y', [1, 2]), ('z', 0)]))]),
                     OrderedDict([('c', [1, 2])])]]
        self.assertEqual(different_type_sorter(data), exp_data)

    def test_complex_data_2(self):
        data = {'journeys': [{'id': 1, 'passengers': [1, 2], 'price': 100},
                {'id': 3, 'passengers': [2, 1], 'price': 200},
                {'id': 2, 'passengers': [4, 3], 'price': 150}, None]}
        exp_data = \
            OrderedDict([('journeys', [None, OrderedDict([('id', 1),
                         ('passengers', [1, 2]), ('price', 100)]),
                        OrderedDict([('id', 2),
                                     ('passengers', [3, 4]),
                                     ('price', 150)]),
                        OrderedDict([('id', 3),
                                     ('passengers', [1, 2]),
                                     ('price', 200)])])])
        self.assertEqual(different_type_sorter(data), exp_data)


if __name__ == '__main__':
    unittest.main()
