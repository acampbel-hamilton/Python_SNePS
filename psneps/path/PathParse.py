from . import PathLex
from ..ply import *
from ..Network import *
from ..Error import SNError
from .. Paths import *

class SNePSPathError(SNError):
    pass

current_network = None
tokens = PathLex.tokens
producedPath = None

# =====================================
# -------------- RULES ----------------
# =====================================

def p_Path1(p):
    '''
    Path :              SlotName
    '''
    p[0] = BasePath(current_network.find_slot(p[1]))
    global producedPath = p[0]

def p_Path2(p):
    '''
    Path :              ReverseSlotName
         |
         |
    '''
    global producedPath

def p_Path3(p):
    '''
    Path :              Path Comma ExPoint
    '''
    global producedPath

def p_Path4(p):
    '''
    Path :              Converse LParen Path RParen
    '''
    global producedPath

def p_Path5(p):
    '''
    Path :              KPlus LParen Path RParen
         |              KStar LParen Path RParen
         |              Compose LParen Paths RParen
         |              Or LParen Paths RParen
         |              And LParen Paths RParen
    '''
    global producedPath

def p_Path6(p):
    '''
    Path :              Irreflexive-Restrict LParen Path RParen
    '''
    raise SNePSPathError("Not yet implemented!")

def p_Paths(p):
    '''
    Paths :             Path
          |             Paths Comma Path
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_error(p):
    if p is None:
        raise SNePSPathError("PARSING FAILED: Term reached end unexpectedly.")
    else:
        raise SNePSPathError("PARSING FAILED: Syntax error on token '" + p.type + "'")

# =====================================
# ------------ RULES END --------------
# =====================================

def path_parser(path, network):
    global current_network
    current_network = network
    yacc.yacc()
    if path != '':
        try:
            yacc.parse(path)
            global producedPath
            return producedPath
        except SNError as e:
            if type(e) is not SNePSPathError:
                print("PARSING FAILED:\n\t", end='')
            print(e)
