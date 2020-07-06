from .ply import *
from re import match
from ..Node import Indefinite, Arbitrary

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
    'close',
    'iff'
)

tokens = (
    'LParen',
    'RParen',
    'WftNode',
    'Impl',
    'DoubImpl',
    'Integer',
    'QIdentifier',
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
    'Iff',
    'AndImpl',
    'SingImpl',
    'LBrace',
    'RBrace',
    'Comma',
    'LBracket',
    'RBracket',
    'VarName'
)

t_LParen  = r'\('
t_RParen  = r'\)'
t_Integer = r'\d+'
t_QIdentifier = r'\?[A-Za-z][A-Za-z0-9_]*'
t_LBrace = r'{'
t_RBrace = r'}'
t_LBracket = r'\['
t_RBracket = r'\]'
t_Comma = r','
t_DoubImpl = r'<=>'
t_Impl = r'\d+=>'
t_AndImpl = r'&=>'
t_SingImpl = r'(v)?=>'

def t_Identifier(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    if match(r'^wft\d+$', t.value):
        t.type = 'WftNode'
    if match(r'^(arb|ind)\d+$', t.value):
        t.type='VarName'
    elif t.value == 'if':
        t.type = 'SingImpl'
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
from .ply import lex
lexer = lex.lex()

if __name__ == '__main__':
    lexer = lex.lex()
    while True:
        try:
            s = input('Command: ')
        except EOFError:
            break
        if s == 'exit()':
            break
        try:
            lexer.input(s)
            while True:
                token = lexer.token()
                if not token:
                    break
                print(token)
        except: # This is probably not a good idea...
            print("Syntax error")
