import re

white_list = ["SELECT\s((\*)|(DISTINCT\s[a-zA-Z,]+)|([\sa-zA-Z,()]+))\sFROM\s([A-Z][a-z]+|[a-z]+)((\sORDER\sBY\s([A-Z][a-z]+|[a-z]+)))?\;$",
"SELECT\s((\*)|(DISTINCT\s[a-zA-Z,]+)|([\sa-zA-Z,]+))\sFROM\s([A-Z][a-z]+|[a-z]+)((\sORDER\sBY\s([A-Z][a-z]+|[a-z]+)))?\;$",
"SELECT\s((\*)|(DISTINCT\s[a-zA-Z,]+)|([\sa-zA-Z,]+))\sFROM\s([A-Z][a-z]+|[a-z]+)((\sORDER\sBY\s([A-Z][a-z]+|[a-z]+)))?((\sWHERE\s[\sa-zA-Z,\*\'\=]+))?((\;))?$",
"SELECT\sCOUNT\s\*\sFROM\s([A-Z][a-z]+|[a-z]+)\;$",
"SELECT\s((\*)|([\sa-zA-Z,]+))\sFROM\s([A-Z][a-z]+|[a-z]+)((\sWHERE\s[\sa-zA-Z,\*\'\=]+))((\;))?$",
"SELECT\s([a-zA-Z]+)\(([a-zA-Z]+)\)\sFROM\s([A-Z][a-z]+|[a-z]+)\;$",
"SELECT\s((\*)|([\sa-zA-Z,()]+))\sFROM\s([A-Z][a-z]+|[a-z]+)\sWHERE\s.+?\;$",
"UPDATE.+?SET\s[a-z]+\s?\=[a-z'\s]+((\;$)|(\sWHERE\s.+?\;$))",
"INSERT INTO\s([a-zA-Z\(\)\,\s]+)\sVALUES([a-zA-Z\(\)\,\s\'\d]+)\;$",
"DELETE((\s)|(\s[a-zA-Z]+\s))FROM\s([A-Z][a-z]+|[a-z]+)\sWHERE\s.+?\;$"]

# The black list of regular expressions. This includes attempts at obfuscation such as HTML character codes.
black_list = ["[\x22\x27]\s*OR\s*\d+\x3d\d+", "(OR|AND)(\s+?).+?=[\x22\x27](\s+?)[\x22\x27]$",
      "(OR|AND)(\s+?).+?=(\s+?)[\x22\x27]$", "([\x22\x27])?(\s+?)--(\s+?)([\x22\x27])?",
      ".+?=[\x22\x27]\*[\x22\x27]\s(AND|OR)\s.+?=[\x22\x27][\x22\x27]", "\x3bDROP",
      "((\x27)|(\x22))\*((\x27)|(\x22))",
      "#.+?WHERE.+?SELECT", "--.+?[\x22\x27]","%27%20","\/\*|\*\/",";.+?$",
      "\w*((\%27)|(\'))(\s?)((\%6F)|(\%4F))((\%72)|(\%52))",
      "\w*((\%27)|(\'))(\s?)((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
      "\w*((\%6F)|(\%4F))((\%72)|(\%52))(\s?)((\%27)|(\'))",".+?(\%2A).+?$",
      ".+?(0x3(a|A)).+?$", ".+?information_schema.+?$"]


#test white list
def testAgainstWhitelist(q):
    matchobject = None
    for line in white_list:
            reg = re.compile(line)
            matchobject = reg.search(q)
            if matchobject is not None:
                print("White list")
                return False

    if matchobject == None:
        print("Not in white list")
        return True

#test against black list
# This tests a query against the black list regex.
def testAgainstBlacklist(q):
    matchobject = None
    for line in black_list:
            reg = re.compile(line)
            matchobject = reg.search(q)
            if matchobject is not None:
                print("detected")
                return False

    if matchobject == None:
        print("Not black list")
        return True

test= "INSERT INTO student (id, name, age) VALUES ('4', 'chris', '28');"
# This function determines whether files passed in via command line are valid files.
def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist. Try again with a valid file path." % arg)
        sys.exit()
    else:
        return open(arg, 'r')

def is_this_query_ok(arg):
    arg = arg.upper()
    if (testAgainstBlacklist(arg) and testAgainstWhitelist(arg)):
        return True
    return False

if __name__=="__main__":
    test = input("abcd: ")
    print("started")
    print(is_this_query_ok(test))
