from src.tokenListTemplate import TokenListTemplate


class SyntaxTemplate():
    def __init__(self):
        self.__syntax_rules__ = []

    def load_syntax (self,json_conf):
        for rule in json_conf['syntax']:
            self.process_syntax_rule(rule['name'],rule['pattern'])

    def process_syntax_rule(self, name, pattern):
        syntax_rule = TokenListTemplate()
        syntax_rule.set_list_name(name)
        syntax_rule.init_pattern(pattern)
        self.__syntax_rules__.append(syntax_rule)
        print (syntax_rule.tokens)



