from unittest import TestCase
from json_checker import json_checker


class JsonTypeTestCase(TestCase):

    def check_from_file(self):
        dict2 = {'b': 4, 'a': 2}
        is_equal, msg = json_checker.check_from_file('example.json', dict2)
        self.assertTrue(is_equal)

    def test_check_two_dict_structure_error_rank(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'b': 4, 'a': 2}

        is_equal, msg = json_checker.structure(dict1, dict2)
        self.assertTrue(is_equal)

    def test_check_two_dict_structure_equal(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'a': 2, 'b': 4}

        is_equal, msg = json_checker.structure(dict1, dict2)
        self.assertTrue(is_equal)

    def test_check_two_dict_structure_type(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'a': 2, 'b': 3.0}
        is_equal, msg = json_checker.structure(dict1, dict2)
        self.assertFalse(is_equal)
        self.assertEqual("error on value: dict1.b is <class 'int'>, dict2.b is <class 'float'>", msg)

    def test_check_two_dict_structure_not_equal(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'a': 2, 'c': 3}
        is_equal, msg = json_checker.structure(dict1, dict2)
        self.assertFalse(is_equal)
        res = ("dict2 do not have key: b" == msg) or ("dict1 do not have key: c" == msg)
        self.assertTrue(res)

    def test_check_two_dict_two_layer(self):
        dict1 = {'a': 1, 'b': 2, 'c': {'d': 1}}
        dict2 = {'a': 2, 'b': 3}

        is_equal, msg = json_checker.structure(dict1, dict2)
        self.assertFalse(is_equal)
        self.assertEqual("dict2 do not have key: c", msg)




