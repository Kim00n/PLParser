from src.tokenizer import Tokenizer
from src.tokenListTemplate import TokenListTemplate

tokenizer = Tokenizer()
tokenizer.load_config('./syntaxConfig.json')
tokenizer.tokenize(open('../Parser/test.pkb').read())
#with open('./token_result.json', 'w') as out_file:
#    out_file.write(tokenizer.get_json_nodes() + '\n')


tokens_tpl = TokenListTemplate()
#tokens_tpl.init_pattern("{,word}", ignore="{,blk}")
tokens_tpl.init_pattern("{create}{or}{replace}{package}{body}(<package_name>{,word}){is}", ignore="{,blk}")
res = tokens_tpl.match(tokenizer.tokens)

tokens_tpl.init_pattern("{!';'}*{';'}", ignore="{,blk}")
res = tokens_tpl.match(tokenizer.tokens, len(res))

for i in res:
    print(i.get_json_node())