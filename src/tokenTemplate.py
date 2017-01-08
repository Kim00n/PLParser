import re
from src.tokenizer import Token


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

    def init_from_pattern (pattern):
        full_token = re.compile(r"([\{][^\}]+[\}](([\*\+\?])|([\[][^\]]+[\]]))?)")
        simple_token = re.compile(r"([,]?)([!\<\>\=]?)(([a-zA-Z0-9]+)|([\'][^']+[\']))")
        token_occ = re.compile(r"(([\*\+\?])|([\[][^\]]+[\]]))")
        token_template = None
        pos = 0
        token = full_token.match(pattern,pos)
        if token is not None and token.group() != '':
            token_template = TokenTemplate()
            pos += 1
            # Handle first element found
            token_content = simple_token.match(pattern, pos)
            if token_content is not None and token_content.group() != '':
                # save value if is is
                token_template.set_token_value(token_content.group(0) if token_content.group(0)[0] != ',' else '')
                # token type otherwise
                token_template.set_token_type(token_content.group(0)[1:] if token_content.group(0)[0] == ',' else '')

                pos += len(token_content.group(0))
                # search for token type if not yet found
                if token_template.__token_type__ == '':
                    token_content = simple_token.match(pattern, pos)
                    if token_content is not None and token_content.group() != '':
                        token_template.set_token_type(
                            token_content.group(0)[1:] if token_content.group(0)[0] == ',' else '')
                        pos += len(token_template.__token_type__) + 1

            # Add closing bracket
            pos += 1

            # Handle occurrences founds
            occ_element = token_occ.match(pattern, pos)
            if occ_element is not None and occ_element.group() != '':
                token_template.set_occurrences(occ_element.group(0))
                pos += len(token_template.__occurrences__)

        return token_template

    def set_token_type (self, token_type):
        if len(token_type) > 0 and token_type[0] in ('>','<','!','='):
            self.__type_modifier__ = token_type[0]
            self.__token_type__ = token_type[1:].strip(' ')
        else:
            self.__token_type__ = token_type.strip(' ')

    def set_token_value (self, token_value):
        if len(token_value) > 0 and token_value[0] in ('>','<','!','='):
            self.__value_modifier__ = token_value[0]
            self.__token_value__ = token_value[1:].strip(' ')
        else:
            self.__token_value__ = token_value.strip(' ')


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
            self.__min_occurrences__ = re.match('[0-9]*', token_occurrences[1:]).group(0) or ''
            if token_occurrences[1+len(self.__min_occurrences__)] == ',':
                self.__max_occurrences__ = re.match('[0-9]*', token_occurrences[2+len(self.__min_occurrences__):])
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
        print (ignore_case.numerator)

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


    def token_match(self, token):
        value_match = self.__token_value__ is None \
                      or self.__token_value__ == '' \
                      or TokenTemplate.__match_element__(token.token_value, self.__token_value__, self.__value_modifier__)
        type_match = self.__token_type__ is None \
                     or self.__token_type__ == '' \
                     or TokenTemplate.__match_element__(token.token_type, self.__token_type__, self.__type_modifier__)
        return value_match and type_match
