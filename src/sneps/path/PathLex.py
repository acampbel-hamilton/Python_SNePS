""" This file uses regular expression matching to generate tokens from a
string of text entered by the user, and corresponding to a Python_SNePS
path expression. """

# =====================================
# -------------- IMPORTS --------------
# =====================================

from ..ply import *
from re import match

# =====================================
# --------------- TOKENS --------------
# =====================================

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
t_Comma = r','

def t_IrreflexiveRestrict(t):
    r'irreflexive-restrict'
    return t

def t_ReverseSlotName(t):
    r'[A-Za-z][A-Za-z0-9_]*\-'
    return t

def t_SlotName(t):
    r'[A-Za-z][A-Za-z0-9_]*'
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
from ..ply import lex
path_lexer = lex.lex()

# =====================================
# -------------- TEST FN --------------
# =====================================

# Repeatedly prompts for user input and prints the tokens generated.
# Use "exit()" to exit.

if __name__ == '__main__':
    while True:
        try:
            s = input('Command: ')
        except EOFError:
            break
        if s == 'exit()':
            break
        try:
            path_lexer.input(s)
            while True:
                token = path_lexer.token()
                if not token:
                    break
                print(token)
        except:
            print("Syntax error")
