from . import WftLex
from .ply import *
from .Network import *
from .Caseframe import Frame, Fillers
from .Node import Base, Molecular, Indefinite, Arbitrary, MinMaxOp

current_network = None
tokens = WftLex.tokens

# =====================================
# -------------- RULES ----------------
# =====================================

class SNePSSyntaxError(SyntaxError):
    pass

def p_Wft(p):
    '''
    Wft :               FWft
        |               OWft
    '''
    p[0] = p[1]

# Function-eligible wfts (Can serve as entities)
# e.g. wft1
def p_FWft(p):
    '''
    FWft :              AtomicName
         |              WftNode
         |              Function
    '''
    p[0] = p[1]

# All other wfts
# e.g. if(wft1, wft2)
def p_OWft(p):
    '''
    OWft :              BinaryOp
         |              NaryOp
         |              MinMaxOp
         |              CloseStmt
         |              EveryStmt
         |              SomeStmt
         |              QIdenStmt
    '''
    p[0] = p[1]

# e.g. if(wft1, wft2)
def p_BinaryOp(p):
    '''
    BinaryOp :          Impl LParen Argument Comma Argument RParen
             |          OrImpl LParen Argument Comma Argument RParen
             |          AndImpl LParen Argument Comma Argument RParen
    '''


# e.g. and(wft1, wft2)
def p_NaryOp(p):
    '''
    NaryOp :            And LParen Wfts RParen
           |            Or LParen Wfts RParen
           |            Not LParen Wfts RParen
           |            Nor LParen Wfts RParen
           |            Thnot LParen Wfts RParen
           |            Thnor LParen Wfts RParen
           |            Nand LParen Wfts RParen
           |            Xor LParen Wfts RParen
           |            DoubImpl LParen Wfts RParen
    '''
    caseframe = current_network.find_caseframe(p[1])
    fillers = Fillers(p[3])
    frame = Frame(caseframe, [fillers])
    for node in current_network.nodes.values():
        if node.has_frame(frame):
            p[0] = node
            return
    wftNode = Molecular(current_network.sem_hierarchy.get_type("Proposition"))
    wftNode.add_down_cables(frame)
    current_network.nodes[wftNode.name] = wftNode
    p[0] = wftNode

# e.g. thresh{1, 2}(wft1)
def p_MinMaxOp(p):
    '''
    MinMaxOp :          AndOr LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer RBrace LParen Wfts RParen
    '''


# e.g. every{x}(Isa(x, Dog))
def p_EveryStmt(p):
    '''
    EveryStmt :         Every LBrace AtomicName RBrace LParen Wfts RParen
              |         Every LBrace AtomicName RBrace LParen RParen
    '''


# e.g. some{x(y)}(Isa(x, y))
def p_SomeStmt(p):
    '''
    SomeStmt :          Some LBrace AtomicName LParen AtomicName RParen RBrace LParen Wfts RParen
             |          Some LBrace AtomicName LParen AtomicName RParen RBrace LParen RParen
    '''


# e.g. close(Dog, wft1)
def p_CloseStmt(p):
    '''
    CloseStmt :         Close LParen AtomicNameSet Comma Wft RParen
    '''


# e.g. brothers(Tom, Ted)
def p_Function(p):
    '''
    Function :          FWft LParen Arguments RParen
    '''


# e.g. ?example()
def p_QIdenStmt(p):
    '''
    QIdenStmt :         QIdentifier LParen Wfts RParen
              |         QIdentifier LParen RParen
    '''


# e.g. setOf(wft1, wft2)
def p_Argument(p):
    '''
    Argument :          Wft
             |          None
             |          ArgumentFunction
             |          LBracket Wfts RBracket
             |          LBracket RBracket
    '''


def p_ArgumentFunction(p):
    '''
    ArgumentFunction :  SetOf LParen Wfts RParen
        |               SetOf LParen RParen
    '''


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


def p_AtomicNameSet(p):
    '''
    AtomicNameSet :     AtomicName
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
    current_network.define_term(p[1], sem_type_name="Proposition")
    p[0] = current_network.find_term(p[1])
from .Node import Base, Molecular, Indefinite

def p_error(p):
    raise SNePSSyntaxError("Syntax error on token '" + p.type + "'")

# =====================================
# ------------ RULES END --------------
# =====================================

def wft_parser(wft, network):
    global current_network
    current_network = network
    yacc.yacc()
    if wft != '':
        try:
            yacc.parse(wft)
        except SNePSSyntaxError as e:
            print(e)
