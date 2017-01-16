import re
from src.syntaxTokenRule import SyntaxTokenRule
from src.ruleScanner import RuleScanner


class SyntaxGroupRule():
    def __init__(self):
        self.__group_id__ = ''
        self.__token_templates__ = []
        self.__token_templates__.append([])
        self.__ignore__ = None

    @property
    def group_id(self):
        return self.__group_id__

    @group_id.setter
    def group_id(self, group_id):
        self.__group_id__ = group_id

    @property
    def list_of_tokens_rule(self):
        return self.__token_templates__

    def init_token_rule (self, pattern):
        token_rule = SyntaxTokenRule()
        token_rule.init_from_pattern(pattern)

        return token_rule

    def init_from_pattern(self, pattern):
        all_rules = RuleScanner().split_pattern_rules(pattern)

        all_token_rules = []
        current_alt_rule = []
        for idx_alt in all_rules:
            for idx_token in all_rules[idx_alt]:
                token_rule_type = all_rules[idx_alt][idx_token][0]
                token_rule_pattern = all_rules[idx_alt][idx_token][1]

                if token_rule_type == 'token':
                    token_rule = SyntaxTokenRule()
                    token_rule.init_from_pattern(token_rule_pattern)
                    current_alt_rule.append(token_rule)
                elif token_rule_type == 'group':
                    token_grp = SyntaxGroupRule()
                    token_grp.init_from_pattern(token_rule_pattern)
                    current_alt_rule.append(token_grp)
                elif token_rule_type == 'group_id':
                    self.group_id = token_rule_pattern
                elif token_rule_type == 'rule_name':
                    self.group_id = token_rule_pattern

            all_alternatives_token_rules.append([])
            all_alternatives_token_rules[index_alternative] = list_of_token_rules

    def __parse_pattern__(self, pattern, __original_str__=None , __original_pos__=None):
        all_alternatives_token_rules = []
        index_alternative = 0
        list_of_token_rules = []
        pos = 0

        while len(pattern) > pos:
            # Search for token
            token = self.ruleScanner.match_token(pattern, pos, strip=None)
            if token is not None:
                single_token_rule = self.init_token_rule(token)
                pos += len(token)
                if single_token_rule is None:
                    break

                #print ('token:',node)
                list_of_token_rules.append(single_token_rule)

            # Search for group
            tok_group = self.ruleScanner.match_grp(pattern, pos, strip=None)
            if (token is None and tok_group is not None):
                group_of_tokens_rule = SyntaxGroupRule()
                grp_pos = 1

                # identify group name and set it
                grp_name = self.ruleScanner.match_cat_name(tok_group, grp_pos)
                if grp_name is not None:
                    group_of_tokens_rule.list_name = grp_name[1:-1]
                    grp_pos += len(grp_name)

                # Inherit the ignore
                group_of_tokens_rule.__ignore__ = self.__ignore__
                # process pattern in the group. We call here this function to ensure the error properly displayed(inheritance of previous string)
                group_of_tokens_rule.__parse_pattern__(
                    tok_group.strip(' ')[grp_pos:-1], __original_str__ or pattern,__original_pos__ or (pos+grp_pos))
                pos += len(tok_group)

                list_of_token_rules.append(group_of_tokens_rule)

            if pos<len(pattern):
                token_char = pattern[pos]
                if self.ruleScanner.group_or_separator == token_char:
                    all_alternatives_token_rules.append([])
                    all_alternatives_token_rules[index_alternative] = list_of_token_rules
                    list_of_token_rules = []
                    index_alternative += 1

                    pos += 1
                elif ' ' == token_char:
                    pos += 1
                else:
                    token_char = None
            else:
                token_char = None

            if token is None and tok_group is None and token_char is None:
                print ('> Error: expected { or ( on the position')
                print ('> On: ', (__original_str__ or pattern))
                print (' '.rjust((__original_pos__ or pos)+(pos is __original_pos__ is None)+6, ' '),'^')
                break

        all_alternatives_token_rules.append([])
        all_alternatives_token_rules[index_alternative] = list_of_token_rules

        self.__token_templates__ = all_alternatives_token_rules
        return all_alternatives_token_rules


    def init_pattern (self, pattern, ignore=None):
        if ignore is not None:
            self.__ignore__ = self.init_SingleTokenRule(ignore)

        self.__token_templates__ = self.__parse_pattern__(pattern)

    def get_json_nodes(self):
        json_node = {}
        json_node['group_name'] = self.__list_name__
        json_node['group_tokens'] = []
        for token in self.list_of_tokens_rule:
            if isinstance(token, SingleTokenRule):
                json_node['group_tokens'].append(token.get_json_node())
            elif isinstance(token, SyntaxGroupRule):
                json_node['group_tokens'].append(token.get_json_nodes())
        return json_node

    def __match_alternative__(self, alternative, tokens, start_pos=0):
        token_index = start_pos
        tpl_match_occ = 0
        tpl_index = 0
        while True:
            tok_tpl = self.list_of_tokens_rule[alternative][tpl_index]
            token = tokens[token_index]
            # Skip the ignored token
            while self.__ignore__ is not None and \
                    isinstance(tok_tpl,SyntaxTokenRule) and \
                    self.__ignore__.is_token_match(token) and \
                    token_index < len(tokens):
                token_index += 1
                token = tokens[token_index]

            if isinstance(tok_tpl,SyntaxTokenRule):
                if tok_tpl.is_token_match(token):
                    token_index += 1
                    tpl_match_occ += 1
                    if tok_tpl.max_occurrences != 0 and tpl_match_occ >= tok_tpl.max_occurrences:
                        tpl_index += 1
                        tpl_match_occ = 0
                else:
                    if tpl_match_occ < tok_tpl.min_occurrences:
                        return None
                    elif tpl_match_occ >= tok_tpl.min_occurrences:
                        tpl_index += 1
                        tpl_match_occ = 0

            if isinstance(tok_tpl, SyntaxGroupRule):
                list_match = tok_tpl.match(tokens,token_index)
                if list_match is None:
                    return None
                else:
                    token_index += len(list_match)
                    tpl_match_occ += 0
                    tpl_index += 1

            if tpl_index >= len(self.list_of_tokens_rule[alternative]):
                return tokens[start_pos:token_index]

            if  token_index > len(tokens):
                return None

    def match(self, tokens, start_pos=0):
        for i in range(0, len(self.list_of_tokens_rule)):
            alt_match = self.__match_alternative__(i,tokens, start_pos)
            if alt_match is not None:
                return alt_match
        return None

            #print ("tpl_index: ",tpl_index)
            #print ("tpl_match_occ: ",tpl_match_occ)
            #print ("tok_tpl.get_json_node: ",tok_tpl.get_json_node())
            #print ("min_occurrences: ",tok_tpl.min_occurrences)
            #print ("max_occurrences: ",tok_tpl.max_occurrences)
            #print ("token.get_json_node: ",token.get_json_node())

            #break
















