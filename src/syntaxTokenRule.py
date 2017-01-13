import re
from src.token import Token
from src.ruleScanner import RuleScanner

class SyntaxTokenRule():
    def __init__(self, token_split_char = None):
        self.__token_type__ = ''
        self.__type_modifier__ = ''
        self.__token_value__ = ''
        self.__value_modifier__ = ''
        self.__occurrences__ = ''
        self.__min_occurrences__ = ''
        self.__max_occurrences__ = ''
        self.__token_split_char__ = token_split_char or ','
        self.E_pattern_issue = Exception()

    @property
    def token_split_char(self):
        return self.__token_split_char__

    @property
    def token_type(self):
        return self.__token_type__

    @property
    def token_value(self):
        return self.__token_value__

    @property
    def token_occurrences(self):
        return self.__occurrences__

    @property
    def min_occurrences(self):
        return int(self.__min_occurrences__)

    @property
    def max_occurrences(self):
        return int(self.__max_occurrences__)

    @token_type.setter
    def token_type (self, token_type):
        if len(token_type) == 0:
            self.__type_modifier__ = ''
            self.__token_type__ = ''
            return

        if token_type[0] in ('>','<','!','='):
            self.__type_modifier__ = token_type[0]
        remain = token_type[len(self.__type_modifier__):]

        if remain[0] == self.token_split_char:
            self.__token_type__ = remain[1:].strip(' ')
        else:
            self.__token_type__ = remain.strip(' ')

    @token_value.setter
    def token_value(self, token_value):
        if len(token_value) == 0:
            self.__value_modifier__=''
            self.__token_value__=''
            return

        if token_value[0] in ('>','<','!','='):
            self.__value_modifier__ = token_value[0]
        remain = token_value[len(self.__value_modifier__):]
        if remain[0] == self.token_split_char:
            self.__token_value__ = remain[1:].strip(' ')
        else:
            self.__token_value__ = remain.strip(' ')

    @token_occurrences.setter
    def token_occurrences (self, token_occurrences):
        self.__occurrences__ = token_occurrences
        if token_occurrences == '':
            self.__min_occurrences__ = 1
            self.__max_occurrences__ = 1
        elif token_occurrences == '*':
            self.__min_occurrences__ = 0
            self.__max_occurrences__ = 0
        elif token_occurrences == '+':
            self.__min_occurrences__ = 1
            self.__max_occurrences__ = 0
        elif token_occurrences == '?':
            self.__min_occurrences__ = 0
            self.__max_occurrences__ = 1
        elif token_occurrences[0] == '[' and token_occurrences[-1] == ']':
            self.__min_occurrences__ = re.match('[0-9]*', token_occurrences[1:]).group(0)
            if token_occurrences[1+len(self.__min_occurrences__)] == self.token_split_char:
                self.__max_occurrences__ = re.match('[0-9]*', token_occurrences[2+len(self.__min_occurrences__):]).group(0)
            else:
                self.__max_occurrences__ = self.__min_occurrences__
        else:
            raise self.E_pattern_issue(token_occurrences)

    def get_json_node(self):
        node = {}
        node ['token'] = self.__token_type__
        node ['value'] = self.__token_value__
        node ['occurrences'] = self.__occurrences__
        return node

    def __match_element__(token_value, matching_element, value_modifier):
        if matching_element is None or matching_element == '':
            return True

        if "'" == matching_element[0] and "'" == matching_element[-1]:
            matching_value = matching_element[1:-1]
            ignore_case = False
        else:
            matching_value = matching_element
            ignore_case = True

        if value_modifier is None or '' == value_modifier or '=' == value_modifier:
            if ignore_case:
                return token_value.lower() == matching_value.lower()
            else:
                return token_value == matching_value
        elif value_modifier == '!':
            if ignore_case:
                return token_value.lower() != matching_value.lower()
            else:
                return token_value != matching_value
        elif value_modifier == '>':
            if ignore_case:
                return token_value.lower() > matching_value.lower()
            else:
                return token_value > matching_value
        elif value_modifier == '<':
            if ignore_case:
                return token_value.lower() < matching_value.lower()
            else:
                return token_value < matching_value
        return False

    def is_token_match(self, token):
        value_match = self.__token_value__ is None \
                      or self.__token_value__ == '' \
                      or SyntaxTokenRule.__match_element__(token.token_value, self.__token_value__, self.__value_modifier__)
        type_match = self.__token_type__ is None \
                     or self.__token_type__ == '' \
                     or SyntaxTokenRule.__match_element__(token.token_type, self.__token_type__, self.__type_modifier__)
        return value_match and type_match
