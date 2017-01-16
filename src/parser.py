import json

from src.syntaxRule import SyntaxRule

class Parser():
    def __init__(self):
        self.__syntax_rules__ = {}
        self.__parsedTokens__ = []

    @property
    def syntax_rules(self):
        return self.__syntax_rules__

    @property
    def parsedTokens(self):
        return self.__parsedTokens__

    def __load_syntaxRules__(self,json_conf):
        for rule in json_conf['syntaxRules']:
            syntax_rule = SyntaxRule()
            syntax_rule.group_id = rule['name']

            syntax_rule.init_from_pattern(rule['pattern'], rule['ignore'] if 'ignore' in rule else None)
            self.__syntax_rules__[rule['name']] = syntax_rule
            print("Loaded Rule: ", rule['name'])

    def load_config(self, filename):
        json_config = json.load(open(filename))
        self.__load_syntaxRules__(json_config)

    def scan_tokens(self, tokens_list):
        pos = 0
        parsed_tokens = []
        i = -1
        while True:
            i += 1
            tokens_matched = None
            rule_matched = None
            for rule_name in self.syntax_rules:
                tokens_matched = self.syntax_rules[rule_name].match(tokens_list, pos, all_syntax_rules=self.syntax_rules)
                if (tokens_matched is not None):
                    rule_matched = rule_name
                    break;

            if (tokens_matched == None):
                parsed_tokens.append(tokens_list[pos])
                pos += 1
                print(i,':',pos,':',':Unable to find a match')
            else:
                parsed_tokens.append(tokens_matched)
                print(i,':',pos,':',':MATCH: ',rule_matched)
                #print(i,',startPos:',startPos,',len:',len(token.token_value),',found:"',token.token_type,'",value:',token.token_value)
                pos += len(tokens_matched)

            if (pos >= len(tokens_list)):
                break
