import re
from src.token import Token
from src.ruleScanner import RuleScanner


class SyntaxTokenRule():
    def __init__(self):
        self.__token_type__ = ''
        self.__type_modifier__ = ''
        self.__token_value__ = ''
        self.__value_modifier__ = ''
        self.__occurrences__ = ''
        self.__min_occurrences__ = ''
        self.__max_occurrences__ = ''

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

    def init_from_pattern(self, pattern):
        pattern_elements = RuleScanner().str_split_token_rule(pattern)
        self.__value_modifier__ = pattern_elements["value_compare"]
        self.__token_value__ = pattern_elements["value"]
        self.__type_modifier__ = pattern_elements["type_compare"]
        self.__token_type__ = pattern_elements["type"]
        self.__min_occurrences__ = pattern_elements["min_occ"]
        self.__max_occurrences__ = pattern_elements["max_occ"]

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
        elif '!' == value_modifier:
            if ignore_case:
                return token_value.lower() != matching_value.lower()
            else:
                return token_value != matching_value

        return False

    def match_token(self, token):
        if not isinstance(token,Token):
            return False

        value_match = self.__token_value__ is None \
                      or '' == self.__token_value__ \
                      or SyntaxTokenRule.__match_element__(token.token_value, self.__token_value__, self.__value_modifier__)
        type_match = self.__token_type__ is None \
                     or '' == self.__token_type__ \
                     or SyntaxTokenRule.__match_element__(token.token_type, self.__token_type__, self.__type_modifier__)
        return value_match and type_match
