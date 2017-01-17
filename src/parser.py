import json

from src.syntaxRules import SyntaxRules

class Parser():
    def __init__(self):
        self.__syntax_rules__ = SyntaxRules()
        self.__parsed_tokens__ = []

    @property
    def syntax_rules(self):
        return self.__syntax_rules__

    @property
    def parsed_tokens(self):
        return self.__parsed_tokens__

    def __load_syntax_rules__(self,json_conf):
        for rule in json_conf['syntaxRules']:
            self.__syntax_rules__.add_rule_from_pattern(rule['name'], rule['pattern'], rule['ignore'] if 'ignore' in rule else None, rule['root_check'])
            print("Loaded Rule: ", rule['name'])

    def load_config(self, filename):
        json_config = json.load(open(filename))
        self.__load_syntax_rules__(json_config)

    def scan_tokens(self, tokens_list):
        pos = 0
        parsed_tokens = []
        i = -1
        while True:
            i += 1
            (rule_name, tokens_matched) = self.syntax_rules.match(tokens_list, pos)

            if (tokens_matched == None):
                parsed_tokens.append(tokens_list[pos])
                pos += 1
                print(i,':',pos,':',':Unable to find a match')
            else:
                parsed_tokens.append(tokens_matched)
                print(i,':',pos,':',':MATCH: ',rule_name)
                #print(i,',startPos:',startPos,',len:',len(token.token_value),',found:"',token.token_type,'",value:',token.token_value)
                pos += len(tokens_matched)

            if (pos >= len(tokens_list)):
                break
