from . import WftLex
from .ply import *
from ..Error import SNError
from ..Node import Indefinite, Arbitrary
from .UniqueRep import *

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
         |              Y_WftNode
         |              VarNode
         |              Function
    '''
    p[0] = p[1]
    global top_wft
    top_wft = p[0]

# e.g. if(wft1, wft2)
def p_BinaryOp1(p):
    '''
    BinaryOp :          Impl LParen Argument Comma Argument RParen
    '''
    filler_set = [p[3], p[5]]
    p[0] = rep_impl(filler_set, int(p[1][:1]))
def p_BinaryOp2(p):
    '''
    BinaryOp :          AndImpl LParen Argument Comma Argument RParen
    '''
    filler_set = [p[3], p[5]]
    p[0] = rep_impl(filler_set, len(p[3]))
def p_BinaryOp3(p):
    '''
    BinaryOp :          SingImpl LParen Argument Comma Argument RParen
    '''
    filler_set = [p[3], p[5]]
    p[0] = rep_impl(filler_set, 1)


# e.g. and(wft1, wft2)
def p_NaryOp1(p):
    '''
    NaryOp :            And LParen Wfts RParen
    '''
    filler_set = [p[3]]
    p[0] = rep_andor(p[1], filler_set, len(p[3]), len(p[3]))
def p_NaryOp2(p):
    '''
    NaryOp :            Or LParen Wfts RParen
    '''
    filler_set = [p[3]]
    p[0] = rep_andor(p[1], filler_set, 1, len(p[3]))
def p_NaryOp3(p):
    '''
    NaryOp :            Not LParen Wfts RParen
           |            Nor LParen Wfts RParen
    '''
    filler_set = [p[3]]
    p[0] = rep_andor(p[1], filler_set, 0, 0)
def p_NaryOp4(p):
    '''
    NaryOp :            Nand LParen Wfts RParen
    '''
    filler_set = [p[3]]
    p[0] = rep_andor(p[1], filler_set, 0, len(p[3]) - 1)
def p_NaryOp5(p):
    '''
    NaryOp :            Xor LParen Wfts RParen
    '''
    filler_set = [p[3]]
    p[0] = rep_andor(p[1], filler_set, 1, 1)
def p_NaryOp6(p):
    '''
    NaryOp :            Iff LParen Wfts RParen
           |            DoubImpl LParen Wfts RParen
    '''
    filler_set = [p[3]]
    p[0] = rep_thresh("iff", filler_set, 1, len(p[3]) - 1)
def p_NaryOp7(p):
    '''
    NaryOp :            Thnot LParen Wfts RParen
           |            Thnor LParen Wfts RParen
    '''
    raise SNePSVarError("Thnot not yet implemented!")

# e.g. thresh{1, 2}(wft1)
def p_MinMaxOp(p):
    '''
    MinMaxOp :          AndOr LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer RBrace LParen Wfts RParen
    '''
    min = int(p[3])
    if len(p) == 8:
        filler_set = p[6]
        max = len(p[6]) - 1
    else:
        max = int(p[5])
        filler_set = p[8]
    if p[1] == "thresh":
        p[0] = rep_thresh(p[1], filler_set, min, max)
    else:
        p[0] = rep_andor(p[1], filler_set, min, max)

# e.g. close(Dog, wft1)
def p_CloseStmt(p):
    '''
    CloseStmt :         Close LParen AtomicNameSet Comma Wft RParen
    '''
    raise SNePSVarError("Close not yet implemented!")

# e.g. brothers(Tom, Ted)
def p_Function(p):
    '''
    Function :          Identifier LParen Arguments RParen
             |          Integer LParen Arguments RParen
    '''
    filler_set = p[3]
    p[0] = build_molecular(p[1], filler_set)

# e.g. ?example()
def p_QIdenStmt(p):
    '''
    QIdenStmt :         QIdentifier LParen Wfts RParen
              |         QIdentifier LParen RParen
    '''
    raise SNePSVarError("? not yet implemented!")

# e.g. wft1
def p_Argument1(p):
    '''
    Argument :          Wft
    '''
    p[0] = [p[1]]

# e.g. None
def p_Argument2(p):
    '''
    Argument :          None
    '''
    p[0] = []

# e.g. setOf(wft1, wft2)
def p_Argument3(p):
    '''
    Argument :          ArgumentFunction
             |          LBracket RBracket
             |          LBracket Wfts RBracket
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]

def p_ArgumentFunction(p):
    '''
    ArgumentFunction :  SetOf LParen RParen
                     |  SetOf LParen Wfts RParen
    '''
    if len(p) == 4:
        p[0] = []
    else:
        p[0] = p[3]

