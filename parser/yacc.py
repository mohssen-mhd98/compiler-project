from ply import yacc
from lexer import Lexer


class Parser:

    tokens = Lexer().tokens

    def __init__(self):
        pass

    def p_program(self, p):
        """program : declist MAIN LRB RRB block"""
        print("program : declist MAIN LRB RRB block")

    def p_program1(self, p):
        """program : MAIN LRB RRB block"""
        print('program : MAIN LRB RRB block')

    def p_declist_decdeclist1(self, p):
        """declist : dec declist1"""
        print('declist : dec declist1')

    def p_declist_dec(self, p):
        """declist : dec"""
        print('declist : dec')

    def p_declist1_declist1(self, p):
        """declist1 : dec declist1"""
        print('declist1 : dec declist1')

    def p_declist1_dec(self, p):
        """declist1 : dec"""
        print('declist1 : dec')

    def p_dec_vardec(self, p):
        """dec : vardec"""
        print('dec : vardec')

    def p_dec_funcdec(self, p):
        """dec : funcdec"""
        print('dec : funcdec')

    def p_type_int(self, p):
        """type : INTEGER"""
        print('type : INTEGER')

    def p_type_float(self, p):
        """type : FLOAT"""
        print('type : FLOAT')

    def p_type_bool(self, p):
        """type : BOOLEAN"""
        print('type : BOOLEAN')

    def p_iddec_id(self, p):
        """iddec : ID"""
        print('iddec : ID')

    def p_iddec_idexp(self, p):
        """iddec : ID LSB exp RSB"""
        print('iddec : ID LSB exp RSB')

    def p_iddec_idAexp(self, p):
        """iddec : ID ASSIGN exp"""
        print('iddec : ID ASSIGN exp')

    def p_idlist_idlist1(self, p):
        """idlist : iddec idlist1"""
        print('idlist : iddec idlist1')

    def p_idlist1_iddec(self, p):
        """idlist1 : """
        print('idlist1 : ')

    def p_idlist1_idlist1(self, p):
        """idlist1 : COMMA iddec idlist1"""
        print('idlist1 : COMMA iddec idlist1')

    def p_vardec(self, p):
        """vardec : type idlist SEMICOLON"""
        print('vardec : type idlist SEMICOLON')

    def p_funcdec_type(self, p):
        """funcdec : type ID LRB paramdecs RRB block"""
        print('funcdec : type ID LRB paramdecs RRB block')

    def p_funcdec_id(self, p):
        """funcdec : VOID ID LRB paramdecs RRB block"""
        print('funcdec : VOID ID LRB paramdecs RRB block')

    def p_paramdecs_plist(self, p):
        """paramdecs : paramdecslist"""
        print('paramdecs : paramdecslist')

    def p_paramdecs_lambda(self, p):
        """paramdecs : """
        print('paramdecs : ')

    def p_paramdecslist_paramdeclist1(self, p):
        """paramdecslist : paramdec paramdecslist1"""
        print('paramdecslist : paramdec paramdecslist1')

    def p_paramdecslist1_paramdeclist1(self, p):
        """paramdecslist1 : COMMA paramdec paramdecslist1"""
        print('paramdecslist1 : COMMA paramdec paramdecslist1')

    def p_paramdecslist1_lambda(self, p):
        """paramdecslist1 : """
        print('paramdecslist1 : ')

    def p_paramdec_type(self, p):
        """paramdec : type ID"""
        print('paramdec : type ID')

    def p_paramdec_id(self, p):
        """paramdec : type ID LSB RSB"""
        print('paramdec : type ID LSB RSB')

    def p_varlist_varlist(self, p):
        """varlist : vardec varlist"""
        print('varlist : vardec varlist')

    def p_varlist_lambda(self, p):
        """varlist : """
        print('varlist : ')

    def p_block(self, p):
        """block : LCB varlist stmtlist RCB"""
        print('block : LCB varlist stmtlist RCB')

    def p_block1(self, p):
        """block : LCB varlist RCB"""
        print('block : LCB varlist RCB')

    def p_stmtlist_stmtlist(self, p):
        """stmtlist : stmt stmtlist"""
        print('stmtlist : stmt stmtlist')

    def p_stmtlist_lambda(self, p):
        """stmtlist : stmt"""
        print('stmtlist : stmt')

    def p_lvalue_id(self, p):
        """lvalue : ID"""
        print('lvalue : ID')

    def p_lvalue_idexp(self, p):
        """lvalue : ID LSB exp RSB"""
        print('lvalue : ID LSB exp RSB')

    def p_stmt_simpstmt(self, p):
        """stmt : simpstmt %prec IF3"""
        print('stmt : simpstmt')

    def p_simpstmt_return(self, p):
        """simpstmt : RETURN exp SEMICOLON"""
        print('simpstmt : RETURN exp SEMICOLON')

    def p_simpstmt_exp(self, p):
        """simpstmt : exp SEMICOLON"""
        print('simpstmt : exp SEMICOLON')

    def p_simpstmt_block(self, p):
        """simpstmt : block"""
        print('simpstmt : block')

    def p_simpstmt_while(self, p):
        """simpstmt : WHILE LRB exp RRB stmt"""
        print('simpstmt : WHILE LRB exp RRB stmt')

    def p_simpstmt_for(self, p):
        """simpstmt : FOR LRB exp SEMICOLON exp SEMICOLON exp RRB stmt"""
        print('simpstmt : FOR LRB exp SEMICOLON exp SEMICOLON exp RRB stmt')

    def p_stmt_ifnoelse(self, p):
        """stmt : ifnoelse"""
        print('stmt : ifnoelse')

    def p_stmt_ifwithelse(self, p):
        """stmt : ifwithelse"""
        print('stmt : ifwithelse')

    def p_ifnoelse_ifnoelse(self, p):
        """ifnoelse : IF LRB exp RRB stmt"""
        print('ifnoelse : IF LRB exp RRB stmt')

    def p_ifnoelse_elif(self, p):
        """ifnoelse : IF LRB exp RRB elseiflist"""
        print('ifnoelse : IF LRB exp RRB elseiflist')

    def p_ifnoelse_elif1(self, p):
        """ifnoelse : IF LRB exp RRB simpstmt elseiflist"""
        print('ifnoelse : IF LRB exp RRB simpstmt elseiflist')

    def p_ifwithelse(self, p):
        """ifwithelse : IF LRB exp RRB simpstmt elseiflist ELSE stmt %prec IF2"""
        print('ifwithelse : IF LRB exp RRB simpstmt elseiflist ELSE stmt')

    def p_ifwithelse_lambda(self, p):
        """ifwithelse : IF LRB exp RRB simpstmt ELSE simpstmt"""
        print('ifwithelse : IF LRB exp RRB simpstmt ELSE simpstmt')

    def p_simpstmt_print(self, p):
        """simpstmt : PRINT LRB ID RRB SEMICOLON"""
        print('simpstmt : PRINT LRB ID RRB SEMICOLON')

    def p_elseiflist_elseiflist(self, p):
        """elseiflist : ELIF LRB exp RRB stmt elseiflist"""
        print('elseiflist : ELIF LRB exp RRB stmt elseiflist')

    def p_elseiflist_elif(self, p):
        """elseiflist : ELIF LRB exp RRB stmt"""
        print('elseiflist : ELIF LRB exp RRB stmt')

    def p_exp_lvalueassignexp(self, p):
        """exp : lvalue ASSIGN exp"""
        print('exp : lvalue ASSIGN exp')

    def p_exp_expopexp(self, p):
        """exp : exp operator exp %prec SUM"""
        print('exp : exp operator exp')

    def p_exp_expop1exp(self, p):
        """exp : exp op1 exp %prec O"""
        print('exp : exp op1 exp')

    def p_exp_exprexp(self, p):
        """exp : exp relop exp %prec EQ"""
        print('exp : exp relop exp')

    def p_exp_const(self, p):
        """exp : const"""
        print('exp : const')

    def p_exp_lvalue(self, p):
        """exp : lvalue"""
        print('exp : lvalue')

    def p_exp_idexp(self, p):
        """exp : ID LRB explist RRB"""
        print('exp : ID LRB explist RRB')

    def p_exp_id(self, p):
        """exp : ID LRB RRB"""
        print('exp : ID LRB RRB')

    def p_exp_explrb(self, p):
        """exp : LRB exp RRB"""
        print('exp : LRB exp RRB')

    def p_exp_expnegative(self, p):
        """exp : SUB exp"""
        print('exp : SUB exp')

    def p_exp_expnot(self, p):
        """exp : NOT exp"""
        print('exp : NOT exp')

    def p_explist(self, p):
        """explist : exp"""
        print('explist : exp')

    def p_explist_explist(self, p):
        """explist :  exp COMMA explist"""
        print('explist :  exp COMMA explist')

    def p_operator_op1(self, p):
        """operator : op1 %prec O"""
        print('operator : op1')

    def p_operator_or(self, p):
        """op1 : OR"""
        print('op1 : OR')

    def p_operator_and(self, p):
        """op1 : AND"""
        print('op1 : AND')

    def p_operator_sum(self, p):
        """operator : SUM"""
        print('operator : SUM')

    def p_operator_sub(self, p):
        """operator : SUB"""
        print('operator : SUB')

    def p_operator_mul(self, p):
        """operator : MUL"""
        print('operator : MUL')

    def p_operator_div(self, p):
        """operator : DIV"""
        print('operator : DIV')

    def p_operator_remainder(self, p):
        """operator : REMAINDER"""
        print('operator : REMAINDER')

    def p_const_intnumber(self, p):
        """const : INTEGERNUMBER"""
        print('const : INTEGERNUMBER')

    def p_const_floatnumber(self, p):
        """const : FLOATNUMBER"""
        print('const : FLOATNUMBER')

    def p_const_true(self, p):
        """const : FALSE"""
        print('const : FALSE')

    def p_const_false(self, p):
        """const : TRUE"""
        print('const : TRUE')

    def p_relop_GT(self, p):
        """relop : GT"""
        print('relop : GT')

    def p_relop_LT(self, p):
        """relop : LT"""
        print('relop : LT')

    def p_relop_NE(self, p):
        """relop : NE"""
        print('relop : NE')

    def p_relop_EQ(self, p):
        """relop : EQ"""
        print('relop : EQ')

    def p_relop_LE(self, p):
        """relop : LE"""
        print('relop : LE')

    def p_relop_GE(self, p):
        """relop : GE"""
        print("relop : GE", str(p))

    '''precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'ID'),
        ('left', 'EQ', 'NE'),
        ('left', 'GE', 'LE'),
        ('left', 'GT', 'LT'),
        ('left', 'RE'),
        ('right', 'ASSIGN'),
        ('left', 'NOT'),
        ('left', 'SUM', 'SUB'),
        ('left', 'OP'),
        ('left', 'MUL', 'DIV', 'REMAINDER'),
        ('left', 'LRB', 'RRB'),
        ('left', 'IF'),
        ('left', 'IF2'),
        ('left', 'IF3'),
        ('left', 'ELIF', 'ELSE'),
        
    )'''

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'O'),
        ('left', 'ID', 'INTEGERNUMBER', 'FLOATNUMBER', 'FALSE', 'TRUE'),
        ('left', 'EQ', 'NE', 'GE', 'LE', 'GT', 'LT'),
        ('right', 'ASSIGN'),
        ('left', 'NOT'),
        ('left', 'LCB', 'LRB', 'LSB'),
        ('left', 'RCB', 'RRB', 'RSB'),
        ('left', 'SUM', 'SUB'),
        ('left', 'MUL', 'DIV', 'REMAINDER'),
        ('left', 'LRB', 'RRB'),
        ('left', 'IF'),
        ('left', 'IF2'),
        ('left', 'IF3'),
        ('left', 'ELIF', 'ELSE'),

    )

    def p_error(self, p):
        print(p.value)
        print("hhhhhh",p.value)
        raise Exception('ParsingError: invalid grammar at ', p)

    def build(self, **kwargs):
        """build the parser"""
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
