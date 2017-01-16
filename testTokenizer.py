from src.tokenizer import Tokenizer
from src.parser import Parser

tokenizer = Tokenizer()
tokenizer.load_config('./syntaxConfig.json')
tokenizer.scan_source(open('../Parser/test.pkb').read())

parser = Parser()
parser.load_config('./syntaxConfig.json')
print(parser.syntax_rules["package_declaration"].match(tokenizer.tokens))

#rule = SyntaxGroupRule()
#rule.init_pattern("type (<type_name> .id) is (<type_spec> !';'.id*) ';'",ignore=".blk")