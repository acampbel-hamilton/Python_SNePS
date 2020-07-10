from . import WftLex
from .ply import *
from ..Error import SNError
from ..Node import Indefinite, Arbitrary
from .UniqueRep import *

current_network = None
tokens = WftLex.tokens
variables = {}
in_var_stmt = 0

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
    if in_var_stmt > 0:
        p[0] = p[1]

def p_BinaryOp(p):
    '''
    BinaryOp :          Impl LParen Argument Comma Argument RParen
             |          AndImpl LParen Argument Comma Argument RParen
             |          SingImpl LParen Argument Comma Argument RParen
    '''
    if in_var_stmt > 0:
        p[0] = UniqueRep(name='')

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
    global in_var_stmt
    global variables
    global current_network
    new_var = Arbitrary(p[3], current_network.sem_hierarchy.get_type('Entity'))
    if p[3] in variables and variables[p[3]] != new_var:
        raise SNePSVarError("Variable with name {} defined twice in same context!".format(new_var.name))
    variables[p[3]] = new_var
    in_var_stmt -= 1

def p_SomeStmt(p):
    '''
    SomeStmt :          Some LParen Var LParen AtomicNameSet RParen Comma Argument RParen
    '''
    global in_var_stmt
    global variables
    global current_network
    new_var = Indefinite(p[3], current_network.sem_hierarchy.get_type('Entity'))
    if p[3] in variables and variables[p[3]] != new_var:
        raise SNePSVarError("Variable with name {} defined twice in same context!".format(new_var.name))
    variables[p[3]] = new_var
    in_var_stmt -= 1

def p_Var(p):
    '''
    Var :               Identifier
        |               Integer
    '''
    global in_var_stmt
    in_var_stmt += 1
    p[0] = p[1]

def p_error(p):
    pass

# =====================================
# ------------- GET FNS ---------------
# =====================================

# def rep_molecular(caseframe_name, children_reps):
#     """ Returns a UniqueRep object corresponding to the node """
#     caseframe = current_network.find_caseframe(caseframe_name)
#     name = caseframe.name
#     (caseframe_name=caseframe.name, children=children_reps)
#
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
    global in_var_stmt
    ret_variables = variables
    variables = {}
    in_var_stmt = 0
    return ret_variables
