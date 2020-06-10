import ply.yacc as yacc

from Lexer2 import MyLexer

lexer = MyLexer()
lexer.build()
tokens = MyLexer.tokens

names = {}


def p_statement_assign(t):
    """statement : LOCAL_NAME '=' expression"""
    names[t[1]] = t[3]


def p_expression_add(t):
    """expression : INT_TYPE ADD term ',' term"""
    t[0] = t[3] + t[5]


def p_expression_mul(t):
    """expression : INT_TYPE MUL term ',' term"""
    t[0] = t[3] * t[5]


def p_expression_div(t):
    """expression : INT_TYPE DIV term ',' term"""
    t[0] = t[3] // t[5]


def p_expression_sub(t):
    """expression : INT_TYPE SUB term ',' term"""
    t[0] = t[3] - t[5]


def p_term_number(t):
    """term : NUMBER"""
    t[0] = t[1]


def p_term_local_name(t):
    """term : LOCAL_NAME"""
    try:
        t[0] = names[t[1]]
    except KeyError:
        raise ValueError(f'Undefined name {t[1]}')


def p_code_block(t):
    """code_block : '{' statement '}'"""
    print(t)


def p_statement_list(t):
    """statement_list : statement
                      | statement statement_list"""


def p_error(t):
    print(f"Syntax error at '{t.value}'")


parser = yacc.yacc()

with open('test.txt') as f:
    for line in f:
        result = parser.parse(line)
        if line != '':
            print(names)
