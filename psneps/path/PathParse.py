from . import PathLex
from ..ply import *
from ..Network import *
from ..Error import SNError

class SNePSPathError(SNError):
    pass

current_network = None
tokens = PathLex.tokens

# =====================================
# -------------- RULES ----------------
# =====================================

def p_Path(p):
    '''
    Path :              SlotName
         |              ReverseSlotName
         |              ExPoint
         |              Converse LParen Path RParen
         |              KPlus LParen Path RParen
         |              KStar LParen Path RParen
         |              Compose LParen Paths RParen
         |              Or LParen Paths RParen
         |              And LParen Paths RParen
         |              Irreflexive-Restrict LParen Path RParen
    '''
    

def p_Path(p):
    '''
    Paths :             Path
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
        yacc.parse(pase)
