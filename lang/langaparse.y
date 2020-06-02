%token T_LParen 1
%token T_RParen 2
%token T_Impl 3
%token T_None 4
%token T_Integer 5
%token T_Identifier 6
%token T_And 7
%token T_Or 8
%token T_Not 9
%token T_Nor 10
%token T_Thnot 11
%token T_Thnor 12
%token T_Nand 13
%token T_Xor 14
%token T_Iff 15
%token T_AndOr 16
%token T_Thresh 17
%token T_SetOf 18
%token T_Every 19
%token T_Some 20
%token T_Close 21
%token T_WftNode 22
%token T_QIdentifier 23
%token T_String 24

%%

Wft:              atomicwft
  |               Y_WftNode
  |               T_LParen Function Arguments T_RParen
  |               T_LParen BinaryOp Argument Argument T_RParen
  |               T_LParen NaryOp Wfts T_RParen
  |               T_LParen Param2Op T_LParen Y_Integer Y_Integer T_RParen Wft Wfts T_RParen
  |               T_LParen Y_Thresh T_LParen Y_Integer T_RParen Wft Wfts T_RParen
  |               T_LParen Y_Close AtomicNameSet Wft T_RParen
  |               T_LParen Y_Every AtomicName Wfts T_RParen
  |               T_LParen Y_Some AtomicName T_LParen Wfts T_RParen Wfts T_RParen
  |               T_LParen T_QIdentifier Wfts T_RParen
;
BinaryOp:         Y_Impl
;
NaryOp:           Y_And | Y_Or | Y_Not | Y_Nor | Y_Thnot | Y_Thnor
  |               Y_Nand _ Y_Xor | Y_Iff
;
Param2Op:         Y_AndOr | Y_Thresh
;
AtomicWtf:        AtomicName | Y_String | Y_Integer
;
AtomicName:       Y_String
;
Function:         Wft
;
Argument:         Wft | T_None
  |               T_LParen ArgumentFunction Wfts T_RParen
;
ArgumentFunction: Y_SetOf
;
ReservedWord:     Y_Every | Y_Some | Y_Close |Y_QIdentifier
  |               BinaryOp | NaryOp | Param2Op
;
Wfts:
  |               Wfts Wft
;
Arguments:        Argument
  |               Arguments Argument
;
AtomicNameSet:    AtomicName
  |               T_LParen AtomicName AtomicNames T_RParen
;
AtomicNames:
  |               AtomicName AtomicNames
;
Y_String:         T_String;
Y_Integer:        T_Integer;
Y_Impl:           T_Impl;
Y_Or:             T_Or;
Y_Not:            T_Not;
Y_Nor:            T_Nor;
Y_Thnot:          T_Thnot;
Y_Thnor:          T_Thnor;
Y_Nand:           T_Nand;
Y_Xor:            T_Xor;
Y_Iff:            T_Iff;
Y_AndOr:          T_AndOr;
Y_Thresh:         T_Thresh;
Y_SetOf:          T_SetOf;
Y_Every:          T_Every;
Y_Some:           T_Some;
Y_Close:          T_Close;
Y_And:            T_And;
Y_WftNode:        T_WftNode;
Y_QIdentifier:    T_QIdentifier;
Y_OrImpl:         T_OrImpl;

%%
