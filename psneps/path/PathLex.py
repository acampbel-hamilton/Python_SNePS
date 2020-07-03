from .ply import *
from re import match

keywords = (
    'converse',
    'compose',
    'or',
    'and'
)

tokens = (
    'LParen',
    'RParen',
    'LBracket',
    'RBracket',
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
    'IrreflexiveRestrict'
)

t_LParen  = r'\('
t_RParen  = r'\)'
t_ExPoint = r'\!'
t_LBracket = r'\['
t_RBracket = r'\]'
t_ReverseSlotName = r'[A-Za-z_][A-Za-z0-9_]*\-'
t_Comma = r','

def t_IrreflexiveRestrict(t):
    r'irreflexive-restrict'
    return t

def t_SlotName(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    if t.value == 'kplus':
        t.type = 'KPlus'
    elif t.value == 'kstar':
        t.type = 'KStar'
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
        except: # We probably shouldn't catch **all** errors here.
            print("Syntax error")
