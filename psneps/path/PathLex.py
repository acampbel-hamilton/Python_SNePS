from ..ply import *

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
    'Comma',
    'Converse',
    'KPlus',
    'KStar',
    'Compose',
    'Or',
    'And',
    'Irreflexive-Restrict'
)

t_LParen  = r'\('
t_RParen  = r'\)'
t_ExPoint = r'\!'
t_ReverseSlotName = r'[A-Za-z_][A-Za-z0-9_]*\-'
t_Comma = r','

def SlotName(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    if t.value in keywords:
        t.type = t.value.capitalize()
    return t

def t_error(t):
    print("Invalid syntax: ", t.value)
    t.lexer.skip(1)

t_ignore = ' \t\r\n\f\v'

# Build the lexer
lexer = lex.lex()
