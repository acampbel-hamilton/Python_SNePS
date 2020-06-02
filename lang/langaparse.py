tokens =  ['T_LParen', 'T_RParen', 'T_Impl', 'T_None', 'T_Integer', 'T_Identifier', 'T_And', 'T_Or', 'T_Not', 'T_Nor', 'T_Thnot', 'T_Thnor', 'T_Nand', 'T_Xor', 'T_Iff', 'T_AndOr', 'T_Thresh', 'T_SetOf', 'T_Every', 'T_Some', 'T_Close', 'T_WftNode', 'T_QIdentifier', 'T_String']

precedence =  []

# -------------- RULES ----------------

def p_Wft(p):
    '''
    Wft :           atomicwft
        |           Y_WftNode
        |           T_LParen Function Arguments T_RParen
        |           T_LParen BinaryOp Argument Argument T_RParen
        |           T_LParen NaryOp Wfts T_RParen
        |           T_LParen Param2Op T_LParen Y_Integer Y_Integer T_RParen Wft Wfts T_RParen
        |           T_LParen Y_Thresh T_LParen Y_Integer T_RParen Wft Wfts T_RParen
        |           T_LParen Y_Close AtomicNameSet Wft T_RParen
        |           Wft : T_LParen Y_Every AtomicName Wfts T_RParen
        |           T_LParen Y_Some AtomicName T_LParen Wfts T_RParen Wfts T_RParen
        |           T_LParen T_QIdentifier Wfts T_RParen
    '''

def p_BinaryOp(p):
    '''
    BinaryOp :   Y_Impl
    '''

def p_NaryOp(p):
    '''
    NaryOp :        Y_And
        |           Y_Or
        |           Y_Not
        |           Y_Nor
        |           Y_Thnot
        |           Y_Thnor
        |           Y_Nand _ Y_Xor
        |           Y_Iff
    '''

def p_Param2Op(p):
    '''
    Param2Op:       Y_AndOr
        |           Y_Thresh
    '''

def p_AtomicWtf(p):
    '''
    AtomicWtf:      AtomicName
        |           Y_String
        |           Y_Integer
    '''

def p_AtomicName(p):
    '''
    AtomicName:     Y_String
    '''

def p_Function(p):
    '''
    Function:       Wft
    '''

def p_Argument(p):
    '''
    Argument:       Wft
        |           T_None
        |           T_LParen ArgumentFunction Wfts T_RParen
    '''

def p_ArgumentFunction(p):
    '''
    ArgumentFunction: Y_SetOf
    '''

def p_ReservedWord(p):
    '''
    ReservedWord:   Y_Every
        |           Y_Some
        |           Y_Close
        |           Y_QIdentifier
        |           BinaryOp
        |           NaryOp
        |           Param2Op
    '''

def p_Wfts(p):
    '''
    Wfts:
        |           Wfts Wft
    '''

def p_Arguments(p):
    '''
    Arguments:      Argument
        |           Arguments Argument
    '''

def p_AtomicNameSet(p):
    '''
    AtomicNameSet : AtomicName
        |           T_LParen AtomicName AtomicNames T_RParen
    '''

def p_AtomicNames(p):
    '''
    AtomicNames :
        | AtomicName AtomicNames
    '''

def p_Y_String(p):
    '''
    Y_String : T_String
    '''

def p_Y_Integer(p):
    '''
    Y_Integer : T_Integer
    '''

def p_Y_Impl(p):
    '''
    Y_Impl : T_Impl
    '''

def p_Y_Or(p):
    '''
    Y_Or : T_Or
    '''

def p_Y_Not(p):
    '''
    Y_Not : T_Not
    '''

def p_Y_Nor(p):
    '''
    Y_Nor : T_Nor
    '''

def p_Y_Thnot(p):
    '''
    Y_Thnot : T_Thnot
    '''

def p_Y_Thnor(p):
    '''
    Y_Thnor : T_Thnor
    '''

def p_Y_Nand(p):
    '''
    Y_Nand : T_Nand
    '''

def p_Y_Xor(p):
    '''
    Y_Xor : T_Xor
    '''

def p_Y_Iff(p):
    '''
    Y_Iff : T_Iff
    '''

def p_Y_AndOr(p):
    '''
    Y_AndOr : T_AndOr
    '''

def p_Y_Thresh(p):
    '''
    Y_Thresh : T_Thresh
    '''

def p_Y_SetOf(p):
    '''
    Y_SetOf : T_SetOf
    '''

def p_Y_Every(p):
    '''
    Y_Every : T_Every
    '''

def p_Y_Some(p):
    '''
    Y_Some : T_Some
    '''

def p_Y_Close(p):
    '''
    Y_Close : T_Close
    '''

def p_Y_And(p):
    '''
    Y_And : T_And
    '''

def p_Y_WftNode(p):
    '''
    Y_WftNode : T_WftNode
    '''

def p_Y_QIdentifier(p):
    '''
    Y_QIdentifier : T_QIdentifier
    '''

def p_Y_OrImpl(p):
    '''
    Y_OrImpl : T_OrImpl
    '''

# -------------- RULES END ----------------

if __name__ == '__main__':
    from ply import *
    yacc.yacc()
