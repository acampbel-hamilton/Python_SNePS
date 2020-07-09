from . import WftLex
from .ply import *
from ..Error import SNError
from ..Node import Indefinite, Arbitrary

current_network = None
tokens = WftLex.tokens
variables = {}

class SNePSVarError(SNError):
    pass

# =====================================
# -------------- RULES ----------------
# =====================================

def p_Wft(p):
    '''
    Wft :               BinaryOp
         |              NaryOp
         |              MinMaxOp
         |              CloseStmt
         |              EveryStmt
         |              SomeStmt
         |              QIdenStmt
         |              AtomicName
         |              WftNode
         |              VarNode
         |              Function
    '''
def p_BinaryOp(p):
    '''
    BinaryOp :          Impl LParen Argument Comma Argument RParen
             |          AndImpl LParen Argument Comma Argument RParen
             |          SingImpl LParen Argument Comma Argument RParen
    '''
def p_NaryOp(p):
    '''
    NaryOp :            And LParen Wfts RParen
           |            Or LParen Wfts RParen
           |            Not LParen Wfts RParen
           |            Nor LParen Wfts RParen
           |            Nand LParen Wfts RParen
           |            Xor LParen Wfts RParen
           |            Iff LParen Wfts RParen
           |            DoubImpl LParen Wfts RParen
           |            Thnot LParen Wfts RParen
           |            Thnor LParen Wfts RParen
    '''
def p_MinMaxOp(p):
    '''
    MinMaxOp :          AndOr LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer RBrace LParen Wfts RParen
    '''
def p_CloseStmt(p):
    '''
    CloseStmt :         Close LParen AtomicNameSet Comma Wft RParen
    '''
def p_Function(p):
    '''
    Function :          Identifier LParen Arguments RParen
             |          Integer LParen Arguments RParen
    '''
def p_QIdenStmt(p):
    '''
    QIdenStmt :         QIdentifier LParen Wfts RParen
              |         QIdentifier LParen RParen
    '''
def p_Argument1(p):
    '''
    Argument :          Wft
             |          None
             |          ArgumentFunction
             |          LBracket RBracket
             |          LBracket Wfts RBracket
    '''
def p_ArgumentFunction(p):
    '''
    ArgumentFunction :  SetOf LParen RParen
                     |  SetOf LParen Wfts RParen
    '''
def p_Wfts(p):
    '''
    Wfts :              Wft
         |              Wfts Comma Wft
    '''
def p_Arguments(p):
    '''
    Arguments :         Argument
              |         Arguments Comma Argument
    '''
def p_AtomicNameSet(p):
    '''
    AtomicNameSet :
                  |     Identifier
                  |     Integer
                  |     LParen AtomicNames RParen
    '''
def p_AtomicNames(p):
    '''
    AtomicNames :       AtomicName
                |       AtomicNames Comma AtomicName
    '''
def p_AtomicName(p):
    '''
    AtomicName :        Identifier
               |        Integer
    '''

def p_VarNode(p):
    '''
    VarNode :           IndNode
            |           ArbNode
    '''

# =====================================
# ------------- VAR RULES -------------
# =====================================

def p_EveryStmt(p):
    '''
    EveryStmt :         Every LParen Var Comma Argument RParen
    '''
    global variables
    global current_network
    new_var = Arbitrary(p[3], current_network.sem_hierarchy.get_type('Entity'))
    if p[3] in variables and variables[p[3]] != new_var:
        raise SNePSVarError("Variable with name {} defined twice in same context!".format(new_var.name))


def p_SomeStmt(p):
    '''
    SomeStmt :          Some LParen Var LParen AtomicNameSet RParen Comma Argument RParen
    '''
    global variables
    global current_network
    new_var = Indefinite(p[3], current_network.sem_hierarchy.get_type('Entity'))
    if p[3] in variables and variables[p[3]] != new_var:
        raise SNePSVarError("Variable with name {} defined twice in same context!".format(new_var.name))

def p_Var(p):
    '''
    Var :               Identifier
        |               Integer
    '''
    p[0] = p[1]

def p_ArbVar(p):
    '''
    ArbVar :            Identifier
           |            Integer
    '''
    p[0] = p[1]

def p_error(p):
    pass

# =====================================
# ----------- VARIABLE FN -------------
# =====================================


def get_vars(wft : str, network):
    """ Strips vars from a wft and ensures uniqueness,
    then returns a dictionary in which variable names correspond to their nodes """

    global current_network
    current_network = network
    yacc.yacc()

    try:
        yacc.parse(wft)

        # Reset and return variables
        global variables
        ret_variables = variables
        variables = {}
        return ret_variables

    # Supress errors
    except SNError as e:
        if type(e) is not SNePSVarError:
            print("PARSING FAILED:\n\t", end='')
        else:
            print("PARSING FAILED: ", end='')
        print(e)
