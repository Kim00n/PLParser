from src.tokenizer import Tokenizer
from src.tokenTemplate import TokenTemplate

tokenizer = Tokenizer()
tokenizer.load_config('./syntaxConfig.json')
tokenizer.tokenize(open('../Parser/test.pkb').read())
#with open('./token_result.json', 'w') as out_file:
#    out_file.write(tokenizer.get_json_nodes() + '\n')
first_token = tokenizer.tokens[0]
print(first_token.get_json_node())
tokenTemplate = TokenTemplate.init_from_pattern("{create,}")

tokenTemplate.token_match(first_token)

