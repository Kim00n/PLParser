from src.tokenizer import Tokenizer
from src.parser import Parser
from src.syntaxGroupRule import SyntaxGroupRule

tokenizer = Tokenizer()
tokenizer.load_config('./syntaxConfig.json')
tokenizer.scan_source(open('../Parser/test.pkb').read())

parser = Parser()
parser.load_config('./syntaxConfig.json')
parser.scan_tokens(tokenizer.tokens)

#rule = SyntaxGroupRule()
#rule.init_pattern("type (<type_name> .id) is (<type_spec> !';'.id*) ';'",ignore=".blk")