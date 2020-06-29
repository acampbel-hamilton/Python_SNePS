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
    global producedPath
    producedPath = p[0]

def p_Path2(p):
    '''
    Path :              ReverseSlotName
    '''
    p[0] = BasePath(current_network.find_slot(p[1][1:]), backward=True)
    global producedPaths
    producedPath = p[0]

def p_Path3(p):
    '''
    Path :              AssertedPath
         |              ConversePath
         |              KPath
         |              MultiPath
         |              IRPath
    '''
    p[0] = p[1]
    global producedPath
    producedPath = p[0]

def p_AssertedPath(p):
    '''
    AssertedPath :       Path Comma ExPoint
    '''
    p[1].asserted = True
    p[0] = p[1]

def p_ConversePath(p):
    '''
    ConversePath :      Converse LParen Path RParen
    '''

def p_KPath1(p):
    '''
    KPath :             KPlus LParen Path RParen
    '''
    p[0] = KPlusPaths(p[3])

def p_KPath2(p):
    '''
    KPath :             KStar LParen Path RParen
    '''
    p[0] = KStarPaths(p[3])

def p_MultiPath1(p):
    '''
    MultiPath :         Compose LParen Paths RParen
    '''
    p[0] = ComposedPaths(p[3])

def p_MultiPath2(p):
    '''
    MultiPath :         Or LParen Paths RParen
    '''
    p[0] = OrPaths(p[3])

def p_MultiPath3(p):
    '''
    MultiPath :         And LParen Paths RParen
    '''
    p[0] = AndPaths(p[3])

def p_Path7(p):
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
