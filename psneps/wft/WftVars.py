from . import WftLex
from .ply import *
from ..Error import SNError

variables = {}

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
         |              Y_WftNode
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

# e.g. every{x}(Isa(x, Dog))
def p_EveryStmt(p):
    '''
    EveryStmt :         Every LParen Var Comma Argument RParen
    '''
    global variables
    arb = p[3]
    if not isinstance(arb, Arbitrary):
        raise SNePSWftError("Variable {} is not arbitrary!".format(arb.name))

    # Add restrictions
    for node in p[5].nodes:
        new_restriction(arb, node)

    # Store in network
    arb.store_in(current_network)
    p[0] = arb


# e.g. some{x(y)}(Isa(x, y))
def p_SomeStmt(p):
    '''
    SomeStmt :          Some LParen Var LParen AtomicNameSet RParen Comma Argument RParen
    '''
    global variables
    ind = p[3]
    if not isinstance(ind, Isndefinite):
        raise SNePSWftError("Variable {} is not indefinite!".format(ind.name))

    # Add dependencies
    # TODO
    for var_name in p[5]:
        if var_name not in variables:
            raise SNePSWftError("Variable \"{}\" does not exist".format(var_name))
        if variables[var_name] is ind:
            raise SNePSWftError("Variables cannot depend on themselves".format(var_name))
        ind.add_dependency(variables[var_name])

    # Add restrictions
    for node in p[8].nodes:
        new_restriction(ind, node)

    # Store in network
    ind.store_in(current_network)
    p[0] = ind

def p_Var(p):
    '''
    Var :                Identifier
           |            Integer
    '''

# e.g. close(Dog, wft1)
def p_CloseStmt(p):
    '''
    CloseStmt :         Close LParen AtomicNameSet Comma Wft RParen
    '''

# e.g. brothers(Tom, Ted)
def p_Function(p):
    '''
    Function :          Identifier LParen Arguments RParen
             |          Integer LParen Arguments RParen
    '''

# e.g. ?example()
def p_QIdenStmt(p):
    '''
    QIdenStmt :         QIdentifier LParen Wfts RParen
              |         QIdentifier LParen RParen
    '''

# e.g. wft1
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

def p_Y_WftNode(p):
    '''
    Y_WftNode :         WftNode
    '''

def p_VarNode(p):
    '''
    VarNode :           IndNode
            |           ArbNode
    '''

def p_error(p):
    if p is None:
        raise SNePSWftError("Term reached end unexpectedly.")
    else:
        raise SNePSWftError("Syntax error on token '" + p.type + "'")


# =====================================
# ----------- VARIABLE FN -------------
# =====================================


def get_vars(wft : str, network):
    """ Strips vars from a wft and ensures uniqueness,
    then returns a dictionary in which variable names correspond to their nodes """

    yacc.yacc()
    try:
        yacc.parse(wft)

        # Reset and return variables
        global variables
        ret_variables = variables
        variables = {}
        return variables

    # Supress errors
    except SNError as e:
        print("ERROR:", e)
        return {}
