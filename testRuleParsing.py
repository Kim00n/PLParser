import re

from src.tokenListTemplate import TokenListTemplate


class syntaxtoken_rules():
    def __init__(self):
        self.sub_rule = {}
        self.sub_rule['group'] = re.compile(r"([\(][^\)]+[\)])")
        self.sub_rule['grp_name'] = re.compile(r"([\<][^>]+[\>])")
        self.sub_rule['token'] = re.compile(r"([\{][^\}]+[\}](([\*\+\?])|([\[][^\]]+[\]]))?)")
        self.sub_rule['tok_element'] = re.compile(r"([,]?)([!\<\>\=]?)(([a-zA-Z0-9]+)|([\'][^']+[\']))")
        self.sub_rule['count'] = re.compile(r"(([\*\+\?])|([\[][^\]]+[\]]))")

    def get_nodes(self, token_string, __original_str__=None, __original_pos__=None):
        node_list = []
        pos = 0
        while len(token_string) > pos:
            # Search for token
            token = self.sub_rule['token'].match(token_string, pos)
            if token is not None and token.group() != '':
                node = {}
                pos += 1
                # Handle first element found
                tok_element = self.sub_rule['tok_element'].match(token_string, pos)
                if tok_element is not None and tok_element.group() != '':
                    # save value if is is
                    node['value']=tok_element.group(0) if tok_element.group(0)[0]!=',' else ''
                    # token type otherwise
                    node['token']=tok_element.group(0)[1:] if tok_element.group(0)[0]==',' else ''
                    pos += len(tok_element.group(0))
                    # search for token type if not yet found
                    if node['token'] == '':
                        tok_element = self.sub_rule['tok_element'].match(token_string, pos)
                        if tok_element is not None and tok_element.group() != '':
                            node['token'] = tok_element.group(0)[1:] if tok_element.group(0)[0] == ',' else ''
                            pos += len(node['token'])+1

                # Add closing bracket
                pos += 1

                # Handle occurences founds
                count_element = self.sub_rule['count'].match(token_string, pos)
                if count_element is not None and count_element.group() != '':
                    node['occurrences']=count_element.group(0)
                    pos += len(node['occurrences'])

                #print ('token:',node)
                node_list.append(node)

            # Search for group
            tok_group = self.sub_rule['group'].match(token_string, pos)
            if (token is None and tok_group is not None and tok_group.group() != ''):
                group_node = {}
                grp_pos  = 1
                grp_name = self.sub_rule['grp_name'].match(tok_group.group(0), grp_pos)
                if grp_name is not None and grp_name.group() != '':
                    group_node['grp_name'] = grp_name.group(0)[1:-1]
                    grp_pos += len(grp_name.group(0))
                else:
                    group_node['grp_name'] = ''
                group_node['grp_tokens'] = self.get_nodes(tok_group.group(0)[grp_pos:-1],__original_str__ or token_string,__original_pos__ or (pos+grp_pos))
                pos += len(tok_group.group(0))

                #print ('group:',group_node)
                node_list.append(group_node)

            if token is None and tok_group is None:
                print ('> Error: expected { or ( on the position')
                print ('> On: ', (__original_str__ or token_string))
                print (' '.rjust((__original_pos__ or pos)+(pos is __original_pos__ is None)+6, ' '),'^')
                break;

        return (node_list)

def process_rule(list_tokens, ignore=None):
    process = token_rules()
    el = process.get_nodes(list_tokens)
    print (el)

#process_rule("{create}{or}{replace}{body}(<package_name>{,word}){is}",ignore="{blk}")
#process_rule("{type,word}*{a}(<type_name>{,word}*){is}[1,3](<type_definition>{!';'}*){';'}",ignore="{blk}")
tokens = TokenListTemplate()
tokens.init_pattern("{type,word}*{a}(<type_name>{,word}*){is}[1,3](<type_definition>{!';'}*){';'}")
print (tokens.get_json_nodes())


