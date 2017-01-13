import json

from src.tokenType import TokenType


class Tokenizer():
    def __init__(self):
        self.token_types = []
        self.tokens = []

    def __load_token_types__(self,json_conf):
        for token_conf in json_conf['typeOfTokens']:
            token_type = TokenType(token_conf['type'], token_conf['pattern'])
            self.token_types.append(token_type)

    def load_config(self, filename):
        json_config = json.load(open(filename))
        self.__load_token_types__(json_config)

    def scan_source(self, source_file):
        startPos = 0
        self.tokens = []
        i = -1
        while True:
            i += 1
            token = None
            for token_type in self.token_types:
                token = token_type.match_token(source_file, startPos)
                if (token is not None):
                    break;

            if (token == None):
                print(i,':',startPos,':',':Unable to find a match')
                break
            else:
                self.tokens.append(token)
                #print(i,',startPos:',startPos,',len:',len(token.token_value),',found:"',token.token_type,'",value:',token.token_value)
                startPos += len(token.token_value)

            if (startPos >= source_file.__len__()):
                break

    def get_json_nodes(self):
        source_json = {}
        source_json['lexic'] = []
        for token in self.tokens:
            source_json['lexic'].append(token.get_json_node())
        return json.dumps(source_json,indent=3)
