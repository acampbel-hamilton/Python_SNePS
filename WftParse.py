from . import WftLex
from .ply import *
from .Network import *

current_network = None
tokens = WftLex.tokens

# =====================================
# -------------- RULES ----------------
# =====================================

def p_Wft(p):
    '''
    Wft :               FWft
        |               OWft
    '''

# Function-eligible wfts (Can serve as entities)
# e.g. wft1
def p_FWft(p):
    '''
    FWft :              AtomicName
         |              WftNode
         |              Function
    '''

# All other wfts
# e.g. if(wft1, wft2)
def p_OWft(p):
    '''
    OWft :              BinaryOp
         |              NaryOp
         |              Param2Op
         |              CloseStmt
         |              EveryStmt
         |              SomeStmt
         |              QIdenStmt
    '''

# e.g. if(wft1, wft2)
def p_BinaryOp(p):
    '''
    BinaryOp :          Impl LParen Argument Comma Argument RParen
             |          OrImpl LParen Argument Comma Argument RParen
             |          AndImpl LParen Argument Comma Argument RParen
    '''
    p[1].add_children(p[3], p[5])
    p[0] = p[1]

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
           |            And LParen RParen
           |            Or LParen RParen
           |            Not LParen RParen
           |            Nor LParen RParen
           |            Thnot LParen RParen
           |            Thnor LParen RParen
           |            Nand LParen RParen
           |            Xor LParen RParen
           |            DoubImpl LParen RParen
    '''
    

# e.g. thresh{1, 2}(wft1)
def p_MinMaxOp(p):
    '''
    MinMaxOp :          AndOr LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Thresh LBrace Integer RBrace LParen Wfts RParen
    '''
    p[1].description = '<' + p[3] + ', ' + p[5] + '>'
    p[1].add_children(*p[8])
    p[0] = p[1]

# e.g. every{x}(Isa(x, Dog))
def p_EveryStmt(p):
    '''
    EveryStmt :         Every LBrace AtomicName RBrace LParen Wfts RParen
              |         Every LBrace AtomicName RBrace LParen RParen
    '''
    p[1].add_children(p[3])
    if len(p) == 8:
        wftTree = ParseTree(description="wfts")
        wftTree.add_children(*p[6])
        p[1].add_children(wftTree)
    p[0] = p[1]

# e.g. some{x(y)}(Isa(x, y))
def p_SomeStmt(p):
    '''
    SomeStmt :          Some LBrace AtomicName LParen AtomicName RParen RBrace LParen Wfts RParen
             |          Some LBrace AtomicName LParen AtomicName RParen RBrace LParen RParen
    '''
    p[1].add_children(p[3], p[5])
    if len(p) == 11:
        wftTree = ParseTree(description="wfts")
        wftTree.add_children(*p[9])
        p[1].add_children(wftTree)
    p[0] = p[1]

# e.g. close(Dog, wft1)
def p_CloseStmt(p):
    '''
    CloseStmt :         Close LParen AtomicNameSet Comma Wft RParen
    '''
    p[1].add_children(p[3], p[5])
    p[0] = p[1]

# e.g. brothers(Tom, Ted)
def p_Function(p):
    '''
    Function :          FWft LParen Arguments RParen
    '''
    argsTree = ParseTree(description="args")
    argsTree.add_children(*p[3])
    p[0] = ParseTree(description="Function")
    p[0].add_children(p[1], argsTree)

# e.g. ?example()
def p_QIdenStmt(p):
    '''
    QIdenStmt :         QIdentifier LParen Wfts RParen
              |         QIdentifier LParen RParen
    '''
    if len(p) == 5:
        p[1].add_children(*p[3])
    p[0] = p[1]

# e.g. setOf(wft1, wft2)
def p_Argument(p):
    '''
    Argument :          Wft
             |          None
             |          ArgumentFunction
             |          LBracket Wfts RBracket
             |          LBracket RBracket
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ParseTree(description="Argument")
        setTree = ParseTree(description="SetOf", value="setOf")
        p[0].add_children(setTree)
        if len(p) == 4:
            wftTree = ParseTree(description="wfts")
            wftTree.add_children(*p[2])
            p[0].add_children(wftTree)

def p_ArgumentFunction(p):
    '''
    ArgumentFunction :  SetOf LParen Wfts RParen
        |               SetOf LParen RParen
    '''
    p[0] = ParseTree(description="Argument")
    p[0].add_children(p[1])
    if len(p) == 5:
        wftTree = ParseTree(description="wfts")
        wftTree.add_children(*p[3])
        p[0].add_children(wftTree)

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
    AtomicNameSet :     AtomicName
                  |     LParen AtomicNames RParen
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ParseTree(description="AtomicNameSet")
        p[0].add_children(*p[3])

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
    current_network.define_term(p[1])
    p[0] = current_network.find_term(p[1])

def p_error(p):
    raise Exception("Syntax error on token '" + p.type + "'")

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
        except Exception as e:
            print(e)
