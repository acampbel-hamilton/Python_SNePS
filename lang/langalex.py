from ply import *

tokens = (
    'LParen',
    'RParen',
    'Impl',
    'DoubImpl',
    'Integer',
    'Identifier',
    'String',
    'WftNode'
)

t_LParen  = r'\('
t_RParen  = r'\)'
t_Impl = r'=>|if'
t_Integer = r'\d+'
t_Identifier = r'[A-Za-z_][A-Za-z0-9_]*'
t_String = r'\".*\"'
t_WftNode = r'wft\d+'

def t_error(t):
    print("Invalid syntax: ", t.value)
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()
