import unittest
from envtypes import EnvTypes
from dotenv import load_dotenv

load_dotenv()


class CustomArguments(unittest.TestCase):
    def setUp(self):
        self.custom = EnvTypes(case_sensitive=False,
                               use_prefix=False,
                               prefix='dJanGo',
                               env_del='___',
                               env_str='sTr',
                               env_int='INt',
                               env_bool='BOOl',
                               bool_true_value='True',
                               bool_false_value='False',
                               env_list='LiSt',
                               list_value_del=',,',
                               list_type_del=',_,',
                               env_tuple='TuPle',
                               tuple_value_del=',.,',
                               tuple_type_del=',-,',
                               env_dict='DicT',
                               dict_key_del='::',
                               dict_value_del=':=: ',
                               dict_type_del=';;',
                               empty_value='naDa',
                               none_value='nONE')

    def test_custom_arguments(self):
        self.values = [False, False, 'dJanGo', '___', 'str', 'int', 'bool',
                       'True', 'False', 'list', ',,', ',_,', 'tuple', ',.,',
                       ',-,', 'dict', '::', ':=: ', ';;', 'naDa', 'nONE']
        for index in self.values:
            self.assertEqual(
                self.custom.arguments[self.values.index(index)]['value'], index)


class Defaults(unittest.TestCase):
    def setUp(self):
        self.default = EnvTypes()

    def test_default_arguments(self):
        self.values = [True, True, 'PYTHON_', ';__', 'str', 'int', 'bool',
                       'True', 'False', 'list', ' - ', ', ', 'tuple', ' - ', ', ',
                       'dict', ': ', ' - ', ', ', 'empty', 'none']
        for index in self.values:
            self.assertEqual(
                self.default.arguments[self.values.index(index)]['value'], index)

    def test_argument_name(self):
        self.assertTrue(self.default.check_argument_name('test_1'))

    def test_env_existence(self):
        self.assertTrue(self.default.check_env_existence(
            'test_2', 'something_env_existence'))

    def test_env_del(self):
        self.assertTrue(self.default.check_env_del(
            'test_3', 'something_env_del;__str'))

    def test_list_dels(self):
        self.assertTrue(self.default.check_list_dels(
            'test_4', 'something_list - str, False - bool, 140 - int'))

    def test_tuple_dels(self):
        self.assertTrue(self.default.check_tuple_dels(
            'test_5', 'something_tuple - str, True - bool, 141 - int'))

    def test_dict_dels(self):
        self.assertTrue(self.default.check_dict_dels(
            'test_6', 'dict_key_1: something_dict - str, dict_key_2: True - bool, dict_key_3: 141 - int'))

    def test_env_type(self):
        self.assertTrue(self.default.check_env_type('test_7', 'int'))

    def test_convert_value_str(self):
        self.assertEqual(self.default.convert_value(
            'test_11', 'something_convert_value_str', 'str'), 'something_convert_value_str')

    def test_convert_value_int(self):
        self.assertEqual(self.default.convert_value(
            'test_12', 143, 'int'), 143)

    def test_convert_value_bool(self):
        self.assertEqual(self.default.convert_value(
            'test_13', 'False', 'bool'), False)

    def test_extract_value(self):
        self.assertEqual(self.default.extract_value(
            'test_14', 'some string from environment;__str'), 'some string from environment')

    def test_set_env_str(self):
        self.assertEqual(self.default.set_env(
            "string"), "some string from environment")

    def test_set_env_int(self):
        self.assertEqual(self.default.set_env(
            "integer"), 123)

    def test_set_env_bool(self):
        self.assertEqual(self.default.set_env(
            "boolean"), False)

    def test_set_env_list(self):
        self.assertEqual(self.default.set_env(
            "list"), ['something_list', 'again', False, 141])

    def test_set_env_tuple(self):
        self.assertEqual(self.default.set_env(
            "tuple"), ('something_tuple', 'again', True, 142))

    def test_set_env_dict(self):
        self.assertEqual(self.default.set_env(
            "dictionary"), {'dict_key_1': 'dict_string_value', 'dict_key_2': False, 'dict_key_3': 143})
