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

precedence =  []

# -------------- RULES ----------------

def p_Wft(p):
    '''
    Wft:                atomicwft
        |               Y_WftNode
        |               LParen Function Arguments RParen
        |               LParen BinaryOp Argument Argument RParen
        |               LParen NaryOp Wfts RParen
        |               LParen Param2Op LParen Y_Integer Y_Integer RParen Wft Wfts RParen
        |               LParen Y_Thresh LParen Y_Integer RParen Wft Wfts RParen
        |               LParen Y_Close AtomicNameSet Wft RParen
        |               LParen Y_Every AtomicName Wfts RParen
        |               LParen Y_Some AtomicName LParen Wfts RParen Wfts RParen
        |               LParen QIdentifier Wfts RParen
    '''

def p_BinaryOp(p):
    '''
    BinaryOp:           Y_Impl
    '''

def p_NaryOp(p):
    '''
    NaryOp:             Y_And
          |             Y_Or
          |             Y_Not
          |             Y_Nor
          |             Y_Thnot
          |             Y_Thnor
          |             Y_Nand
          |             Y_Xor
          |             Y_Iff
    '''

def p_Param2Op(p):
    '''
    Param2Op:           Y_AndOr
            |           Y_Thresh
    '''

def p_AtomicWft(p):
    '''
    AtomicWft:          AtomicName
             |          Y_String
             |          Y_Integer
    '''

def p_AtomicName(p):
    '''
    AtomicName:         Y_String
    '''

def p_Function(p):
    '''
    Function:           Wft
    '''

def p_Argument(p):
    '''
    Argument:           Wft
            |           None
            |           LParen ArgumentFunction Wfts RParen
    '''

def p_ArgumentFunction(p):
    '''
    ArgumentFunction:   Y_SetOf
    '''

def p_ReservedWord(p):
    '''
    ReservedWord:       Y_Every
                |       Y_Some
                |       Y_Close
                |       Y_QIdentifier
                |       BinaryOp
                |       NaryOp
                |       Param2Op
    '''

def p_Wfts(p):
    '''
    Wfts:
        |               Wfts Wft
    '''

def p_Arguments(p):
    '''
    Arguments:          Argument
             |          Arguments Argument
    '''

def p_AtomicNameSet(p):
    '''
    AtomicNameSet:      AtomicName
                 |      LParen AtomicName AtomicNames RParen
    '''

def p_AtomicNames(p):
    '''
    AtomicNames:
               |        AtomicName AtomicNames
    '''

def p_Y_String(p):
    '''
    Y_String:           String
    '''

def p_Y_Integer(p):
    '''
    Y_Integer:          Integer
    '''

def p_Y_Impl(p):
    '''
    Y_Impl:             Impl
    '''

def p_Y_Or(p):
    '''
    Y_Or:               Or
    '''

def p_Y_Not(p):
    '''
    Y_Not:              Not
    '''

def p_Y_Nor(p):
    '''
    Y_Nor:              Nor
    '''

def p_Y_Thnot(p):
    '''
    Y_Thnot:            Thnot
    '''

def p_Y_Thnor(p):
    '''
    Y_Thnor:            Thnor
    '''

def p_Y_Nand(p):
    '''
    Y_Nand:             Nand
    '''

def p_Y_Xor(p):
    '''
    Y_Xor:              Xor
    '''

def p_Y_Iff(p):
    '''
    Y_Iff:              Iff
    '''

def p_Y_AndOr(p):
    '''
    Y_AndOr:            AndOr
    '''

def p_Y_Thresh(p):
    '''
    Y_Thresh:           Thresh
    '''

def p_Y_SetOf(p):
    '''
    Y_SetOf:            SetOf
    '''

def p_Y_Every(p):
    '''
    Y_Every:            Every
    '''

def p_Y_Some(p):
    '''
    Y_Some:             Some
    '''

def p_Y_Close(p):
    '''
    Y_Close:            Close
    '''

def p_Y_And(p):
    '''
    Y_And:              And
    '''

def p_Y_WftNode(p):
    '''
    Y_WftNode:          WftNode
    '''

def p_Y_QIdentifier(p):
    '''
    Y_QIdentifier:      QIdentifier
    '''

def p_Y_OrImpl(p):
    '''
    Y_OrImpl:           OrImpl
    '''

 def p_error(p):
     print("Syntax error in input!")

# -------------- RULES END ----------------

if __name__ == '__main__':
    from ply import *
    yacc.yacc()
