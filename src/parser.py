import json

from src.syntaxGroupRule import SyntaxGroupRule


class Parser():
    def __init__(self):
        self.__syntaxRules__ = []
        self.__parsedTokens__ = []

    @property
    def syntaxRules(self):
        return self.__syntaxRules__

    @property
    def parsedTokens(self):
        return self.__parsedTokens__

    def __load_syntaxRules__(self,json_conf):
        for rule in json_conf['syntaxRules']:
            syntaxGroupRule = SyntaxGroupRule()
            syntaxGroupRule.list_name = rule['name']
            syntaxGroupRule.init_pattern(rule['pattern'],rule['ignore'] if 'ignore' in rule else None)
            self.syntaxRules.append(syntaxGroupRule)
            print("Loaded Rule: ",rule['pattern'])

    def load_config(self, filename):
        json_config = json.load(open(filename))
        self.__load_syntaxRules__(json_config)

    def scan_tokens(self, tokens_list):
        pos = 0
        parsedTokens = []
        i = -1
        while True:
            i += 1
            tokensMatched = None
            ruleMatch = None
            for syntaxRule in self.syntaxRules:
                tokensMatched = syntaxRule.match(tokens_list, pos)
                if (tokensMatched is not None):
                    ruleMatch = syntaxRule
                    break;

            if (tokensMatched == None):
                parsedTokens.append(tokens_list[pos])
                pos += 1
                print(i,':',pos,':',':Unable to find a match')
            else:
                parsedTokens.append(tokensMatched)
                print(i,':',pos,':',':MATCH: ',ruleMatch.list_name)
                #print(i,',startPos:',startPos,',len:',len(token.token_value),',found:"',token.token_type,'",value:',token.token_value)
                pos += len(tokensMatched)

            if (pos >= len(tokens_list)):
                break

