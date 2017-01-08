import json
import re


class TokenType():
    # describe a type of token according a given pattern (regex)
    # This class can test if a source match the pattern and return the relevant token
    def __init__(self, type, pattern):
        self.token_type = type
        self.re_token = re.compile(pattern)

    def match_token(self, source, startPos):
        self.last_value = None
        token_match = self.re_token.match(source, startPos)
        if (token_match is not None and token_match.group() != ''):
            token = Token(self.token_type, token_match.group(0), startPos)
            return token
        return None


class Token():
    def __init__(self, token_type, token_value, start_position):
        self.token_type = token_type
        self.token_value = token_value
        self.start_position = start_position

    def get_json_node(self):
        node = {}
        node['token'] = self.token_type
        node['value'] = self.token_value
        node['start_position'] = self.start_position
        node['length'] = len(self.token_value)
        return node


class Tokenizer():
    def __init__(self):
        self.token_types = []
        self.tokens = []

    def __load_tokens__(self,json_conf):
        for token_conf in json_conf['tokens']:
            token_type = TokenType(token_conf['type'],token_conf['pattern'])
            self.token_types.append(token_type)

    def load_config(self, filename):
        json_config = json.load(open(filename))
        self.__load_tokens__(json_config)

    def tokenize(self, source_file):
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
