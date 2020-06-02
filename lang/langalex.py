from ply import *
from re import match
from sys import argv, exit

if len(argv) != 2:
    print("Usage: python3 langalex.py filename")
    exit(1)

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

tokens = keywords + (
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
    'SetOf'
)

t_LParen  = r'\('
t_RParen  = r'\)'
t_Impl = r'=>'
t_DoubImpl = r'<=>'
t_Integer = r'\d+'
t_QIdentifier = r'\?[A-Za-z_][A-Za-z0-9_]*'
t_String = r'\".*\"'

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
    elif t.value == 'someof':
        t.type = 'SetOf'
    elif t.value in keywords:
        t.type = t.value.capitalize()
    return t

def t_error(t):
    print("Invalid syntax: ", t.value)
    t.lexer.skip(1)

t_ignore = '\n'

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

lexer.input(''.join(open(argv[1]).readlines()))

while True:
     tok = lexer.token()
     if tok == '\n':
         continue
     if not tok:
         break      # No more input
     print(tok)
