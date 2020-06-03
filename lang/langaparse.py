import langalex
from langAInterpreter import * # For ParseTree

tokens =  (
    'Xor',
    'Or',
    'And',
    'Thresh',
    'Thnor',
    'Thnot',
    'AndOr',
    'SetOf',
    'Some',
    'Every',
    'Nand',
    'Nor',
    'None',
    'Not',
    'Close',
    'LParen',
    'RParen',
    'WftNode',
    'Impl',
    'DoubImpl',
    'Integer',
    'QIdentifier',
    'String',
    'Identifier'
)

# Contains root of ParseTree
top = None

# -------------- RULES ----------------

def p_Wft1(p):
    '''
    Wft :               AtomicWft
        |               Y_WftNode
    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[1])
    global top
    top = p[0]

def p_Wft2(p):
    '''
    Wft  :               LParen Function Arguments RParen
    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[2], *p[3])
    global top
    top = p[0]

def p_Wft3(p):
    '''
    Wft  :              LParen BinaryOp Argument Argument RParen
    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[2], p[3], p[4])
    global top
    top = p[0]

def p_Wft4(p):
    '''
    Wft :               LParen NaryOp Wfts RParen
    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[2], *p[3])
    global top
    top = p[0]

def p_Wft5(p):
    '''
    Wft :               LParen Param2Op Wft Wfts RParen
        |               LParen Param1Op Wft Wfts RParen
    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[2], p[3], *p[4])
    global top
    top = p[0]

def p_Wft6(p):
    '''
    Wft :               LParen Y_Close AtomicNameSet Wft RParen
    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[2], *p[3], p[4])
    global top
    top = p[0]

def p_Wft7(p):
    '''
    Wft :               LParen Y_Every AtomicName Wfts RParen
    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[2], p[3], *p[4])
    global top
    top = p[0]

def p_Wft8(p):
    '''
    Wft :               LParen SomeCondition Wfts RParen
        |               LParen QIdentifier Wfts RParen
    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[2], *p[3])
    global top
    top = p[0]

def p_BinaryOp(p):
    '''
    BinaryOp :          Y_Impl
    '''
    p[0] = p[1]

def p_NaryOp(p):
    '''
    NaryOp :            Y_And
          |             Y_Or
          |             Y_Not
          |             Y_Nor
          |             Y_Thnot
          |             Y_Thnor
          |             Y_Nand
          |             Y_Xor
          |             Y_DoubImpl
    '''
    p[0] = p[1]

def p_Param2Op(p):
    '''
    Param2Op :          Y_AndOr LParen Y_Integer Y_Integer RParen
            |           Y_Thresh LParen Y_Integer Y_Integer RParen
    '''
    p[0] = ParseTree(description="operator")
    p[0].add_children(p[1], p[3], p[4])

def p_Param1Op(p):
    '''
    Param1Op :          Y_Thresh LParen Y_Integer RParen
    '''
    p[0] = ParseTree(description="operator")
    p[0].add_children(p[1], p[3])

def p_AtomicWft(p):
    '''
    AtomicWft :         AtomicName
             |          Y_String
             |          Y_Integer
    '''
    p[0] = p[1]

def p_AtomicName(p):
    '''
    AtomicName  :        Y_Identifier
    '''
    p[0] = ParseTree(description="Atom")
    p[0].add_children(p[1])

def p_Function(p):
    '''
    Function :          Wft
    '''
    p[0] = ParseTree(description="Function")
    p[0].add_children(p[1])

def p_Argument(p):
    '''
    Argument :          Wft
            |           None
            |           LParen ArgumentFunction Wfts RParen
    '''
    if len(p) == 2:
        p[0] = ParseTree(description="Argument")
        p[0].add_children(p[1])
    else:
        p[0] = ParseTree(description="Argument")
        p[0].add_children(p[2], *p[3])

def p_ArgumentFunction(p):
    '''
    ArgumentFunction :  Y_SetOf
    '''
    p[0] = p[1]

