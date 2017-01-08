import json
import re
from token import Token

class Parser():
    def __init__(self):
        self.tokens_def = []
        self.syntax_def = []

    def __load_tokens__(self,json_conf):
        for tk in json_conf['tokens']:
            tk['re']=re.compile(tk['pattern'])
            self.tokens_def.append(tk)

    def __load_syntax__(self,json_conf):
        for rule in json_conf['syntax']:
            name=rule['name']
            pattern=rule['pattern']

    def load_config(self, filename):
        json_config = json.load(open(filename))
        self.__load_tokens__(json_config)
        #self.__load_rules__(json_config)

    def tokenizer(self, source_file):
        startPos = 0
        source_json = {}
        source_json['lexic'] = []
        i = -1
        while True:
            i += 1
            token_match = None
            for el in self.tokens_def:
                token_match = el['re'].match(source_file, startPos)
                token_found = el['name']
                if (token_match is not None and token_match.group() != ''):
                    break;

            if (token_match == None):
                print(i,':',startPos,':',':Unable to find a match')
                break
            else:
                token_value = token_match.group(0)
                token = Token(token_found, token_value, startPos)
                source_json['lexic'].append(token.get_json_node())
                print(i,':',startPos,':',token_value.__len__(),':"',token_found,'":',token_value)
                startPos += token_value.__len__()

            if (startPos >= source_file.__len__()):
                break
        return json.dumps(source_json,indent=3)

parser = Parser()
parser.load_config('./syntaxConfig.json')
json_result = parser.tokenizer(open('../../Parser/pkg_ctx.pkb').read())
with open('./token_result.json', 'w') as out_file:
    out_file.write(json_result + '\n')
