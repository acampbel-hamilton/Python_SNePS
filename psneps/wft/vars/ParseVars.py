from .. import WftLex
from ...ply import *
from ...Error import SNError
from ...Node import Indefinite, Arbitrary, Variable
from .UniqueRep import *
from ...Node import Base, Molecular, Indefinite, Arbitrary, ThreshNode, AndOrNode, ImplNode

current_network = None
tokens = WftLex.tokens
variables = {}
var_names = {}

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

# ==============================================================================

# ==============================================================================

# e.g. if(wft1, wft2)
def p_BinaryOp1(p):
    '''
    BinaryOp :          Impl LParen Argument Comma Argument RParen
    '''
    filler_set = unique_children([p[3], p[5]])
    p[0] = rep_impl(filler_set, int(p[1][:1]))
def p_BinaryOp2(p):
    '''
    BinaryOp :          AndImpl LParen Argument Comma Argument RParen
    '''
    filler_set = unique_children([p[3], p[5]])
    p[0] = rep_impl(filler_set, len(filler_set[0]))
def p_BinaryOp3(p):
    '''
    BinaryOp :          SingImpl LParen Argument Comma Argument RParen
    '''
    filler_set = unique_children([p[3], p[5]])
    p[0] = rep_impl(filler_set, 1)

# ==============================================================================

# e.g. and(wft1, wft2)
def p_NaryOp1(p):
    '''
    NaryOp :            And LParen Wfts RParen
    '''
    filler_set = unique_children([p[3]])
    p[0] = rep_andor(p[1], filler_set, len(filler_set[0]), len(filler_set[0]))
def p_NaryOp2(p):
    '''
    NaryOp :            Or LParen Wfts RParen
    '''
    filler_set = unique_children([p[3]])
    p[0] = rep_andor(p[1], filler_set, 1, len(filler_set[0]))
def p_NaryOp3(p):
    '''
    NaryOp :            Not LParen Wfts RParen
           |            Nor LParen Wfts RParen
    '''
    filler_set = unique_children([p[3]])
    p[0] = rep_andor(p[1], filler_set, 0, 0)
def p_NaryOp4(p):
    '''
    NaryOp :            Nand LParen Wfts RParen
    '''
    filler_set = unique_children([p[3]])
    p[0] = rep_andor(p[1], filler_set, 0, len(filler_set[0]) - 1)
def p_NaryOp5(p):
    '''
    NaryOp :            Xor LParen Wfts RParen
    '''
    filler_set = unique_children([p[3]])
    p[0] = rep_andor(p[1], filler_set, 1, 1)
def p_NaryOp6(p):
    '''
    NaryOp :            Iff LParen Wfts RParen
           |            DoubImpl LParen Wfts RParen
    '''
    filler_set = unique_children([p[3]])
    p[0] = rep_thresh("iff", filler_set, 1, len(filler_set[0]) - 1)
def p_NaryOp7(p):
    '''
    NaryOp :            Thnot LParen Wfts RParen
           |            Thnor LParen Wfts RParen
    '''
    filler_set = unique_children([p[3]])
    raise SNePSVarError("Thnot not yet implemented!")

# ==============================================================================

# e.g. thresh{1, 2}(wft1)
def p_MinMaxOp(p):
    '''
    MinMaxOp :          AndOr LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer RBrace LParen Wfts RParen
    '''
    min = int(p[3])
    if len(p) == 8:
        filler_set = unique_children([p[6]])
        max = len(filler_set[0]) - 1
    else:
        max = int(p[5])
        filler_set = unique_children([p[8]])
    if p[1] == "thresh":
        p[0] = rep_thresh(p[1], filler_set, min, max)
    else:
        p[0] = rep_andor(p[1], filler_set, min, max)

# ==============================================================================

# e.g. brothers(Tom, Ted)
def p_Function(p):
    '''
    Function :          Identifier LParen Arguments RParen
             |          Integer LParen Arguments RParen
    '''
    filler_set = unique_children(p[3])
    p[0] = rep_molecular(p[1], filler_set)

# ==============================================================================