def p_Wfts(p):
    '''
    Wfts :
        |               Wfts Wft
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_Arguments(p):
    '''
    Arguments :         Argument
        |               Arguments Argument
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_AtomicNameSet(p):
    '''
    AtomicNameSet :     AtomicName
        |               LParen AtomicName AtomicNames RParen
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ParseTree(description="AtomicNameSet")
        p[0].add_children(p[2], *p[3])

def p_AtomicNames(p):
    '''
    AtomicNames :
        |               AtomicName AtomicNames
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_SomeCondition(p):
    '''
    SomeCondition :     Y_Some AtomicName LParen Wfts RParen
    '''
    p[0] = ParseTree(description="Some")
    p[0].add_children(p[1], p[2], *p[4])

def p_Y_String(p):
    '''Y_String : String'''
    p[0] = ParseTree(description="String", value=p[1])

def p_Y_Integer(p):
    '''Y_Integer : Integer'''
    p[0] = ParseTree(description="Integer", value=p[1])

def p_Y_Impl(p):
    '''Y_Impl : Impl'''
    p[0] = ParseTree(description="Implication", value=p[1])

def p_Y_Or(p):
    '''Y_Or : Or'''
    p[0] = ParseTree(description="Or", value=p[1])

def p_Y_Not(p):
    '''Y_Not : Not'''
    p[0] = ParseTree(description="Not", value=p[1])

def p_Y_Nor(p):
    '''Y_Nor : Nor'''
    p[0] = ParseTree(description="Nor", value=p[1])

def p_Y_Thnot(p):
    '''Y_Thnot : Thnot'''
    p[0] = ParseTree(description="Thnot", value=p[1])

def p_Y_Thnor(p):
    '''Y_Thnor : Thnor'''
    p[0] = ParseTree(description="Thnor", value=p[1])

def p_Y_Nand(p):
    '''Y_Nand : Nand'''
    p[0] = ParseTree(description="Nand", value=p[1])

def p_Y_Xor(p):
    '''Y_Xor : Xor'''
    p[0] = ParseTree(description="Xor", value=p[1])

def p_Y_DoubImpl(p):
    '''Y_DoubImpl : DoubImpl'''
    p[0] = ParseTree(description="DoubImpl", value=p[1])

def p_Y_AndOr(p):
    '''Y_AndOr : AndOr'''
    p[0] = ParseTree(description="AndOr", value=p[1])

def p_Y_Thresh(p):
    '''Y_Thresh : Thresh'''
    p[0] = ParseTree(description="Thresh", value=p[1])

def p_Y_SetOf(p):
    '''Y_SetOf : SetOf'''
    p[0] = ParseTree(description="String", value=p[1])

def p_Y_Every(p):
    '''Y_Every : Every'''
    p[0] = ParseTree(description="Every", value=p[1])

def p_Y_Some(p):
    '''Y_Some : Some'''
    p[0] = ParseTree(description="Some", value=p[1])

def p_Y_Close(p):
    '''Y_Close : Close'''
    p[0] = ParseTree(description="Close", value=p[1])

def p_Y_And(p):
    '''Y_And : And'''
    p[0] = ParseTree(description="And", value=p[1])

def p_Y_WftNode(p):
    '''Y_WftNode : WftNode'''
    p[0] = ParseTree(description="WftNode", value=p[1])

def p_Y_QIdentifier(p):
    '''Y_QIdentifier : QIdentifier'''
    p[0] = ParseTree(description="QIdentifier", value=p[1])

def p_Y_Identifier(p):
    '''Y_Identifier : Identifier'''
    p[0] = ParseTree(description="Identifier", value=p[1])

def p_error(p):
    print("Syntax error in input!")

# -------------- RULES END ----------------

if __name__ == '__main__':
    from ply import *
    yacc.yacc()
    s = input('John')
    yacc.parse(s)
    top.to_networkx()
    return
