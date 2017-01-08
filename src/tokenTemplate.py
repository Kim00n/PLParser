import re


class TokenTemplate():
    def __init__(self):
        self.__token_type__ = ''
        self.__type_modifier__ = ''
        self.__token_value__ = ''
        self.__value_modifier__ = ''
        self.__occurrences__ = ''
        self.__min_occurrences__ = ''
        self.__max_occurrences__ = ''
        self.E_pattern_issue = Exception()

    def set_token_type (self, token_type):
        self.__token_type__ = token_type

    def set_token_value (self, token_value):
        self.__token_value__ = token_value

    def set_occurrences (self, token_occurrences):
        self.__occurrences__ = token_occurrences
        if token_occurrences == '*':
            self.__min_occurrences__ = 0
            self.__max_occurrences__ = ''
        elif token_occurrences == '+':
            self.__min_occurrences__ = 1
            self.__max_occurrences__ = ''
        elif token_occurrences == '?':
            self.__min_occurrences__ = 0
            self.__max_occurrences__ = 1
        elif token_occurrences[0] == '[' and token_occurrences[-1] == ']':
            self.__min_occurrences__ = re.match('[0-9]*', token_occurrences[1:])
            if token_occurrences[1+len(self.__min_occurrences__)] == ',':
                self.__max_occurrences__ = re.match('[0-9]*', token_occurrences[2+len(self.__min_occurrences__):])
        else:
            raise self.E_pattern_issue(token_occurrences)

    def get_node(self):
        node = {}
        node ['token'] = self.__token_name__
        node ['value'] = self.__token_name__
        node ['occurrences'] = self.__token_name__