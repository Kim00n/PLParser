import re

from src.tokenTemplate import TokenTemplate


class TokenListTemplate():
    def __init__(self):
        self.list_name = ''
        self.tokens = []
        # init regex syntax elements
        self.re_syntax_el = dict(
            token_group = re.compile(r"([\(][^\)]+[\)])"),
            token_grp_name = re.compile(r"([\<][^>]+[\>])"),
            full_token = re.compile(r"([\{][^\}]+[\}](([\*\+\?])|([\[][^\]]+[\]]))?)"),
            simple_token = re.compile(r"([,]?)([!\<\>\=]?)(([a-zA-Z0-9]+)|([\'][^']+[\']))"),
            token_occ = re.compile(r"(([\*\+\?])|([\[][^\]]+[\]]))")
        )

    def set_list_name (self, list_name):
        self.list_name = list_name

    def append (self, name, value, occurrences = ''):
        token = TokenTemplate()
        token.set_token_name(name)
        token.set_token_value(value)
        token.set_occurrences(occurrences)
        self.tokens.append(token)

    def init_pattern (self, pattern, __original_str__=None, __original_pos__=None):
        self.tokens = []
        pos = 0
        while len(pattern) > pos:
            # Search for token
            token = self.re_syntax_el['full_token'].match(pattern, pos)
            if token is not None and token.group() != '':
                token_template = TokenTemplate()
                pos += 1
                # Handle first element found
                tok_element = self.re_syntax_el['simple_token'].match(pattern, pos)
                if tok_element is not None and tok_element.group() != '':
                    # save value if is is
                    token_template.set_token_value(tok_element.group(0) if tok_element.group(0)[0]!=',' else '')
                    # token type otherwise
                    token_template.set_token_type(tok_element.group(0)[1:] if tok_element.group(0)[0]==',' else '')

                    pos += len(tok_element.group(0))
                    # search for token type if not yet found
                    if token_template.__token_type__ == '':
                        tok_element = self.re_syntax_el['simple_token'].match(pattern, pos)
                        if tok_element is not None and tok_element.group() != '':
                            token_template.set_token_type(tok_element.group(0)[1:] if tok_element.group(0)[0] == ',' else '')
                            pos += len(token_template.__token_type__)+1

                # Add closing bracket
                pos += 1

                # Handle occurrences founds
                count_element = self.re_syntax_el['token_occ'].match(pattern, pos)
                if count_element is not None and count_element.group() != '':
                    token_template.set_occurrences(count_element.group(0))
                    pos += len(token_template.__occurrences__)

                #print ('token:',node)
                self.tokens.append(token_template)

            # Search for group
            tok_group = self.re_syntax_el['token_group'].match(pattern, pos)
            if (token is None and tok_group is not None and tok_group.group() != ''):
                sublist_token_template = TokenListTemplate()
                grp_pos  = 1
                # identify group name
                grp_name = self.re_syntax_el['token_grp_name'].match(tok_group.group(0), grp_pos)
                if grp_name is not None and grp_name.group() != '':
                    sublist_token_template.set_list_name(grp_name.group(0)[1:-1])
                    grp_pos += len(grp_name.group(0))

                # process pattern in the group
                sublist_token_template.init_pattern(tok_group.group(0)[grp_pos:-1],__original_str__ or pattern,__original_pos__ or (pos+grp_pos))
                pos += len(tok_group.group(0))

                self.tokens.append(sublist_token_template)

            if token is None and tok_group is None:
                print ('> Error: expected { or ( on the position')
                print ('> On: ', (__original_str__ or pattern))
                print (' '.rjust((__original_pos__ or pos)+(pos is __original_pos__ is None)+6, ' '),'^')
                break;

    def get_json_nodes(self):
        json_nodes = []