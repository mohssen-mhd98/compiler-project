from ply import yacc
from d1.lexer import Lexer
from d1.nonTerminal import NonTerminal
from d1.codeGenerator import CodeGenerator

class Parser1:
    tokens = Lexer().tokens

    def __init__(self):
        self.tempCount = 0
        self.codeGenerator = CodeGenerator()
        pass

    def p_program(self, p):
        """program : declist MAIN LRB RRB block"""
        pass

    def p_program1(self, p):
        """program : MAIN LRB RRB block"""
        pass

    def p_declist_decdeclist1(self, p):
        """declist : dec declist1"""
        pass

    def p_declist_dec(self, p):
        """declist : dec"""
        pass

    def p_declist1_declist1(self, p):
        """declist1 : dec declist1"""
        pass

    def p_declist1_dec(self, p):
        """declist1 : dec"""
        pass

    def p_dec_vardec(self, p):
        """dec : vardec"""
        pass

    def p_type_int(self, p):
        """type : INTEGER"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_iddec_id(self, p):
        """iddec : ID"""
        p[0] = NonTerminal()
        p[0].place = p[1]
        pass

    def p_iddec_idexp(self, p):
        """iddec : ID LSB exp RSB"""
        pass

    def p_iddec_idAexp(self, p):
        """iddec : ID ASSIGN exp"""
        pass

    def p_idlist_idlist1(self, p):
        """idlist : iddec idlist1"""
        pass

    def p_idlist1_iddec(self, p):
        """idlist1 : """
        pass

    def p_idlist1_idlist1(self, p):
        """idlist1 : COMMA iddec idlist1"""
        pass

    def p_vardec(self, p):
        """vardec : type idlist SEMICOLON"""
        pass

    def p_varlist_varlist(self, p):
        """varlist : vardec varlist"""
        pass

    def p_varlist_lambda(self, p):
        """varlist : """
        pass

    def p_block(self, p):
        """block : LCB varlist stmtlist RCB"""
        pass

    def p_block1(self, p):
        """block : LCB varlist RCB"""
        pass

    def p_stmtlist_stmtlist(self, p):
        """stmtlist : stmt stmtlist"""
        pass

    def p_stmtlist_lambda(self, p):
        """stmtlist : stmt"""
        pass

    def p_lvalue_id(self, p):
        """lvalue : ID"""
        p[0] = NonTerminal()
        p[0].place = p[1]
        print(p[0].place)
        pass

    def p_lvalue_idexp(self, p):
        """lvalue : ID LSB exp RSB"""
        pass

    def p_stmt_simpstmt(self, p):
        """stmt : simpstmt %prec STMT"""
        pass

    def p_simpstmt_exp(self, p):
        """simpstmt : exp SEMICOLON %prec SEMICOLON"""
        pass

    def p_simpstmt_block(self, p):
        """simpstmt : block"""
        pass

    def p_simpstmt_while(self, p):
        """simpstmt : WHILE LRB exp RRB stmt"""
        pass

    def p_simpstmt_for(self, p):
        """simpstmt : FOR LRB exp SEMICOLON exp SEMICOLON exp RRB stmt"""
        pass

    def p_stmt_ifnoelse(self, p):
        """stmt : ifnoelse"""
        pass

    def p_stmt_ifwithelse(self, p):
        """stmt : ifwithelse"""
        pass

    def p_ifnoelse_ifnoelse(self, p):
        """ifnoelse : IF LRB exp RRB stmt"""
        pass

    def p_ifnoelse_ifnoelse1(self, p):
        """ifnoelse : IF LRB exp RRB simpstmt ifwithelse"""
        pass

    def p_ifnoelse_elif(self, p):
        """ifnoelse : IF LRB exp RRB elseiflist"""
        pass

    def p_ifnoelse_elif1(self, p):
        """ifnoelse : IF LRB exp RRB simpstmt elseiflist"""
        pass

    def p_ifwithelse(self, p):
        """ifwithelse : elseiflist ELSE stmt %prec IF2"""
        pass

    def p_simpstmt_print(self, p):
        """simpstmt : PRINT LRB ID RRB SEMICOLON"""
        pass

    def p_elseiflist_elseiflist(self, p):
        """elseiflist : ELIF LRB exp RRB stmt elseiflist"""
        pass

    def p_elseiflist_elif(self, p):
        """elseiflist : ELIF LRB exp RRB stmt"""
        pass

    def p_exp_lvalueassignexp(self, p):
        """exp : lvalue ASSIGN exp"""
        pass

    def p_exp_expopexp(self, p):
        """exp : exp operator exp %prec SUM"""
        self.codeGenerator.generate_arithmetic_code(p, self.new_temp())
        pass

    def p_exp_expop1exp(self, p):
        """exp : exp op1 exp %prec ASSIGN"""
        pass

    def p_exp_exprexp(self, p):
        """exp : exp relop exp %prec EQ"""
        pass

    def p_exp_const(self, p):
        """exp : const"""
        pass

    def p_exp_lvalue(self, p):
        """exp : lvalue"""
        p[0] = NonTerminal()
        p[0].place = p[1].place
        print(p[0].place)
        pass

    def p_exp_explrb(self, p):
        """exp : LRB exp RRB"""
        pass

    def p_exp_expnegative(self, p):
        """exp : SUB exp"""
        pass

    def p_exp_expnot(self, p):
        """exp : NOT exp"""
        pass

    def p_operator_op1(self, p):
        """operator : op1 %prec O"""
        pass

    def p_operator_or(self, p):
        """op1 : OR"""
        pass

    def p_operator_and(self, p):
        """op1 : AND"""
        pass

    def p_operator_sum(self, p):
        """operator : SUM"""
        pass

    def p_operator_sub(self, p):
        """operator : SUB"""
        pass

    def p_operator_mul(self, p):
        """operator : MUL"""
        pass

    def p_operator_div(self, p):
        """operator : DIV"""
        pass

    def p_operator_remainder(self, p):
        """operator : REMAINDER"""
        pass

    def p_const_intnumber(self, p):
        """const : INTEGERNUMBER"""
        pass

    def p_const_true(self, p):
        """const : FALSE"""
        pass

    def p_const_false(self, p):
        """const : TRUE"""
        pass

    def p_relop_GT(self, p):
        """relop : GT"""
        pass

    def p_relop_LT(self, p):
        """relop : LT"""
        pass

    def p_relop_NE(self, p):
        """relop : NE"""
        pass

    def p_relop_EQ(self, p):
        """relop : EQ"""
        pass

    def p_relop_LE(self, p):
        """relop : LE"""
        pass

    def p_relop_GE(self, p):
        """relop : GE"""
        pass


    precedence = (
        ('left', 'COMMA'),
        ('right', 'ASSIGN'),
        ('left', 'AND'),
        ('left', 'OR'),
        ('left', 'O'),
        ('left', 'EQ', 'NE'),
        ('left', 'GT', 'LT', 'GE', 'LE'),
        ('left', 'NOT'),
        ('left', 'SUM', 'SUB'),
        ('left', 'MUL', 'DIV', 'REMAINDER'),
        ('left', 'LCB', 'RCB', 'LRB', 'RRB'),
        ('left', 'IF2'),
        ('left', 'STMT'),
        ('left', 'IF'),
        ('left', 'ELIF'),
        ('left', 'ELSE'),
        ('left', 'INTEGER'),
        ('left', 'ID', 'INTEGERNUMBER', 'FLOATNUMBER', 'FALSE', 'TRUE', 'SEMICOLON'),
    )

    def new_temp(self):
        temp = "T" + str(self.tempCount)
        self.tempCount += 1
        return temp

    def p_error(self, p):
        print(p.value)
        print("hhhhhh", p.value)
        raise Exception('ParsingError: invalid grammar at ', p)

    def build(self, **kwargs):
        """build the parser"""
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
