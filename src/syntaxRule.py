import re
from src.syntaxTokenRule import SyntaxTokenRule
from src.ruleScanner import RuleScanner


class SyntaxRule():
    def __init__(self):
        self.__group_id__ = ''
        self.__all_tokens__ = None
        self.__ignore_tokens__ = None
        self.__ignore_string__ = None

    @property
    def group_id(self):
        return self.__group_id__

    @group_id.setter
    def group_id(self, group_id):
        self.__group_id__ = group_id

    @property
    def ignore_tokens(self):
        return self.__ignore_tokens__

    @property
    def all_tokens(self):
        return self.__all_tokens__

    def init_token_rule (self, pattern):
        token_rule = SyntaxTokenRule()
        token_rule.init_from_pattern(pattern)

        return token_rule

    def str_pattern_to_array (self, pattern):
        all_rules = RuleScanner().str_split_syntax_rule(pattern)

        all_token_rules = []
        current_alt_rule = []
        for idx_alt in range(0,len(all_rules)):
            for tuple_token in all_rules[idx_alt]:
                (token_rule_type,token_rule_pattern) = tuple_token

                if token_rule_type == 'token':
                    token_rule = SyntaxTokenRule()
                    token_rule.init_from_pattern(token_rule_pattern)
                    current_alt_rule.append((token_rule_type,token_rule))
                elif token_rule_type == 'group':
                    token_rule_pattern = token_rule_pattern.strip(' ').lstrip('(').rstrip(')')
                    token_grp = SyntaxRule()
                    token_grp.init_from_pattern(token_rule_pattern)
                    token_grp.__ignore_tokens__ = self.__ignore_tokens__
                    current_alt_rule.append((token_rule_type,token_grp))
                elif token_rule_type == 'group_id':
                    self.group_id = token_rule_pattern
                elif token_rule_type == 'rule':
                    rule_name = token_rule_pattern
                    current_alt_rule.append((token_rule_type,rule_name))

            all_token_rules.append([])
            all_token_rules[idx_alt] = current_alt_rule

        return all_token_rules


    def init_from_pattern (self, pattern, ignore=None):
        if ignore is not None:
            self.__ignore_tokens__ = self.str_pattern_to_array(ignore)[0]

        self.__all_tokens__ = self.str_pattern_to_array(pattern)

    def __all_tokens_match__(self, rule_tokens, source_tokens, start_pos=0, ignore_tokens = None, all_syntax_rules = None):
        src_token_idx = start_pos
        rule_token_occ = 0
        rule_token_idx = 0
        while True:
            (token_type, tok_tpl) = rule_tokens[rule_token_idx]

            src_token = source_tokens[src_token_idx]


            # Skip the ignored token
            if ignore_tokens is not None and \
                    isinstance(tok_tpl, SyntaxTokenRule) and \
                    self.__all_tokens_match__(ignore_tokens, [src_token] ) is not None and \
                    src_token_idx < len(source_tokens):
                src_token_idx += 1

            if 'token' == token_type and isinstance(tok_tpl,SyntaxTokenRule):
                if tok_tpl.match_token(src_token):
                    src_token_idx += 1
                    rule_token_occ += 1
                    if tok_tpl.max_occurrences != 0 and rule_token_occ >= tok_tpl.max_occurrences:
                        rule_token_idx += 1
                        rule_token_occ = 0
                else:
                    if rule_token_occ < tok_tpl.min_occurrences:
                        return None
                    elif rule_token_occ >= tok_tpl.min_occurrences:
                        rule_token_idx += 1
                        rule_token_occ = 0
            elif 'rule' == token_type:
                if tok_tpl["rule"] in all_syntax_rules:
                    result_matching = all_syntax_rules[tok_tpl["rule"]].match(source_tokens, src_token_idx, all_syntax_rules)
                    if result_matching is not None:
                        src_token_idx += len(result_matching)
                        rule_token_occ += 1
                        if tok_tpl["max_occ"]  != 0 and rule_token_occ >= tok_tpl["max_occ"]:
                            src_token_idx += len(result_matching)
                            rule_token_occ = 0
                    else:
                        if rule_token_occ < tok_tpl["min_occ"]:
                            return None
                        elif rule_token_occ >= tok_tpl["min_occ"]:
                            rule_token_idx += 1
                            rule_token_occ = 0

            elif 'group' == token_type and isinstance(tok_tpl, SyntaxRule):
                result_matching = tok_tpl.match(source_tokens,src_token_idx, all_syntax_rules)
                if result_matching is not None:
                    src_token_idx += len(result_matching)
                    rule_token_occ += 0
                    rule_token_idx += 1
                else:
                    return None
            else:
                print ("error on token ",src_token)


            if rule_token_idx >= len(rule_tokens):
                return source_tokens[start_pos:src_token_idx]

            if src_token_idx > len(source_tokens):
                return None



    def match(self, tokens, start_pos=0, all_syntax_rules = None):
        for i in range(0, len(self.all_tokens)):
            alt_match = self.__all_tokens_match__(self.all_tokens[i],tokens, start_pos,self.ignore_tokens, all_syntax_rules)
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
















