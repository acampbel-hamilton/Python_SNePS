from . import WftLex
from ..vars.WftVars import get_vars, SNePSVarError
from .ply import *
from ..Network import *
from ..Caseframe import Frame, Fillers
from ..Node import Base, Molecular, Indefinite, Arbitrary, ThreshNode, AndOrNode, ImplNode
from ..Error import SNError

class SNePSWftError(SNError):
    pass

current_network = None
tokens = WftLex.tokens

variables = {}
top_wft = None

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
    p[0] = build_impl(filler_set, int(p[1][:1]))
def p_BinaryOp2(p):
    '''
    BinaryOp :          AndImpl LParen Argument Comma Argument RParen
    '''
    filler_set = [p[3], p[5]]
    p[0] = build_impl(filler_set, len(p[3].nodes))
def p_BinaryOp3(p):
    '''
    BinaryOp :          SingImpl LParen Argument Comma Argument RParen
    '''
    filler_set = [p[3], p[5]]
    p[0] = build_impl(filler_set, 1)


# e.g. and(wft1, wft2)
def p_NaryOp1(p):
    '''
    NaryOp :            And LParen Wfts RParen
    '''
    filler_set = [Fillers(p[3])]
    p[0] = build_andor(p[1], filler_set, len(p[3]), len(p[3]))
def p_NaryOp2(p):
    '''
    NaryOp :            Or LParen Wfts RParen
    '''
    filler_set = [Fillers(p[3])]
    p[0] = build_andor(p[1], filler_set, 1, len(p[3]))
def p_NaryOp3(p):
    '''
    NaryOp :            Not LParen Wfts RParen
           |            Nor LParen Wfts RParen
    '''
    filler_set = [Fillers(p[3])]
    p[0] = build_andor(p[1], filler_set, 0, 0)
def p_NaryOp4(p):
    '''
    NaryOp :            Nand LParen Wfts RParen
    '''
    filler_set = [Fillers(p[3])]
    p[0] = build_andor(p[1], filler_set, 0, len(p[3]) - 1)
def p_NaryOp5(p):
    '''
    NaryOp :            Xor LParen Wfts RParen
    '''
    filler_set = [Fillers(p[3])]
    p[0] = build_andor(p[1], filler_set, 1, 1)
def p_NaryOp6(p):
    '''
    NaryOp :            Iff LParen Wfts RParen
           |            DoubImpl LParen Wfts RParen
    '''
    filler_set = [Fillers(p[3])]
    p[0] = build_thresh("iff", filler_set, 1, len(p[3]) - 1)
def p_NaryOp7(p):
    '''
    NaryOp :            Thnot LParen Wfts RParen
           |            Thnor LParen Wfts RParen
    '''
    raise SNePSWftError("Not yet implemented!")

# e.g. thresh{1, 2}(wft1)
def p_MinMaxOp(p):
    '''
    MinMaxOp :          AndOr LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer RBrace LParen Wfts RParen
    '''
    min = int(p[3])
    if len(p) == 8:
        filler_set = [Fillers(p[6])]
        max = len(p[6]) - 1
    else:
        max = int(p[5])
        filler_set = [Fillers(p[8])]
    if p[1] == "thresh":
        p[0] = build_thresh(p[1], filler_set, min, max)
    else:
        p[0] = build_andor(p[1], filler_set, min, max)

# e.g. every{x}(Isa(x, Dog))
def p_EveryStmt(p):
    '''
    EveryStmt :         Every LParen Var Comma Argument RParen
    '''
    global variables
    arb = p[3]
    if not isinstance(arb, Arbitrary):
        raise SNePSVarError("Variable {} is not arbefinite!".format(arb.name))

    # # Add restrictions
    # for node in p[8].nodes:
    #     new_restriction(arb, node)

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
    if not isinstance(ind, Indefinite):
        raise SNePSVarError("Variable {} is not indefinite!".format(ind.name))

    # # Add dependencies
    # # TODO
    # for var_name in p[5]:
    #     if var_name not in variables:
    #         raise SNePSVarError("Variable \"{}\" does not exist".format(var_name))
    #     if variables[var_name] is ind:
    #         raise SNePSVarError("Variables cannot depend on themselves".format(var_name))
    #     ind.add_dependency(variables[var_name])
    #
    # # Add restrictions
    # for node in p[8].nodes:
    #     new_restriction(ind, node)

    # Store in network
    ind.store_in(current_network)
    p[0] = ind

def p_Var(p):
    '''
    Var :               Identifier
        |               Integer
    '''
    # Grabs from variable dictionary
    global variables
    p[0] = variables[p[1]]

# e.g. close(Dog, wft1)
def p_CloseStmt(p):
    '''
    CloseStmt :         Close LParen AtomicNameSet Comma Wft RParen
    '''
    raise SNePSWftError("Not yet implemented!")

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
    raise SNePSWftError("Not yet implemented!")

# e.g. wft1
def p_Argument1(p):
    '''
    Argument :          Wft
    '''
    p[0] = Fillers([p[1]])

# e.g. None
def p_Argument2(p):
    '''
    Argument :          None
    '''
    p[0] = Fillers()

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
        p[0] = Fillers()
    else:
        p[0] = Fillers(p[2])

