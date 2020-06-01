%token T_LParen
%token T_RParen
%token T_Impl
%token T_DoubImpl
%token T_Integer
%token T_String
%token T_And
%token T_Or
%token T_Not
%token T_Nor
%token T_Thnot
%token T_Thnor
%token T_Nand
%token T_Xor
%token T_Iff
%token T_AndOr
%token T_Thresh
%token T_SetOf
%token T_Every
%token T_Some
%token T_Close

%%

Wft:  atomicwft
  |   T_LParen Function Arguments T_RParen
  |   T_LParen BinaryOp Argument Argument T_RParen
  |   T_LParen NaryOp Wfts T_RParen
  |   T_LParen Param2Op T_LParen T_RParen T_RParen
  |

Y_Impl: T_Impl { $$ = new ParseTree(myTok); }
Y_DoubImpl: T_DoubImpl { $$ = new ParseTree(myTok); }
Y_Or: T_Or { $$ = new ParseTree(myTok); }
Y_Not: T_Not { $$ = new ParseTree(myTok); }
Y_Nor: T_Nor { $$ = new ParseTree(myTok); }
Y_Thnot: T_Thnot { $$ = new ParseTree(myTok); }
Y_Thnor: T_Thnor { $$ = new ParseTree(myTok); }
Y_Nand: T_Nand { $$ = new ParseTree(myTok); }
Y_Xor: T_Xor { $$ = new ParseTree(myTok); }
Y_Iff: T_Iff { $$ = new ParseTree(myTok); }
Y_AndOr: T_AndOr { $$ = new ParseTree(myTok); }
Y_Thresh: T_Thresh { $$ = new ParseTree(myTok); }
Y_SetOf: T_SetOf { $$ = new ParseTree(myTok); }
Y_Every: T_Every { $$ = new ParseTree(myTok); }
Y_Some: T_Some { $$ = new ParseTree(myTok); }
Y_Close: T_Close { $$ = new ParseTree(myTok); }
Y_And: T_And { $$ = new ParseTree(myTok); }

%%

int yyerror(const char * s)
{
  fprintf(stderr, "%s\n", s);
  return 0;
}