# e.g. ?example()
def p_QIdenStmt(p):
    '''
    QIdenStmt :         QIdentifier LParen Wfts RParen
              |         QIdentifier LParen RParen
    '''
    raise SNePSVarError("? not yet implemented!")

# ==============================================================================

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

# ==============================================================================

def p_ArgumentFunction(p):
    '''
    ArgumentFunction :  SetOf LParen RParen
                     |  SetOf LParen Wfts RParen
    '''
    if len(p) == 4:
        p[0] = []
    else:
        p[0] = p[3]

# ==============================================================================

def p_Wfts(p):
    '''
    Wfts :              Wft
         |              Wfts Comma Wft
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# ==============================================================================

def p_Arguments(p):
    '''
    Arguments :         Argument
              |         Arguments Comma Argument
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# ==============================================================================

def p_AtomicNameSet(p):
    '''
    AtomicNameSet :
                  |     Identifier
                  |     Integer
                  |     LBracket AtomicNames RBracket
    '''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[2]

# ==============================================================================

def p_AtomicNames(p):
    '''
    AtomicNames :       Identifier
                |       Integer
                |       AtomicNames Comma Identifier
                |       AtomicNames Comma Integer
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# ==============================================================================

# e.g. ind8
def p_VarNode(p):
    '''
    VarNode :           IndNode
            |           ArbNode
    '''
    if int(p[1][3:]) >= Arbitrary.counter:
        raise SNePSVarError('Invalid arb number. Max number: {}'.format(Arbitrary.counter - 1))
    p[0] = current_network.nodes[p[1]].get_unique_rep()

# ==============================================================================

# e.g. wft9
def p_Y_WftNode(p):
    '''
    Y_WftNode :         WftNode
    '''
    if int(p[1][3:]) >= Molecular.counter:
        raise SNePSVarError('Invalid wft number. Max number: {}'.format(Molecular.counter - 1))
    p[0] = current_network.nodes[p[1]].get_unique_rep()

# =====================================
# ------------- VAR RULES -------------
# =====================================

def p_CloseStmt(p):
    '''
    CloseStmt :         Close LParen AtomicNameSet Comma Wft RParen
    '''
    raise SNePSVarError("Close not yet implemented!")

def p_EveryStmt(p):
    '''
    EveryStmt :         Every LParen ArbVar Comma Argument RParen
    '''
    global variables
    global current_network

    # Stores variable and shorthand representation
    new_var = p[3][1]
    temp_var_name = p[3][0]

    # Representation of restrictions
    for restriction in p[5]:
        new_var.var_rep.add_restriction(restriction)

    # Checks if node already exists in network
    for node in current_network.nodes.values():
        if isinstance(node, Arbitrary) and node == new_var:
            new_var = node

    # Ensures variable name only used to refer to one object in wft
    if temp_var_name in variables and variables[temp_var_name] != new_var:
        raise SNePSVarError("Variable with name {} defined twice in same context!".format(new_var.name))

    # Stores in variable dictionary for second pass
    variables[temp_var_name] = new_var

def p_SomeStmt(p):
    '''
    SomeStmt :          Some LParen IndVar LParen AtomicNames RParen Comma Argument RParen
    '''
    global variables
    global current_network

    # Stores variable and shorthand representation
    new_var = p[3][1]
    temp_var_name = p[3][0]

    # Representation of dependencies
    for dependency_name in p[5]:
        located = False
        if dependency_name in variables:
            new_var.var_rep.add_dependency(variables[dependency_name])
        else:
            raise SNePSVarError("Restriction {} referrenced before variable creation!".format(dependency_name))

    # Representation of restrictions
    for restriction in p[8]:
        new_var.var_rep.add_restriction(restriction)

    # Checks if node already exists in network
    for node in current_network.nodes.values():
        if isinstance(node, Indefinite) and node == new_var:
            new_var = node

    # Ensures variable name only used to refer to one object in wft
    if temp_var_name in variables and variables[temp_var_name] != new_var:
        raise SNePSVarError("Variable with name {} defined twice in same context!".format(new_var.name))

    # Stores in variable dictionary for second pass
    variables[temp_var_name] = new_var

def p_ArbVar(p):
    '''
    ArbVar :            Identifier
           |            Integer
    '''
    # Returns a tuuple of the variable followed by a shorthand representation (e.g. "x")
    global current_network
    global var_names
    new_var = Arbitrary(p[1], current_network.sem_hierarchy.get_type('Entity'))
    var_names[p[1]] = new_var.get_unique_rep()
    p[0] = (p[1], new_var)


def p_IndVar(p):
    '''
    IndVar :            Identifier
           |            Integer
    '''
    # Returns a tuuple of the variable followed by a shorthand representation (e.g. "x")
    global current_network
    global var_names
    new_var = Indefinite(p[1], current_network.sem_hierarchy.get_type('Entity'))
    var_names[p[1]] = new_var.get_unique_rep()
    p[0] = (p[1], new_var)

def p_error(p):
    if p is None:
        raise SNePSVarError("Term reached end unexpectedly.")
    else:
        raise SNePSVarError("Syntax error on token '" + p.type + "'")

def p_AtomicName(p):
    '''
    AtomicName :        Identifier
               |        Integer
    '''
    global var_names
    if p[1] in var_names:
        p[0] = var_names[p[1]]
    else:
        p[0] = UniqueRep(name=p[1])

# =====================================
# ------------- GET FNS ---------------
# =====================================

def rep_molecular(caseframe_name, children_reps):
    """ Returns a UniqueRep object corresponding to the node """
    caseframe = current_network.find_caseframe(caseframe_name)
    name = caseframe.name
    return UniqueRep(caseframe_name=caseframe.name, children=children_reps)

def rep_thresh (caseframe_name, children_reps, min, max):
    """ Returns a UniqueRep object corresponding to the node """

    # Simplifies caseframes - See slide 439:
    # https://cse.buffalo.edu/~shapiro/Courses/CSE563/Slides/krrSlides.pdf
    if caseframe_name == 'thresh':
        num_nodes = len(children_reps[0])
        if min == 1 and max == num_nodes - 1:
            caseframe_name = 'iff'

    return UniqueRep(caseframe_name=caseframe_name, children=children_reps, min=min, max=max)

def rep_andor (caseframe_name, children_reps, min, max):
    """ Returns a UniqueRep object corresponding to the node """

    # Simplifies caseframes - See slide 437:
    # https://cse.buffalo.edu/~shapiro/Courses/CSE563/Slides/krrSlides.pdf
    if caseframe_name == 'andor':
        num_nodes = len(children_reps[0])
        if min == max == num_nodes:
            caseframe_name = 'and'
        elif min == 1 and max == num_nodes:
            caseframe_name = 'or'
        elif min == 0 and max == num_nodes - 1:
            caseframe_name = 'nand'
        elif min == max == 0:
            caseframe_name = 'nor'
        elif min == max == 1:
            caseframe_name = 'xor'
    return UniqueRep(caseframe_name=caseframe_name, children=children_reps, min=min, max=max)

def rep_impl(children_reps, bound):
    """ Returns a UniqueRep object corresponding to the node """
    return UniqueRep(caseframe_name='if', children=children_reps, bound=bound)

def unique_children(children):
    """ Returns a list of unique representations for children """
    unique_children = []
    for slot_group in children:
        unique_slot_group = []
        for filler in slot_group:
            located = False
            for unique_filler in unique_slot_group:
                if unique_filler.equivalent_structure(filler):
                    located = True
                    break
            if not located:
                unique_slot_group.append(filler)
        unique_children.append(unique_slot_group)
    return unique_children

# =====================================
# ----------- VARIABLE FN -------------
# =====================================

def get_vars(wft: str, network):
    """ Strips vars from a wft and ensures uniqueness,
    then returns a dictionary in which variable names correspond to their nodes. """

    global current_network
    current_network = network
    var_parser = yacc.yacc()

    # First pass on wft string
    var_parser.parse(wft, lexer=WftLex.wft_lexer)

    # Reset and return variables
    global variables
    ret_variables = variables
    variables = {}
    var_names = {}
    return ret_variables
