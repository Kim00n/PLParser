import re

from src.tokenTemplate import TokenTemplate


class TokenListTemplate():
    def __init__(self):
        self.__list_name__ = ''
        self.__token_templates__ = []
        self.__ignore__ = None
        # init regex syntax elements
        self.re_syntax_el = dict(
            token_group = re.compile(r"([\(][^\)]+[\)])"),
            token_grp_name = re.compile(r"([\<][^>]+[\>])"),
            full_token = re.compile(r"([\{][^\}]+[\}](([\*\+\?])|([\[][^\]]+[\]]))?)"),
            simple_token = re.compile(r"([,]?)([!\<\>\=]?)(([a-zA-Z0-9]+)|([\'][^']+[\']))"),
            token_occ = re.compile(r"(([\*\+\?])|([\[][^\]]+[\]]))")
        )

    @property
    def list_name(self):
        return self.__list_name__

    @list_name.setter
    def list_name(self, list_name):
        self.__list_name__ = list_name

    @property
    def token_templates(self):
        return self.__token_templates__

    def append (self, name, value, occurrences = ''):
        token = TokenTemplate()
        token.token_name = name
        token.token_value = value
        token.token_occurrences = occurrences
        self.__token_templates__.append(token)

    def __parse_pattern__(self, pattern, __original_str__=None , __original_pos__=None):
        token_tpl_list = []
        pos = 0

        while len(pattern) > pos:
            # Search for token
            token = self.re_syntax_el['full_token'].match(pattern, pos)
            if token is not None and token.group() != '':
                new_token_tpl = TokenTemplate.init_from_pattern(token.group(0))
                pos += len(token.group(0))
                if new_token_tpl is None:
                    print ("issue processing the template ",token.group(0),". EXIT")
                    break

                #print ('token:',node)
                token_tpl_list.append(new_token_tpl)

            # Search for group
            tok_group = self.re_syntax_el['token_group'].match(pattern, pos)
            if (token is None and tok_group is not None and tok_group.group() != ''):
                new_token_tpl_list = TokenListTemplate()
                # Inherit the ignore
                new_token_tpl_list.__ignore__ = self.__ignore__

                grp_pos  = 1

                # identify group name and set it
                grp_name = self.re_syntax_el['token_grp_name'].match(tok_group.group(0), grp_pos)
                if grp_name is not None and grp_name.group() != '':
                    new_token_tpl_list.list_name = grp_name.group(0)[1:-1]
                    grp_pos += len(grp_name.group(0))

                # process pattern in the group
                new_token_tpl_list.__parse_pattern__(
                    tok_group.group(0)[grp_pos:-1], __original_str__ or pattern,__original_pos__ or (pos+grp_pos))
                pos += len(tok_group.group(0))

                token_tpl_list.append(new_token_tpl_list)

            if token is None and tok_group is None:
                print ('> Error: expected { or ( on the position')
                print ('> On: ', (__original_str__ or pattern))
                print (' '.rjust((__original_pos__ or pos)+(pos is __original_pos__ is None)+6, ' '),'^')
                break

        self.__token_templates__ = token_tpl_list
        return token_tpl_list


    def init_pattern (self, pattern, ignore=None):
        if ignore is not None:
            self.__ignore__ = TokenTemplate.init_from_pattern(ignore)

        self.__token_templates__ = self.__parse_pattern__(pattern)

    def get_json_nodes(self):
        json_node = {}
        json_node['group_name'] = self.__list_name__
        json_node['group_tokens'] = []
        for token in self.token_templates:
            if type(token) is TokenTemplate:
                json_node['group_tokens'].append(token.get_json_node())
            elif type(token) is TokenListTemplate:
                json_node['group_tokens'].append(token.get_json_nodes())
        return json_node

    def match(self, tokens, start_pos=0):
        token_index = start_pos
        tpl_match_occ = 0
        tpl_index = 0
        while True:
            tok_tpl = self.token_templates[tpl_index]
            token = tokens[token_index]
            # Skip the ignored token
            while self.__ignore__ is not None and \
                    isinstance(tok_tpl,TokenTemplate) and \
                    self.__ignore__.is_token_match(token) and \
                    token_index < len(tokens):
                print("ignored token ", token_index)
                token_index += 1
                token = tokens[token_index]

            if isinstance(tok_tpl,TokenTemplate):
                print ("--tok_tpl ",tpl_index," is a token template")

                if tok_tpl.is_token_match(token):
                    token_index += 1
                    tpl_match_occ += 1
                    print(">token ", token_index, " MATCH token tpl ", tpl_index, ", occurrence(s): ", tpl_match_occ)
                    if tok_tpl.max_occurrences != 0 and tpl_match_occ >= tok_tpl.max_occurrences:
                        print("--MAX occurrences reached: ",
                              tpl_match_occ, " out of ", tok_tpl.max_occurrences, ". Go next token tpl.")
                        tpl_index += 1
                        tpl_match_occ = 0
                else:
                    if tpl_match_occ < tok_tpl.min_occurrences:
                        print(">token ", token_index, " NOT match token tpl ", tpl_index,", MIN occurrences not reached: ", tpl_match_occ," out of ",tok_tpl.min_occurrences,". EXIT")
                        print (token.get_json_node())
                        return None
                    elif tpl_match_occ >= tok_tpl.min_occurrences:
                        print(">token ", token_index, " NOT match token tpl ", tpl_index,", MIN occurrences reached: ", tpl_match_occ," out of ",tok_tpl.min_occurrences,". Next Tpl")
                        tpl_index += 1
                        tpl_match_occ = 0

            if isinstance(tok_tpl,TokenListTemplate):
                print ("--tok_tpl is a token list template")
                list_match = tok_tpl.match(tokens,token_index)
                if list_match is None:
                    print(">List token from ", token_index, " NOT MATCH token tpl LIST. Exit")
                    return None
                else:
                    print(">List token from ", token_index, " for ",len(list_match)," tokens MATCH token tpl LIST. Next Tpl")
                    token_index += len(list_match)
                    tpl_match_occ += 0
                    tpl_index += 1
                    for i in list_match:
                        print(i.get_json_node())

            if tpl_index >= len(self.token_templates):
                print ("FULL MATCH")
                return tokens[start_pos:token_index]

            if  token_index > len(tokens):
                print ("--Out of index, no match")
                return None


            #print ("tpl_index: ",tpl_index)
            #print ("tpl_match_occ: ",tpl_match_occ)
            #print ("tok_tpl.get_json_node: ",tok_tpl.get_json_node())
            #print ("min_occurrences: ",tok_tpl.min_occurrences)
            #print ("max_occurrences: ",tok_tpl.max_occurrences)
            #print ("token.get_json_node: ",token.get_json_node())

            #break
