def p_Wfts(p):
    '''
    Wfts :              Wft
         |              Wfts Comma Wft
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_Arguments(p):
    '''
    Arguments :         Argument
              |         Arguments Comma Argument
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_AtomicNameSet(p):
    '''
    AtomicNameSet :
                  |     Identifier
                  |     Integer
                  |     LParen AtomicNames RParen
    '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[2]

def p_AtomicNames(p):
    '''
    AtomicNames :       AtomicName
                |       AtomicNames Comma AtomicName
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_AtomicName(p):
    '''
    AtomicName :        Identifier
               |        Integer
    '''
    p[0] = UniqueRep(name=p[1])

def p_VarNode(p):
    '''
    VarNode :           IndNode
            |           ArbNode
    '''
    if int(p[1][3:]) >= Arbitrary.counter:
        raise SNePSVarError('Invalid arb number. Max number: {}'.format(Arbitrary.counter - 1))
    p[0] = current_network.nodes[p[1]].unique_rep

def p_Y_WftNode(p):
    '''
    Y_WftNode :         WftNode
    '''
    if int(p[1][3:]) >= Molecular.counter:
        raise SNePSVarError('Invalid wft number. Max number: {}'.format(Molecular.counter - 1))
    p[0] = current_network.nodes[p[1]].unique_rep

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
    variables[p[3]] = new_var

def p_SomeStmt(p):
    '''
    SomeStmt :          Some LParen Var LParen AtomicNameSet RParen Comma Argument RParen
    '''
    global variables
    global current_network
    new_var = Indefinite(p[3], current_network.sem_hierarchy.get_type('Entity'))
    if p[3] in variables and variables[p[3]] != new_var:
        raise SNePSVarError("Variable with name {} defined twice in same context!".format(new_var.name))
    variables[p[3]] = new_var

def p_Var(p):
    '''
    Var :               Identifier
        |               Integer
    '''
    p[0] = p[1]

def p_error(p):
    if p is None:
        raise SNePSVarError("Term reached end unexpectedly.")
    else:
        raise SNePSVarError("Syntax error on token '" + p.type + "'")

# =====================================
# ------------- GET FNS ---------------
# =====================================

def rep_molecular(caseframe_name, children_reps):
    """ Returns a UniqueRep object corresponding to the node """
    caseframe = current_network.find_caseframe(caseframe_name)
    name = caseframe.name
    return UniqueRep(caseframe_name=caseframe.name, children=children_reps)

# def rep_thresh (caseframe_name, filler_set, min, max):
#     """ Returns a UniqueRep object corresponding to the node """
#
#     # Simplifies caseframes - See slide 439:
#     # https://cse.buffalo.edu/~shapiro/Courses/CSE563/Slides/krrSlides.pdf
#     if caseframe_name == 'thresh':
#         num_nodes = len(filler_set[0])
#         if min == 1 and max == num_nodes - 1:
#             caseframe_name = 'iff'
#
#     caseframe = current_network.find_caseframe(caseframe_name)
#     frame = Frame(caseframe, filler_set)
#     for node in current_network.nodes.values():
#         if node.has_frame(frame) and node.has_min_max(min, max):
#             return node
#     wftNode = ThreshNode(frame, min, max)
#     current_network.nodes[wftNode.name] = wftNode
#     return wftNode
#
# def rep_andor (caseframe_name, filler_set, min, max):
#     """ Returns a UniqueRep object corresponding to the node """
#
#     # Simplifies caseframes - See slide 437:
#     # https://cse.buffalo.edu/~shapiro/Courses/CSE563/Slides/krrSlides.pdf
#     if caseframe_name == 'andor':
#         num_nodes = len(filler_set[0])
#         if min == max == num_nodes:
#             caseframe_name = 'and'
#         elif min == 1 and max == num_nodes:
#             caseframe_name = 'or'
#         elif min == 0 and max == num_nodes - 1:
#             caseframe_name = 'nand'
#         elif min == max == 0:
#             caseframe_name = 'nor'
#         elif min == max == 1:
#             caseframe_name = 'xor'
#
#     caseframe = current_network.find_caseframe(caseframe_name)
#     frame = Frame(caseframe, filler_set)
#     for node in current_network.nodes.values():
#         if node.has_frame(frame) and node.has_min_max(min, max):
#             return node
#     wftNode = AndOrNode(frame, min, max)
#     current_network.nodes[wftNode.name] = wftNode
#     return wftNode
#
# def rep_impl(filler_set, bound):
#     """ Returns a UniqueRep object corresponding to the node """
#     caseframe = current_network.find_caseframe("if")
#     frame = Frame(caseframe, filler_set)
#     for node in current_network.nodes.values():
#         if node.has_frame(frame) and node.has_bound(bound):
#             return node
#     wftNode = ImplNode(frame, bound)
#     current_network.nodes[wftNode.name] = wftNode
#     return wftNode

# =====================================
# ----------- VARIABLE FN -------------
# =====================================


def get_vars(wft : str, network):
    """ Strips vars from a wft and ensures uniqueness,
    then returns a dictionary in which variable names correspond to their nodes """

    global current_network
    current_network = network
    yacc.yacc()

    yacc.parse(wft)

    # Reset and return variables
    global variables
    ret_variables = variables
    variables = {}
    return ret_variables
