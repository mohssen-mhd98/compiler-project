from ply import lex

class Lexer:

    reserved = {
        'if': 'IF', 'then': 'THEN',
        'else': 'ELSE', 'while': 'WHILE',
        'true':  'TRUE', 'void':  'VOID',
        'for': 'FOR', 'bool': 'BOOLEAN',
        'print': 'PRINT', 'return': 'RETURN',
        'main': 'MAIN', 'elif': 'ELIF', 'int': 'INTEGER',
        'float': 'FLOAT', 'false': 'FALSE'
     }

    tokens = [
        "LRB", "RRB", "LCB", "RCB",
        "RSB", "LSB",
        "ERROR", "SUM", "SUB", "MUL", "DIV", "REMAINDER",
        "LT", "GT", "SEMICOLON", "ID", "INTEGERNUMBER", "FLOATNUMBER", "ASSIGN",
        "AND", "OR", "EQ", "NE", "LE", "GE", "NOT", "COMMA"
    ] + list(reserved.values())

    '''
        tokens = [
        "IF", "WHILE", "PRINT",
        "LRB", "RRB", "LCB", "RCB",
        "Error", "SUM", "SUB", "MUL", "DIV",
        "LT", "GT", "SEMICOLON", "ID", "INTEGER", "FLOAT"
    ]'''

    st = []
    # COLONS
    t_SEMICOLON = r';'
    # BRACKETS
    t_LRB = r'\('
    t_RRB = r'\)'
    t_LCB = r'\{'
    t_RCB = r'\}'
    t_RSB = r'\]'
    t_LSB = r'\['
    # OPERATOR
    t_SUM = r'\+'
    t_SUB = r'\-'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_REMAINDER = r'\%'
    t_ASSIGN = r'\='
    t_LT = r'\<'
    t_GT = r'\>'
    t_LE = r'\<\='
    t_GE = r'\>\='
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_EQ = r'\=\='
    t_NE = r'\!\='
    t_NOT = r'\!'
    t_COMMA = r'\,'
    # KW
   # t_IF = r'if'
    #t_WHILE = r'while'
    #t_PRINT = r'print'
    #r'\([-|+](\d+)\)|(\d+)'

    def t_ERROR(self, t) :
       r'[0-9]+[a-z_A-Z]+ | [\+ \* \% \- \/]{3,} | [\+\*\%\-\/]{2,} | [0-9\.]*(\.)[0-9\.]*(\.)+[0-9\.]* | (^[-+])?(\d){10,}\.\d* | (^[-+])?(\d){10,}'
       return  t

    '''def t_SUM(self, t):
        r'\+'
        Lexer.st.append(t.value)
        l = len(Lexer.st)
        if(Lexer.st[l-2]=="+"):
            self.error1(t, Lexer.st[l-2])
        return t'''


    def t_ID(self, t):
        r'[a-z_A-Z][a-z_A-Z0-9]*'
        t.type = Lexer.reserved.get(t.value , 'ID')
        return t

    def t_FLOATNUMBER(self, t):
        #r'[-|+]?(\d){1,1000}'
        r'(^[-+])?\d*\.\d*'
        t.value = float(t.value)
        Lexer.st.append(t.value)
        return t

    def t_INTEGERNUMBER(self, t):
        #r'[-|+]?(\d){1,1000}'
        #r'(^[+-])?[1-9][0-9]*|0+'
        r'(^[+-])?[0-9]+'
        ''''if int(t.value) > 0 :
            t.value = "+" + str(int(t.value))
        else:
            t.value = str(int(t.value))'''''
        Lexer.st.append(t.value)
        return t



    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = '\n \t '
    t_ignore_COMMENT = r'\#.*'

    def t_error(self, t):
        raise Exception('Error at', t.value)

    def error1(self, t, st):
        raise Exception('Error at', t.value, st)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
