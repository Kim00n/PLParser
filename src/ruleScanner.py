import re

class RuleScanner():
    def __init__(self, version = None):
        self.__version__ = version
        # init regex syntax elements
        if version=='{}':
            self.re_syntax = dict(
                def_group = re.compile(r"([\(][^\)]+[\)])"),
                def_rule_name = re.compile(r"([\<][^>]+[\>])"),
                def_token = re.compile(r"([\{][^\}]+[\}](([\*\+\?])|([\[][^\]]+[\]]))?)"),
                def_token_part = re.compile(r"([,]?)([!\<\>\=]?)(([a-zA-Z0-9]+)|([\'][^']+[\']))"),
                def_occ = re.compile(r"(([\*\+\?])|([\[][^\]]+[\]]))")
            )
            self.__token_split_char__ = ','
            self.__token_separator__ = '{'
            self.__group_or_separator__ = '|'

        else:
            self.re_syntax = dict(
                def_group = re.compile(r"([ ]*)([\(][^\)]+[\)])([ ]*)"),
                def_group_id = re.compile(r"(\@[a-zA-Z0-9_]+)([ ]*)"),
                def_rule_name = re.compile(r"([\<][^>]+[\>])(([\*\+\?])|([\[][^\]]+[\]]))?([ ]*)"),
                def_token = re.compile(r"([ ]*)(?:[\.]?([\!]?)(([a-zA-Z0-9_]+)|([\'][^']+[\'])))(\1?)(([\*\+\?])|([\[][^\]]+[\]]))?([ ]*)"),
                def_part_token = re.compile(r"([.]?)([\!]?)(([a-zA-Z0-9_]+)|([\'][^']+[\']))"),
                def_part_occ = re.compile(r"(([\*\+\?])|([\[][^\]]+[\]]))")
            )
            self.__token_split_char__ = '.'
            self.__token_separator__ = ''
            self.__alternative_split_char__ = '|'

    @property
    def version(self):
        return self.__version__

    @property
    def token_split_char(self):
        return self.__token_split_char__

    @property
    def token_separator(self):
        return self.__token_separator__

    @property
    def alternative_split_char(self):
        return self.__alternative_split_char__

    def match_grp(self, pattern, pos, strip = ' '):
        el = self.re_syntax['def_group'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        if strip == None:
            return el.group(0)
        return el.group(0).strip(strip)

    def match_grp_id(self, pattern, pos, strip = ' '):
        el = self.re_syntax['def_group_id'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        if strip == None:
            return el.group(0)
        return el.group(0).strip(strip)

    def match_rule_name(self, pattern, pos, strip = ' '):
        el = self.re_syntax['def_rule_name'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        return el.group(0).strip(' ')

    def match_token(self, pattern, pos, strip = ' '):
        el = self.re_syntax['def_token'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        if strip == None:
            return el.group(0)
        return el.group(0).strip(strip)

    def match_part_token(self, pattern, pos):
        el = self.re_syntax['def_part_token'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        return el.group(0).strip(' ')

    def match_part_occ(self, pattern, pos):
        el = self.re_syntax['def_part_occ'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        return el.group(0).strip(' ')

    def split_pattern_rules(self, pattern):
        all_alternatives_token_rules = []
        index_alternative = 0
        list_of_token_rules = []
        pos = 0

        while len(pattern) > pos:
            print (pos,':',len(pattern))
            # Search for token
            token_el = self.match_token(pattern, pos, strip=None)
            if token_el is not None:
                pos += len(token_el)
                list_of_token_rules.append(('token',token_el))
                continue

            # Search for group
            token_el = self.match_grp(pattern, pos, strip=None)
            if (token_el is not None):
                pos += len(token_el)
                list_of_token_rules.append(('group',token_el))
                continue

            # Search for group identifier
            token_el = self.match_grp_id(pattern, pos, strip=None)
            if (token_el is not None):
                pos += len(token_el)
                list_of_token_rules.append(('group_id',token_el))
                continue

            token_el = self.match_rule_name(pattern, pos, strip=None)
            if (token_el is not None):
                pos += len(token_el)
                list_of_token_rules.append(('rule_name',token_el))
                continue

            token_el = pattern[pos]
            if (token_el == self.alternative_split_char):
                pos += len(token_el)
                all_alternatives_token_rules.append([])
                all_alternatives_token_rules[index_alternative] = list_of_token_rules
                list_of_token_rules = []
                index_alternative += 1
                continue
            else:
                token_el = None

            if token_el is None:
                print ('> Error: expected { or ( on the position')
                print ('> On: ', pattern)
                print (' '.rjust(pos + 6, ' '),'^')
                break

        all_alternatives_token_rules.append([])
        all_alternatives_token_rules[index_alternative] = list_of_token_rules

        return all_alternatives_token_rules

    def split_token_rules(self, pattern):
        pos = 0
        strip_pattern = pattern.strip(' ')
        token_el = ['','','','','1', '1']
        token_right = None

        #init token left part
        token_left = self.match_part_token(strip_pattern, pos)
        if (token_left is not None):
            # process left part
            pos += len(token_left)
            # 0 = left modifier
            if token_left[0] == '!':
                token_el[0] = token_left[0]
                token_left = token_left[1:]

            # 1 = left value
            if token_left[0] != '.':
                token_el[1] = token_left
            else:
                # start by . mean right part
                token_right = token_left
                pos -= len(token_right)   # pos will be recounted when processing right part (avoid double count)

        # if right part not found, init right part
        if token_right is None:
            token_right = self.match_part_token(strip_pattern, pos)

        if (token_right is not None):
            #process right part
            pos += len(token_right)
            # remove separator if needed
            if token_right[0] == '.':
                token_right = token_right[1:]

            # 2 = right modifier
            if token_right[0] == '!':
                token_el[2] = token_right[0]
                token_right = token_right[1:]

            # 3 = right value
            token_el[3] = token_right

        token_occ = self.match_part_occ(strip_pattern, pos)
        if token_occ is None:
            token_occ = '[1]'
        if token_occ == '*':
            token_el[4] = 0
            token_el[5] = -1     # mean not defined
        elif token_occ == '+':
            token_el[4] = 1
            token_el[5] = -1     # mean not defined
        elif token_occ == '?':
            token_el[4] = 0
            token_el[5] = 1
        elif token_occ[0] == '[' and token_occ[-1] == ']':
            token_el[4:] = token_occ[1:-1].split(',')
            if 5 not in token_el:
                token_el.append(token_el[4])

        return token_el
