import ply.lex as lex


class MyLexer(object):
    reserved = {
        'declare': 'DECLARE',
        'define': 'DEFINE',
        'getelementptr': 'GETELEMENTRPTR',
        'call': 'call',
        'ret': 'ret',
        'unnamed_addr': 'UNNAMED_ADDR',
        'global': 'GLOBAL',
        'constant': 'CONSTANT',
        'nocapture': 'NOCAPTURE'
    }

    tokens = [
        'NUMBER',
        'ADD',
        'SUB',
        'MUL',
        'DIV',
        'COMMENT',
        'GLOBAL_NAME',
        'LOCAL_NAME',
        'INT_TYPE',
        'GLOBAL_ID',
        'LOCAL_ID',
        'LABEL',
        'ATTR_GROUP_ID',
        'COMDAT_NAME',
        'METADATA_NAME',
        'METADATA_ID',
        'STRING',
        'LINKAGE_TYPE'
    ] + list(reserved.values())

    t_ADD = r'add'
    t_SUB = r'sub'
    t_MUL = r'mul'
    t_DIV = r'sdiv'
    literals = ['(', ')', '{', '}', ',', '=', '!', '[', ']', 'x']
    t_INT_TYPE = r'((i32)|(i8)|(i16)|(i64))\*?'
    NAME = r'[a-zA-Z$._][a-zA-Z$._0-9]*'
    ID = r'\d+'
    t_LABEL = rf'{NAME}:'
    t_ATTR_GROUP_ID = rf'\#{ID}'
    t_COMDAT_NAME = rf'${NAME}'
    t_METADATA_NAME = rf'!{NAME}'
    t_METADATA_ID = rf'!{ID}'
    t_STRING = r'c".*"'
    t_LINKAGE_TYPE = r'(private)|(internal)|(available_externally)|(linkonce)|(weak)|(common)|(appending)|(' \
                     r'extern_weak)|(external) '

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
        r'-{0,1}\d+'
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


if __name__ == '__main__':
    test = '''
    %0 = add i32 %X, %X           ; yields i32:%0
    %1 = add i32 %0, %0           ; yields i32:%1
    %result = add i32 %1, %1
    !foo = !{ !1, !2 }
    @.str = private constant [13 x i8] c"hello world\0A\00"
    '''
    lexer = MyLexer()
    lexer.build()
    lexer.test(test)
