import os
import sys
import re
from fileHandling import TextFile


ReWord = re.compile(r'([a-zA-Z0-9_#\*]*)')
#             word : ([a-zA-Z0-9_#\*]*)
ReOp = re.compile(r'([:=!+><]{1,2}|[\-](?!\-))')
#             op : ([:=!+><]{1,2}|[\-](?!\-))
ReSeparator = re.compile(r'(?:([\()\.\,])|([\|]{2}))')
#             separator : (?:([\()\.\,])|([\|]{2}))
ReBlank = re.compile(r'([ \n\t]+)')
#             blank : ([ \n\t]+)
ReStringDef = re.compile(r'(\"[^"]*\")')
#             stringDef : (\"[^"]*\")
ReString = re.compile(r"((?<!['])['])(([^'])|(''))*(['](?!'))")
#ReString = re.compile(r"((?<!['])['])(([^'](?!\1))|(''))*")
ReComment = re.compile(r"((--[^\n]+)|(\/\*((.|\n)(?!\*\/))*(.|\n)(\*\/)))")
#             comment : ((--[^\n]+)|(\/\*((.|\n)(?!\*\/))*(.|\n)(\*\/)))
ReEndOfStatment = re.compile(r'([;\/])')
#               EOStatement : ([;\/])
ReEndOfFile = re.compile(r'(\Z)')


def process(source):
    startPos = 0
    typeFound = ""
    i = -1
    while True:
        i+=1
        tokenMatch = ReWord.match(source, startPos)
        typeFound = "Word"

        if (tokenMatch is None or tokenMatch.group()==''):
            tokenMatch = ReOp.match(source, startPos)
            typeFound = "Op"

        if (tokenMatch is None or tokenMatch.group()==''):
            tokenMatch = ReSeparator.match(source, startPos)
            typeFound = "Separator"

        if (tokenMatch is None or tokenMatch.group()==''):
            tokenMatch = ReBlank.match(source, startPos)
            typeFound = "Blank"

        if (tokenMatch is None or tokenMatch.group()==''):
            tokenMatch = ReStringDef.match(source, startPos)
            typeFound = "StringDef"

        if (tokenMatch is None or tokenMatch.group()==''):
            tokenMatch = ReString.match(source, startPos)
            typeFound = "String"

        if (tokenMatch is None or tokenMatch.group()==''):
            tokenMatch = ReComment.match(source, startPos)
            typeFound = "Comment"

        if (tokenMatch is None or tokenMatch.group()==''):
            tokenMatch = ReEndOfStatment.match(source, startPos)
            typeFound = "EOStmt"

        if (tokenMatch is None or tokenMatch.group()==''):
            tokenMatch = ReEndOfFile.match(source, startPos)
            typeFound = "EOFile"

        if (tokenMatch == None):
            print(i,',',startPos,':Unable to find a match')
            break
        else:
            token = tokenMatch.group(0)
            print(i,',',startPos,':',token.__len__(),':"',typeFound,'":',token)
            startPos += token.__len__()

        if (typeFound == "EOFile"):
            break


file = TextFile().read("./pkg_ctx.pkb")
process(file)
