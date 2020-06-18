from . import PathLex
from .ply import *
from .Network import *

current_network = None
tokens = PathLex.tokens

# =====================================
# -------------- RULES ----------------
# =====================================

def p_Path(p):
    '''
    Path :              SlotName
         |              ReverseSlotName
         |              converse LParen Path RParen
         |              kplus LParen Path RParen
         |              kstar LParen Path RParen
         |              compose LParen Paths RParen
         |              or LParen Paths RParen
         |              and LParen Paths RParen
         |              irreflexive-restrict LParen Path RParen
    '''

def p_Path(p):
    '''
    Paths :
          |             Path
          |             Path Comma Paths
    '''

# =====================================
# ------------ RULES END --------------
# =====================================

def path_parser(path, network):
    global current_network
    current_network = network
    yacc.yacc()
    if path != '':
        try:
            yacc.parse(pase)
        except Exception as e:
            print(e)
