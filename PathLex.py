from . import ply
from re import match
from sys import stderr

keywords = (
    'converse',
    'kplus',
    'kstar',
    'compose',
    'or',
    'and',
    'irreflexive-restrict'
)

tokens = (
    'LParen',
    'RParen',
    'SlotName',
    'ExPoint',
    'ReverseSlotName',
    'Comma'
)

t_LParen  = r'\('
t_RParen  = r'\)'
t_SlotName = r'[A-Za-z_][A-Za-z0-9_]*'
t_ExPoint = r'\!'
t_ReverseSlotName = r'[A-Za-z_][A-Za-z0-9_]*\-'
t_Comma = r','

def t_error(t):
    print("Invalid syntax: ", t.value, file=stderr)
    t.lexer.skip(1)

t_ignore = ' \t\r\n\f\v'

# Build the lexer
from .ply import lex
lexer = lex.lex()
