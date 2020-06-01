from ply import *

tokens = (
    'AND', 'OR', 'NOT', 'NOR', 'THNOT', 'THNOR' , 'NAND' 'XOR' ,
    'IFF', 'ANDOR', 'THRESH', 'SETOF', 'EVERY', 'SOME', 'CLOSE',
    'LPAREN', 'RPAREN'
)

t_LParen  = r'\('
t_RParen  = r'\)'
t_Impl = r'=>'
t_DoubImpl = r'<=>'
t_Integer = r'\d+'
t_String = r'\".*?\"'

def t_error(t):
    print("Invalid syntax: ", t.value)
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()
