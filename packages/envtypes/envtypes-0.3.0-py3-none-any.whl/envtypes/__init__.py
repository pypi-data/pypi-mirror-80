import os
import re


class EnvTypes():
    """Can be configured the use or not of the prefix for environment fields,
       the prefix value for fields, delimitation between value and type,
       delimitation between list and tuple values, delimitation between
       dictionary key and value, name used for different environment types:
       strings, integers, booleans, lists, tuples and dictionaries.
       """

    def __init__(self, **kwargs):
        self.string = {'name': 'string', 'class': str, 'regex': r'[a-zA-Z]\w*',
                       'error': 'Are allowed only alpha-numeric characters and the underscore sign "_". It can start only with a letter.'}
        self.symbol = {'name': 'symbol', 'class': str, 'regex': r'[^a-zA-Z0-9]*',
                       'error': 'Are allowed all symbols without backslash "\".'}
        self.integer = {'name': 'integer', 'class': int, 'regex': r'\d*',
                        'error': 'Are allowed only digits from 0 to 9.'}
        self.boolean = {'name': 'boolean', 'class': bool, 'regex': r'',
                        'error': 'Are allowed only boolean values: "True" or "False".'}
        self.list = {'name': 'list', 'class': list, 'regex': r'', 'error': ''}
        self.tuple = {'name': 'tuple',
                      'class': tuple, 'regex': r'', 'error': ''}
        self.dictionary = {'name': 'dictionary',
                           'class': dict, 'regex': r'', 'error': ''}

        self.config_tag = {'name': 'config'}
        self.name_tag = {'name': 'name'}
        self.value_tag = {'name': 'value'}
        self.del_tag = {'name': 'delimiter'}
        self.type_tag = {'name': 'type'}

        self.case_sensitive = {
            'name': 'case_sensitive', 'value': True,
            'type': self.boolean, 'tag': self.config_tag}
        self.use_prefix = {
            'name': 'use_prefix', 'value': True,
            'type': self.boolean, 'tag': self.config_tag}
        self.prefix = {
            'name': 'prefix', 'value': 'PYTHON_',
            'type': self.string, 'tag': self.name_tag}
        self.env_del = {
            'name': 'env_del', 'value': ';__',
            'type': self.symbol, 'tag': self.del_tag}
        self.env_str = {
            'name': 'env_str', 'value': 'str', 'value_class': self.string,
            'type': self.string, 'tag': self.type_tag}
        self.env_int = {
            'name': 'env_int', 'value': 'int', 'value_class': self.integer,
            'type': self.string, 'tag': self.type_tag}
        self.env_bool = {
            'name': 'env_bool', 'value': 'bool', 'value_class': self.boolean,
            'type': self.string, 'tag': self.type_tag}
        self.bool_true_value = {
            'name': 'bool_true_value', 'value': 'True', 'value_class': self.boolean,
            'type': self.string, 'tag': self.value_tag}
        self.bool_false_value = {
            'name': 'bool_false_value', 'value': 'False', 'value_class': self.boolean,
            'type': self.string, 'tag': self.value_tag}
        self.env_list = {
            'name': 'env_list', 'value': 'list', 'value_class': self.list,
            'type': self.string, 'tag': self.type_tag}
        self.list_value_del = {
            'name': 'list_value_del', 'value': ' - ',
            'type': self.symbol, 'tag': self.del_tag}
        self.list_type_del = {
            'name': 'list_type_del', 'value': ', ',
            'type': self.symbol, 'tag': self.del_tag}
        self.env_tuple = {
            'name': 'env_tuple', 'value': 'tuple', 'value_class': self.tuple,
            'type': self.string, 'tag': self.type_tag}
        self.tuple_value_del = {
            'name': 'tuple_value_del', 'value': ' - ',
            'type': self.symbol, 'tag': self.del_tag}
        self.tuple_type_del = {
            'name': 'tuple_type_del', 'value': ', ',
            'type': self.symbol, 'tag': self.del_tag}
        self.env_dict = {
            'name': 'env_dict', 'value': 'dict', 'value_class': self.dictionary,
            'type': self.string, 'tag': self.type_tag}
        self.dict_key_del = {
            'name': 'dict_key_del', 'value': ': ',
            'type': self.symbol, 'tag': self.del_tag}
        self.dict_value_del = {
            'name': 'dict_value_del', 'value': ' - ',
            'type': self.symbol, 'tag': self.del_tag}
        self.dict_type_del = {
            'name': 'dict_type_del', 'value': ', ',
            'type': self.symbol, 'tag': self.del_tag}
        self.empty_value = {
            'name': 'empty_value', 'value': 'empty',
            'type': self.string, 'tag': self.value_tag}
        self.none_value = {
            'name': 'none_value', 'value': 'none',
            'type': self.string, 'tag': self.value_tag}

        self.arguments = [self.case_sensitive, self.use_prefix,
                          self.prefix, self.env_del, self.env_str,
                          self.env_int, self.env_bool, self.bool_true_value,
                          self.bool_false_value, self.env_list,
                          self.list_value_del, self.list_type_del,
                          self.env_tuple, self.tuple_value_del,
                          self.tuple_type_del, self.env_dict,
                          self.dict_key_del, self.dict_value_del,
                          self.dict_type_del, self.empty_value,
                          self.none_value]

        self.env_types = []
        self.env_dels = []
        self.list_dels = [self.list_value_del, self.list_type_del]
        self.tuple_dels = [self.tuple_value_del, self.tuple_type_del]
        self.dict_dels = [self.dict_key_del,
                          self.dict_value_del, self.dict_type_del]
        self.env_values = []

        for arg in self.arguments:
            if arg['tag'] == self.type_tag:
                self.env_types.append(arg)
            elif arg['tag'] == self.del_tag and arg['name'] != self.env_del['name']:
                self.env_dels.append(arg)
            elif arg['tag'] == self.value_tag:
                self.env_values.append(arg)

        for argument in self.arguments:
            self.user_argument = kwargs.get(argument['name'])
            if self.user_argument is not None:
                if (argument['type'] == self.string and
                    isinstance(self.user_argument, self.string['class']) and
                        re.match(self.string['regex'], self.user_argument)):
                    if not self.case_sensitive['value'] and argument['tag'] == self.type_tag:
                        argument['value'] = self.user_argument.lower().strip()
                    else:
                        argument['value'] = self.user_argument.strip()
                elif (argument['type'] == self.symbol and
                      isinstance(self.user_argument, self.symbol['class']) and
                        re.match(self.symbol['regex'], self.user_argument)):
                    argument['value'] = self.user_argument
                elif (argument['type'] == self.integer and
                        isinstance(self.user_argument, self.integer['class']) and
                        re.match(self.integer['regex'], self.user_argument)):
                    argument['value'] = self.user_argument
                elif (argument['type'] == self.boolean and
                      isinstance(self.user_argument, self.boolean['class'])):
                    argument['value'] = self.user_argument
                else:
                    raise ValueError(
                        f'The "{argument["name"]}" value must be a "{argument["type"]["name"]}". {argument["type"]["error"]}')

        for env_type_1 in self.env_types:
            for env_type_2 in self.env_types:
                if env_type_1['name'] != env_type_2['name']:
                    if env_type_1['value'] == env_type_2['value']:
                        raise ValueError(
                            f'The "{env_type_1["name"]}" value must be different from "{env_type_2["name"]}".')

        for type_del_argument in self.env_dels:
            if type_del_argument['value'] == self.env_del['value']:
                raise ValueError(
                    f'The "{self.env_del["name"]}" value must be different from "{type_del_argument["name"]}".')

        if self.list_type_del['value'] == self.list_value_del['value']:
            raise ValueError(
                f'The "{self.list_value_del["name"]}" value must be different from "{self.list_type_del["name"]}".')

        if self.tuple_type_del['value'] == self.tuple_value_del['value']:
            raise ValueError(
                f'The "{self.tuple_value_del["name"]}" value must be different from "{self.tuple_type_del["name"]}".')

        for env_dict_1 in self.dict_dels:
            for env_dict_2 in self.dict_dels:
                if env_dict_1['name'] != env_dict_2['name']:
                    if env_dict_1['value'] == env_dict_2['value']:
                        raise ValueError(
                            f'The "{env_dict_1["name"]}" must be different from "{env_dict_2["name"]}".')

        for env_value_1 in self.env_values:
            for env_value_2 in self.env_values:
                if env_value_1['name'] != env_value_2['name']:
                    if env_value_1['value'] == env_value_2['value']:
                        raise ValueError(
                            f'The "{env_value_1["name"]}" must be different from "{env_value_2["name"]}".')

    def check_argument_name(self, field_name):
        if field_name is not None:
            if field_name != '':
                # replace the ' ' with regex expression
                if not field_name.__contains__(' '):
                    if isinstance(field_name, str):
                        return True
                    else:
                        raise ValueError(
                            f'The value of the "field_name" argument from "set_env" methond must be a string. "{field_name}" is not a string.')
                else:
                    raise ValueError(
                        f'The value of the "field_name" argument from "set_env" method can not contains spaces.')
            else:
                raise ValueError(
                    f'The value of the "field_name" argument from "set_env" method can not be empty.')
        else:
            raise ValueError(
                f'The value of the "field_name" argument from "set_env" method can not be "None".')

    def check_env_existence(self, field_name, field_value):
        if field_value is not None:
            if field_value != '':
                return True
            else:
                raise ValueError(
                    f'The value of the "{field_name}" can not be empty.')
        else:
            raise ValueError(
                f'In .env file was not found any field with name "{field_name}".')

    def check_env_del(self, field_name, field_value):
        if self.env_del['value'] in field_value:
            if field_value.count(self.env_del['value']) == 1:
                return True
            else:
                raise ValueError(
                    f'The "{self.env_del["name"]}" value "{self.env_del["value"]}" was found {field_value.count(self.env_del["value"])} times in "{field_name}" field.')
        else:
            raise ValueError(
                f'The "{self.env_del["name"]}" value "{self.env_del["value"]}" was not found in "{field_name}" field.')

    def check_list_dels(self, field_name, field_value):
        value_del = field_value.count(self.list_value_del['value'])
        type_del = field_value.count(self.list_type_del['value'])
        for list_del in self.list_dels:
            if list_del['value'] in field_value:
                if (field_value.count(list_del['value']) >= 1 and
                        value_del - 1 == type_del):
                    return True
                else:
                    raise ValueError(
                        f'The field "{field_name}" has an inconsistent number of delimiters. The "{self.list_value_del["name"]}" delimiter should be one less than "{self.list_type_del["name"]}" delimiter.')
            else:
                raise ValueError(
                    f'The "{list_del["name"]}" value "{list_del["value"]}" was not found in "{field_name}" field.')

    def check_tuple_dels(self, field_name, field_value):
        value_del = field_value.count(self.tuple_value_del['value'])
        type_del = field_value.count(self.tuple_type_del['value'])
        for tuple_del in self.tuple_dels:
            if tuple_del['value'] in field_value:
                if (field_value.count(tuple_del['value']) >= 1 and
                        value_del - 1 == type_del):
                    return True
                else:
                    raise ValueError(
                        f'The field "{field_name}" has an inconsistent number of delimiters. The "{self.tuple_value_del["name"]}" delimiter should be one less than "{self.tuple_type_del["name"]}" delimiter.')
            else:
                raise ValueError(
                    f'The "{tuple_del["name"]}" value "{tuple_del["value"]}" was not found in "{field_name}" field.')

    def check_dict_dels(self, field_name, field_value):
        key_del = field_value.count(self.dict_key_del['value'])
        value_del = field_value.count(self.dict_value_del['value'])
        type_del = field_value.count(self.dict_type_del['value'])
        for dict_del in self.dict_dels:
            if dict_del['value'] in field_value:
                if (field_value.count(dict_del['value']) >= 1 and
                    key_del - 1 == type_del and key_del == value_del and
                        value_del - 1 == type_del):
                    return True
                else:
                    raise ValueError(
                        f'The field "{field_name}" has an inconsistent number of delimiters. The "{self.dict_key_del["name"]}" and "{self.dict_value_del["name"]}" delimiters should be one less than "{self.dict_type_del["name"]}" delimiter.')
            else:
                raise ValueError(
                    f'The "{dict_del["name"]}" value "{dict_del["value"]}" was not found in "{field_name}" field.')

    def check_env_type(self, field_name, field_type):
        for env_type in self.env_types:
            if field_type == env_type['value']:
                return True
        raise ValueError(
            f'The "{field_type}" was not set up as a type. The field "{field_name}" does not have a valid type value.')

    def convert_value(self, field_name, field_value, field_type):
        if field_type == self.env_str['value']:
            try:
                field_value = str(field_value)
            except ValueError:
                raise ValueError(
                    f'The value of the field "{field_name}", "{field_value}" can not be converted into "{self.env_str["value_class"]["name"]}".')
            else:
                if self.check_env_type(field_name, field_type):
                    return field_value
        elif field_type == self.env_int['value']:
            try:
                field_value = int(field_value)
            except ValueError:
                raise ValueError(
                    f'The value of the field "{field_name}", "{field_value}" can not be converted into "{self.env_int["value_class"]["name"]}".')
            else:
                if self.check_env_type(field_name, field_type):
                    return field_value
        elif field_type == self.env_bool['value']:
            if self.check_env_type(field_name, field_type):
                if field_value == self.bool_true_value['value']:
                    return True
                elif field_value == self.bool_false_value['value']:
                    return False
                else:
                    raise ValueError(
                        f'The value of the field "{field_name}", "{field_value}" was not set up as a boolean value.')

    def extract_value(self, field_name, field_value):
        if self.check_env_del(field_name, field_value):
            self.field_value = field_value.split(
                self.env_del['value'])[0].strip()
            if self.case_sensitive:
                self.field_type = field_value.split(
                    self.env_del['value'])[1].strip()
            else:
                self.field_type = field_value.split(
                    self.env_del['value'])[1].lower().strip()
            if self.field_value == self.empty_value['value']:
                return ''
            elif self.field_value == self.none_value['value']:
                return None
            else:
                if (self.field_type == self.env_str['value'] or
                    self.field_type == self.env_int['value'] or
                        self.field_type == self.env_bool['value']):
                    return self.convert_value(
                        field_name, self.field_value, self.field_type)
                elif self.field_type == self.env_list['value']:
                    the_list = []
                    if self.check_list_dels(field_name, self.field_value):
                        list_items = self.field_value.split(
                            self.list_type_del['value'])
                        for list_item in list_items:
                            list_item_value = list_item.split(
                                self.list_value_del['value'])[0]
                            list_item_type = list_item.split(
                                self.list_value_del['value'])[1]
                            the_list.append(self.convert_value(
                                field_name, list_item_value, list_item_type))
                        return the_list
                elif self.field_type == self.env_tuple['value']:
                    the_tuple = []
                    if self.check_tuple_dels(field_name, self.field_value):
                        tuple_items = self.field_value.split(
                            self.tuple_type_del['value'])
                        for tuple_item in tuple_items:
                            tuple_item_value = tuple_item.split(
                                self.tuple_value_del['value'])[0]
                            tuple_item_type = tuple_item.split(
                                self.tuple_value_del['value'])[1]
                            the_tuple.append(self.convert_value(
                                field_name, tuple_item_value, tuple_item_type))
                        return tuple(the_tuple)
                elif self.field_type == self.env_dict['value']:
                    the_dict = {}
                    if self.check_dict_dels(field_name, self.field_value):
                        dict_items = self.field_value.split(
                            self.dict_type_del['value'])
                        for dict_item in dict_items:
                            dict_item_key = dict_item.split(
                                self.dict_key_del['value'])[0]
                            dict_item_value = dict_item.split(
                                self.dict_key_del['value'])[1].split(
                                    self.dict_value_del['value'])[0]
                            dict_item_type = dict_item.split(
                                self.dict_value_del['value'])[1]
                            the_dict[dict_item_key] = self.convert_value(
                                field_name, dict_item_value, dict_item_type)
                        return the_dict

    def set_env(self, field_name):
        if self.check_argument_name(field_name):
            if self.use_prefix['value']:
                self.field_name = f"{self.prefix['value']}{field_name.upper().strip()}"
            else:
                self.field_name = field_name.upper().strip()
            self.value = os.getenv(self.field_name)
            if self.check_env_existence(self.field_name, self.value):
                return self.extract_value(
                    self.field_name, self.value)
