import re
from src.syntaxTokenRule import SyntaxTokenRule
from src.ruleScanner import RuleScanner


class SyntaxRules():
    def __init__(self):
        self.__all_rules__ = {}

    @property
    def all_rules(self):
        return self.__all_rules__

    @property
    def rule(self, rule_id):
        if rule_id in self.all_rules:
            return self.all_rules[rule_id]
        return None

    def pattern_rule_to_tokens (self, pattern):
        # split string pattern into string tokens. This result in a 2D matrix, each element a tuple. See ruleScanner
        all_rules = RuleScanner().str_split_syntax_rule(pattern)
        token_rule = {
            "type": 'rule',
            "def": None,
            "name": None
        }

        all_token_rules = []
        # loop through alternatives of tokens (in case of)
        for idx_alt in range(0,len(all_rules)):
            # Init the current alternative containing all tokens
            current_alt_rule = []
            # loop through list of tokens by alternative
            for tuple_token in all_rules[idx_alt]:
                # extract the tuple
                (token_rule_type, token_rule_pattern) = tuple_token
                new_token = {}

                if 'single_token' == token_rule_type:
                    # Prepare the single token
                    token_rule_el = SyntaxTokenRule()
                    token_rule_el.init_from_pattern(token_rule_pattern)
                    new_token["type"] = token_rule_type
                    new_token["def"] = token_rule_el
                    new_token["name"] = None

                elif 'group_tokens' == token_rule_type:
                    # Strip the surrounding of the group
                    token_rule_pattern = token_rule_pattern.strip(' ').lstrip('(').rstrip(')')
                    # recursive call to get a 2D matrix of the group (list of alternatives)
                    new_token = self.pattern_rule_to_tokens(token_rule_pattern)
                    # override the type to make difference between rule and group
                    new_token["type"] = token_rule_type

                elif 'rule_call' == token_rule_type:
                    rule_call = RuleScanner().str_split_rule_name(token_rule_pattern)
                    new_token["type"] = token_rule_type
                    new_token["def"] = rule_call
                    new_token["name"] = rule_call["rule_name"]

                elif 'id' == token_rule_type:
                    token_rule["name"] = token_rule_pattern

                # Add new token to the current alternative of tokens
                if "type" in new_token:
                    current_alt_rule.append(new_token)

            # Once the current alternative processed, add it to the current all_token_rules
            all_token_rules.append([])
            all_token_rules[idx_alt] = current_alt_rule

        # Once all alternatives processed, return the dict
        token_rule["def"] = all_token_rules
        return token_rule

    def add_rule_from_pattern (self, name, pattern, ignore=None, root_check=0):
        # parse pattern
        syntax_token = self.pattern_rule_to_tokens(pattern)
        # parse ignore pattern
        if ignore is not None:
            syntax_token["ignore"] = self.pattern_rule_to_tokens(ignore)["def"]

        syntax_token["root_check"] = int(root_check)

        # Add the rule to all_rules based on the name given
        self.__all_rules__[name]=syntax_token

    def rule_match(self, syntax_token, tokens, pos=0, ignore_syntax = None):
        # Handle rule_call by recursive call to the rule stored
        if 'rule_call' == syntax_token["type"]:
            rule_name = syntax_token["name"]
            return self.rule_match(self.all_rules[rule_name], tokens, pos)

        # Handle rule_match token
        elif 'single_token' == syntax_token["type"]:
            if syntax_token["def"].match_token(tokens[pos]):
                return [tokens[pos]]
            else:
                return None

        # Init the ignore token according the request
        elif 'rule' == syntax_token["type"]:
            # Special ignore syntax based on the rule def
            ignore = {
                "type":'ignore',
                "def":syntax_token["ignore"]
            }

        elif 'group_tokens' == syntax_token["type"]:
            # ignore syntax inherited
            ignore = ignore_syntax

        elif 'ignore' == syntax_token["type"]:
            # no ignore syntax to avoid recursive loop
            ignore = None

        for alt_idx in range(0, len(syntax_token["def"])):
            match = self.list_match(syntax_token["def"][alt_idx], tokens, pos, ignore)
            if match is not None:
                return match
        else:
            return None

    def list_match (self, list_rule_tokens, tokens, pos=0, ignore_syntax = None):
        src_token_idx = pos
        rule_token_occ = 0
        rule_token_idx = 0
        while True:
            syntax_token = list_rule_tokens[rule_token_idx]
            src_token = tokens[src_token_idx]

            # Check if the current token match ignore, and then skip it
            while ignore_syntax is not None and \
                    self.rule_match(ignore_syntax,[src_token]) is not None and \
                    src_token_idx < len(tokens)-1:
                src_token_idx += 1
                src_token = tokens[src_token_idx]

            if syntax_token["type"] in ('single_token', 'rule_call', 'group_tokens'):
                if 'single_token' == syntax_token["type"]:
                    token_min_occ = syntax_token["def"].min_occurrences
                    token_max_occ = syntax_token["def"].max_occurrences
                elif 'rule_call' == syntax_token["type"]:
                    token_min_occ = int(syntax_token["def"]["min_occ"])
                    token_max_occ = int(syntax_token["def"]["max_occ"])
                elif 'group_tokens' == syntax_token["type"]:
                    token_min_occ = 1
                    token_max_occ = 1
                result_matching = self.rule_match(syntax_token, tokens, src_token_idx, ignore_syntax)

                if result_matching is not None:
                    src_token_idx += len(result_matching)
                    rule_token_occ += 1
                    if token_max_occ != 0 and rule_token_occ >= token_max_occ:
                        rule_token_idx += 1
                        rule_token_occ = 0
                else:
                    if rule_token_occ < token_min_occ:
                        return None
                    elif rule_token_occ >= token_min_occ:
                        rule_token_idx += 1
                        rule_token_occ = 0

            else:
                print ("error on token ", syntax_token["type"])
                break;


            if rule_token_idx >= len(list_rule_tokens):
                return tokens[pos:src_token_idx]

            if src_token_idx > len(tokens):
                return None


    def match(self, tokens, pos=0):
        for rule_name in self.all_rules:
            if self.all_rules[rule_name]["root_check"] == 1:
                rule_match = self.rule_match(self.all_rules[rule_name], tokens, pos)
                if rule_match is not None:
                    return (rule_name, rule_match)
        return (None, None)

            #print ("tpl_index: ",tpl_index)
            #print ("tpl_match_occ: ",tpl_match_occ)
            #print ("tok_tpl.get_json_node: ",tok_tpl.get_json_node())
            #print ("min_occurrences: ",tok_tpl.min_occurrences)
            #print ("max_occurrences: ",tok_tpl.max_occurrences)
            #print ("token.get_json_node: ",token.get_json_node())

            #break
















