import ply.lex as lex


class MyLexer(object):
    tokens = (
        'NUMBER',
        'ADD',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'LCURL',
        'RCURL',
        'COMMENT',
        'COMMA',
        'EQUALS',
        'GLOBAL_NAME',
        'LOCAL_NAME',
        'INT_TYPE',
        'GLOBAL_ID',
        'LOCAL_ID',
        'LABEL',
        'ATTR_GROUP_ID',
    )

    t_ADD = r'add'
    t_MINUS = r'minus'
    t_TIMES = r'mul'
    t_DIVIDE = r'div'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LCURL = r'\{'
    t_RCURL = r'\}'
    t_COMMA = r','
    t_EQUALS = r'='
    t_INT_TYPE = r'(i32)|(i8)|(i16)|(i64)'
    t_LABEL = r'[a-zA-Z$._0-9]+:'
    t_ATTR_GROUP_ID = r'#\d+'

    t_ignore_COMMENT = r';.*'

    def t_ID(self, t):
        r'[@%]\d+'
        if t.value[0] == '@':
            t.type = 'GLOBAL_ID'
        else:
            t.type = 'LOCAL_ID'

        return t

    def t_NAME(self, t):
        r'[@%][a-zA-Z$._][a-zA-Z$._0-9]*'
        if t.value[0] == '@':
            t.type = 'GLOBAL_NAME'
        else:
            t.type = 'LOCAL_NAME'

        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self,data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


test = '''
%0 = add i32 %X, %X           ; yields i32:%0
%1 = add i32 %0, %0           ; yields i32:%1
%result = add i32 %1, %1
'''
lexer = MyLexer()
lexer.build()
lexer.test(test)
