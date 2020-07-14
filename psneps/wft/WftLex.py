""" This file uses regular expression matching to generate tokens from a
string of text entered by the user, and corresponding to a Python_SNePS
well-formed-term. """

# =====================================
# -------------- IMPORTS --------------
# =====================================

from .ply import *
from re import match

# =====================================
# --------------- TOKENS --------------
# =====================================

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
    'IndNode',
    'ArbNode'
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

def t_SingImpl(t):
    r'v?=>'
    return t

def t_Identifier(t):
    r'[A-Za-z][A-Za-z0-9_]*'
    if match(r'^wft\d+$', t.value):
        t.type = 'WftNode'
    if match(r'^arb\d+$', t.value):
        t.type='ArbNode'
    if match(r'^ind\d+$', t.value):
        t.type='IndNode'
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

# =====================================
# -------------- TEST FN --------------
# =====================================

# Repeatedly prompts for user input and prints the tokens generated.
# Use "exit()" to exit.

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
        except:
            print("Syntax error")
