import re

class RuleScanner():
    def __init__(self, version = None):
        self.__version__ = version
        # init regex syntax elements
        if version=='{}':
            self.re_syntax = dict(
                def_group = re.compile(r"([\(][^\)]+[\)])"),
                def_cat_name = re.compile(r"([\<][^>]+[\>])"),
                def_token = re.compile(r"([\{][^\}]+[\}](([\*\+\?])|([\[][^\]]+[\]]))?)"),
                def_token_part = re.compile(r"([,]?)([!\<\>\=]?)(([a-zA-Z0-9]+)|([\'][^']+[\']))"),
                def_occ = re.compile(r"(([\*\+\?])|([\[][^\]]+[\]]))")
            )
            self.__token_split_char__ = ','
            self.__token_separator__ = '{'
            self.__group_or_separator__ = '|'

        else:
            self.re_syntax = dict(
                def_group = re.compile(r"([ ]*)([\(][^\)]+[\)])(([\*\+\?])|([\[][^\]]+[\]]))?([ ]*)"),
                def_cat_name = re.compile(r"([\<][^>]+[\>])"),
                def_token = re.compile(r"([ ]*)(?:[\.]?([!\<\>\=]?)(([a-zA-Z0-9]+)|([\'][^']+[\'])))(\1?)(([\*\+\?])|([\[][^\]]+[\]]))?([ ]*)"),
                def_token_part = re.compile(r"([.]?)([!\<\>\=]?)(([a-zA-Z0-9]+)|([\'][^']+[\']))"),
                def_occ = re.compile(r"(([\*\+\?])|([\[][^\]]+[\]]))")
            )
            self.__token_split_char__ = '.'
            self.__token_separator__ = ''
            self.__group_or_separator__ = '|'

    @property
    def version(self):
        return self.__version__

    @property
    def token_split_char(self):
        return self.__token_split_char__

    @property
    def token_separator(self):
        return self.__token_separator__

    @property
    def group_or_separator(self):
        return self.__group_or_separator__

    def match_grp(self, pattern, pos, strip = ' '):
        el = self.re_syntax['def_group'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        if strip == None:
            return el.group(0)
        return el.group(0).strip(strip)

    def match_cat_name(self, pattern, pos):
        el = self.re_syntax['def_cat_name'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        return el.group(0).strip(' ')

    def match_token(self, pattern, pos, strip = ' '):
        el = self.re_syntax['def_token'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        if strip == None:
            return el.group(0)
        return el.group(0).strip(strip)

    def match_token_part(self, pattern, pos):
        el = self.re_syntax['def_token_part'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        return el.group(0).strip(' ')

    def match_occ(self, pattern, pos):
        el = self.re_syntax['def_occ'].match(pattern, pos)
        if el is None or el.group == '':
            return None
        return el.group(0).strip(' ')