def p_ArgumentFunction(p):
    '''
    ArgumentFunction :  SetOf LParen RParen
        |               SetOf LParen Wfts RParen
    '''
    if len(p) == 4:
        p[0] = Fillers()
    else:
        p[0] = Fillers(p[3])

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
    if p[1] in variables:
        p[0] = variables[p[1]]
    else:
        current_network.define_term(p[1])
        p[0] = current_network.find_term(p[1])

def p_Y_WftNode(p):
    '''
    Y_WftNode :         WftNode
    '''
    if int(p[1][3:]) >= Molecular.counter:
        raise SNePSWftError('Invalid wft number. Max number: {}'.format(Molecular.counter - 1))

    p[0] = current_network.nodes[p[1]]

def p_VarNode1(p):
    '''
    VarNode :           IndNode
    '''
    if int(p[1][3:]) >= Indefinite.counter:
        raise SNePSWftError('Invalid ind number. Max number: {}'.format(Indefinite.counter - 1))
    p[0] = current_network.nodes[p[1]]
def p_VarNode2(p):
    '''
    VarNode :           ArbNode
    '''
    if int(p[1][3:]) >= Arbitrary.counter:
        raise SNePSWftError('Invalid arb number. Max number: {}'.format(Arbitrary.counter - 1))
    p[0] = current_network.nodes[p[1]]

def p_error(p):
    if p is None:
        raise SNePSWftError("Term reached end unexpectedly.")
    else:
        raise SNePSWftError("Syntax error on token '" + p.type + "'")

# =====================================
# ------------ BUILD FNS --------------
# =====================================

def build_molecular(caseframe_name, filler_set):
    """ Builds and returns (or simply returns) a Molecular node from given parameters """
    caseframe = current_network.find_caseframe(caseframe_name)
    frame = Frame(caseframe, filler_set)
    for node in current_network.nodes.values():
        if node.has_frame(frame):
            return node
    wftNode = Molecular(frame)
    current_network.nodes[wftNode.name] = wftNode
    return wftNode

def build_thresh (caseframe_name, filler_set, min, max):
    """ Builds and returns (or simply returns) a thresh node from given parameters """

    # Simplifies caseframes - See slide 439:
    # https://cse.buffalo.edu/~shapiro/Courses/CSE563/Slides/krrSlides.pdf
    if caseframe_name == 'thresh':
        num_nodes = len(filler_set[0])
        if min == 1 and max == num_nodes - 1:
            caseframe_name = 'iff'

    caseframe = current_network.find_caseframe(caseframe_name)
    frame = Frame(caseframe, filler_set)
    for node in current_network.nodes.values():
        if node.has_frame(frame) and node.has_min_max(min, max):
            return node
    wftNode = ThreshNode(frame, min, max)
    current_network.nodes[wftNode.name] = wftNode
    return wftNode

def build_andor (caseframe_name, filler_set, min, max):
    """ Builds and returns (or simply returns) an andor node from given parameters """

    # Simplifies caseframes - See slide 437:
    # https://cse.buffalo.edu/~shapiro/Courses/CSE563/Slides/krrSlides.pdf
    if caseframe_name == 'andor':
        num_nodes = len(filler_set[0])
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

    caseframe = current_network.find_caseframe(caseframe_name)
    frame = Frame(caseframe, filler_set)
    for node in current_network.nodes.values():
        if node.has_frame(frame) and node.has_min_max(min, max):
            return node
    wftNode = AndOrNode(frame, min, max)
    current_network.nodes[wftNode.name] = wftNode
    return wftNode

def build_impl(filler_set, bound):
    """ Builds and returns (or simply returns) an impl node from given parameters """
    caseframe = current_network.find_caseframe("if")
    frame = Frame(caseframe, filler_set)
    for node in current_network.nodes.values():
        if node.has_frame(frame) and node.has_bound(bound):
            return node
    wftNode = ImplNode(frame, bound)
    current_network.nodes[wftNode.name] = wftNode
    return wftNode

def new_restriction(variable, restriction):
    """ Adds a restriction to a variable if it is valid """
    if restriction is variable:
        raise SNePSWftError("Variables cannot be restricted on themselves")
    if not restriction.has_constituent(variable):
        raise SNePSWftError("{} used as a restriction, but does not reference variable".format(variable.name))
    variable.add_restriction(restriction)
    current_network.current_context.add_hypothesis(restriction)

# =====================================
# ------------ PARSER FN --------------
# =====================================

def wft_parser(wft : str, network):
    global current_network
    current_network = network

    yacc.yacc()
    if wft != '':
        try:
            # Store variables in array indexed by names
            global variables
            variables = get_vars(wft, network)

            # Parse and store wft created by string (as opposed to sub-wfts it might create)
            yacc.parse(wft)
            global top_wft
            ret_top_wft = top_wft

            # Reset globals and return the wft
            top_wft = None
            variables = {}
            return (ret_top_wft)

        # Error messages
        except SNError as e:
            if type(e) is not SNePSWftError and type(e) is not SNePSVarError:
                print("PARSING FAILED:\n\t", end='')
            else:
                print("PARSING FAILED: ", end='')
            print(e)
