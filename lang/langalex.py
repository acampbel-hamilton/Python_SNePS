from ply import *
from re import match

keywords = (
    'xor',
    'or',
    'and',
    'thresh',
    'thnor',
    'thnot',
    'some',
    'every',
    'nand',
    'nor',
    'None',
    'not',
    'close'
)

tokens = (
    'LParen',
    'RParen',
    'WftNode',
    'Impl',
    'DoubImpl',
    'Integer',
    'QIdentifier',
    'String',
    'Identifier',
    'AndOr',
    'SetOf',
    'Xor',
    'Or',
    'And',
    'Thresh',
    'Thnor',
    'Thnot',
    'Some',
    'Every',
    'Nand',
    'Nor',
    'None',
    'Not',
    'Close',
    'OrImpl',
    'AndImpl',
    'LBrace',
    'RBrace',
    'Comma',
    'LBracket',
    'RBracket'
)

t_LParen  = r'\('
t_RParen  = r'\)'
t_Impl = r'=>'
t_DoubImpl = r'<=>'
t_Integer = r'\d+'
t_QIdentifier = r'\?[A-Za-z_][A-Za-z0-9_]*'
t_String = r'\".*\"'
t_OrImpl = r'v=>'
t_AndImpl = r'\d+=>'
t_LBrace = r'{'
t_RBrace = r'}'
t_LBracket = r'\['
t_RBracket = r'\]'
t_Comma = r','

def t_Identifier(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    if match(r'wft\d+', t.value):
    	t.type = 'WftNode'
    elif t.value == 'if':
        t.type = 'Impl'
    elif t.value == 'iff':
        t.type = 'DoubImpl'
    elif t.value == 'andor':
        t.type = 'AndOr'
    elif t.value == 'setof':
        t.type = 'SetOf'
    elif t.value in keywords:
        t.type = t.value.capitalize()
    return t

def t_error(t):
    print("Invalid syntax: ", t.value)
    t.lexer.skip(1)

t_ignore = ' \t\r\n\f\v'

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

if __name__ == '__main__':
    import ply.lex as lex
    lexer = lex.lex()
    while True:
        try:
            s = input('Command: ')
        except EOFError:
            break
        if str(s) == 'exit()':
            break
        try:
            lexer.input(s)
            while True:
                token = lexer.token()
                if not token:
                    break
                print(token)
        except:
            print("Syntax error")
