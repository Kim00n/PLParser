import re

from src.token import Token


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