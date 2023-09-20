from ply import yacc
from d1.lexer import Lexer
from d1.nonTerminal import NonTerminal
from d1.codeGenerator import CodeGenerator


class Parser1:
    tokens = Lexer().tokens
    pid = NonTerminal()
    tmp = ""

    def __init__(self):
        self.codeGenerator = CodeGenerator()
        self.eCount = 0
        pass

    def p_program(self, p):
        """program : declist MAIN LRB RRB block"""
        p[0] = NonTerminal()
        self.codeGenerator.id = "int " + self.codeGenerator.id
        p[0].code = self.codeGenerator.id + "\n" + p[1].code + p[5].code
        print(p[0].code)
        pass

    def p_declist_decdeclist1(self, p):
        """declist : declist dec"""
        p[0] = NonTerminal()
        p[0].code = p[1].code + "\n" + p[2].code
        pass

    def p_declist_lambda(self, p):
        """declist : """
        p[0] = NonTerminal()
        pass


    def p_dec_vardec(self, p):
        """dec : vardec"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
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
        p[0] = NonTerminal()
        if p[3].code != "":
            p[0].code = p[3].code + "\n"
        p[0].place = p[1] + p[2] + str(p[3].get_value()) + p[4]
        pass

    def p_iddec_idAexp(self, p):
        """iddec : ID ASSIGN exp"""
        p[0] = NonTerminal()
        p[0].place = p[1] + p[2] + str(p[3].get_value())
        p[0].code = p[3].code + "\n"
        pass

    def p_idlist_idlist(self, p):
        """idlist : iddec COMMA idlist"""
        p[0] = NonTerminal()
        p[0].code = p[1].code + p[3].code
        p[0].place += p[1].place + p[2] + p[3].place
        pass

    def p_idlist_iddec(self, p):
        """idlist : iddec"""
        p[0] = NonTerminal()
        p[0].place = p[1].place
        p[0].code = p[1].code
        pass

    def p_vardec(self, p):
        """vardec : type idlist SEMICOLON"""
        p[0] = NonTerminal()
        p[0].code = p[2].code + p[1].value + " " + p[2].place + p[3] + "\n"
        pass

    def p_varlist_varlist(self, p):
        """varlist : varlist vardec"""
        p[0] = NonTerminal()
        p[0].code = p[1].code + "\n" + p[2].code
        pass

    def p_varlist_vardec(self, p):
        """varlist : """
        p[0] = NonTerminal()
        pass

    def p_block(self, p):
        """block : LCB varlist stmtlist RCB"""
        p[0] = NonTerminal()
        p[0].code = p[2].code + p[3].code
        p[0].n_list = p[3].n_list
        p[0].labels_dic = p[3].labels_dic.copy()
        pass

    def p_stmtlist_stmtlist(self, p):
        """stmtlist : stmt stmtlist"""
        p[0] = NonTerminal()
        if bool(p[1].labels_dic):
            if bool(p[2].labels_dic):
                if list(p[2].labels_dic.keys())[0][0] == "S":
                    #print("SsssSS",p[1].code)
                    m = self.codeGenerator.make_list()
                    self.codeGenerator.back_patch(p[1].n_list, m, p[1].labels_dic)
                    p[2].code = m + " : " + p[2].code
                if list(p[2].labels_dic.keys())[0][0] == "L":
                    #print("LLllllL")
                    m = list(p[2].labels_dic.keys())[0]
                    self.codeGenerator.back_patch(p[1].n_list, m, p[1].labels_dic)
            else:
                p[0].labels_dic = p[1].labels_dic.copy()
                m = self.codeGenerator.make_list()
                self.codeGenerator.back_patch(p[1].n_list, m, p[1].labels_dic)
                p[2].code = m + " : " + p[2].code
        else:
            p[0].labels_dic.clear()
            p[0].labels_dic.update(p[2].a_dic)
            p[0].labels_dic.update(p[1].labels_dic)
        p[0].n_list = p[1].n_list + p[2].n_list
        for x in p[1].labels_dic:
            p[1].code += p[1].labels_dic[x] + "\n"
        p[0].code += p[1].code + "\n" + p[2].code

        pass

    def p_stmtlist_lambda(self, p):
        """stmtlist : """
        p[0] = NonTerminal()
        pass

    def p_stmt_block(self, p):
        """stmt : block"""
        p[0] = NonTerminal()
        p[0].code = p[1].code
        p[0].n_list = p[1].n_list
        p[0].labels_dic = p[1].labels_dic.copy()
        pass

    def p_lvalue_id(self, p):
        """lvalue : ID"""
        p[0] = NonTerminal()
        p[0].place = p[1]
        pass

    def p_lvalue_idexp(self, p):
        """lvalue : ID LSB exp RSB"""
        p[0] = NonTerminal()
        p[0].place = p[1] + p[2] + str(p[3].get_value()) + p[4]
        p[0].code = p[3].code
        pass

    def p_stmt_exp(self, p):
        """stmt : exp SEMICOLON"""
        p[0] = NonTerminal()
        p[0].code = p[1].code + p[2]
        p[0].a_dic = p[1].a_dic.copy()
        #print(p[0].code)
        pass

    def p_m(self, p):
        """m : %prec A"""
        p[0] = NonTerminal()
        p[0].quad = "L" + str(self.codeGenerator.lCount)
        self.codeGenerator.lCount += 1
        pass

    def p_n(self, p):
        """n : %prec A"""
        p[0] = NonTerminal()
        p[0].n_list.append("L" + str(self.codeGenerator.lCount))
        self.codeGenerator.lCount += 1
        pass

    def p_stmt_while(self, p):
        """stmt : WHILE LRB exp RRB m stmt"""
        p[0] = NonTerminal()
        p[0].n_list = p[3].f_list
        if p[3].a_dic["S0"] != "":
            sc = self.codeGenerator.state_count()
            p[0].labels_dic.update({sc: p[3].a_dic["S0"]})
        p[0].labels_dic.update(p[3].labels_dic)
        tmp = list(p[3].labels_dic.keys())[0]

        if not bool(p[6].labels_dic):
            self.codeGenerator.back_patch(p[3].t_list, p[5].quad, p[0].labels_dic)
            p[0].labels_dic[p[5].quad] = p[5].quad + " : " + p[6].code

        else:
            #print(p[6].n_list, tmp,"p[6].n_list, tmp")
            if list(p[6].labels_dic.keys())[0][0] == "S":
                self.codeGenerator.back_patch(p[3].t_list, p[5].quad, p[0].labels_dic)
                p[0].labels_dic[p[5].quad] = p[5].quad + " : " + "\n"
                p[0].labels_dic.update(p[6].labels_dic)
                self.codeGenerator.back_patch(p[6].n_list, tmp, p[0].labels_dic)

            else:
                tmp1 = int(p[5].quad[1:]) + 1
                q = "L" + str(tmp1)
                self.codeGenerator.back_patch(p[3].t_list, q, p[0].labels_dic)
                p[0].labels_dic.update(p[6].labels_dic)
                self.codeGenerator.back_patch(p[6].n_list, tmp, p[0].labels_dic)

        s1 = "goto " + tmp
        sc = self.codeGenerator.state_count()
        p[0].labels_dic.update({sc: s1})
        pass

    def p_stmt_for(self, p):
        """stmt : FOR LRB exp SEMICOLON m exp SEMICOLON exp RRB m stmt"""
        p[0] = NonTerminal()
        p[0].n_list = p[6].f_list
        sc = self.codeGenerator.state_count()
        p[0].labels_dic.update({sc: p[3].a_dic["S0"]})
        if p[6].a_dic["S0"] != "":
            sc = self.codeGenerator.state_count()
            p[0].labels_dic.update({sc: p[6].a_dic["S0"]})
        p[0].labels_dic.update(p[6].labels_dic)
        tmp = list(p[6].labels_dic.keys())[0]

        if not bool(p[11].labels_dic):
            self.codeGenerator.back_patch(p[6].t_list, p[10].quad, p[0].labels_dic)
            p[0].labels_dic[p[10].quad] = p[10].quad + " : " + p[11].code
            sc = self.codeGenerator.state_count()
            p[0].labels_dic.update({sc: p[8].a_dic["S0"]})

        else:
            if list(p[11].labels_dic.keys())[0][0] == "S":
                self.codeGenerator.back_patch(p[6].t_list, p[10].quad, p[0].labels_dic)
                p[0].labels_dic[p[10].quad] = p[10].quad + " : " + "\n"
                p[0].labels_dic.update(p[11].labels_dic)
                self.codeGenerator.back_patch(p[11].n_list, tmp, p[0].labels_dic)
                sc = self.codeGenerator.state_count()
                p[0].labels_dic.update({sc: p[8].a_dic["S0"]})
            else:
                tmp1 = int(p[10].quad[1:]) + 1
                q = "L" + str(tmp1)
                self.codeGenerator.back_patch(p[6].t_list, q, p[0].labels_dic)
                p[0].labels_dic.update(p[11].labels_dic)
                self.codeGenerator.back_patch(p[11].n_list, tmp, p[0].labels_dic)
                sc = self.codeGenerator.state_count()
                p[0].labels_dic.update({sc: p[8].a_dic["S0"]})
        s1 = "goto " + tmp
        sc = self.codeGenerator.state_count()
        p[0].labels_dic.update({sc: s1})
        pass

    def p_stmt_ifnoelse(self, p):
        """stmt : ifnoelse n elseiflist ifwithelse"""
        p[0] = NonTerminal()
        if not bool(p[3].labels_dic) and not bool(p[4].labels_dic):
            p[0].labels_dic = p[1].labels_dic.copy()
            p[0].n_list = p[1].n_list.copy()

        elif bool(p[3].labels_dic) and not bool(p[4].labels_dic):
            #print(p[3].n_list)
            for x in p[1].f_list:
                if x in p[1].n_list:
                    p[1].n_list.remove(x)

            if p[3].code != "":
                e = self.new_elif()
                self.codeGenerator.back_patch(p[1].f_list, e, p[1].labels_dic)
                p[0].labels_dic = p[1].labels_dic.copy()
                p[0].labels_dic[p[2].n_list[0]] = p[2].n_list[0] + " : " + "goto "
                p[0].labels_dic.update({e: p[3].code})

            else:
                tmp = list(p[3].labels_dic.keys())[0]
                self.codeGenerator.back_patch(p[1].f_list, tmp, p[1].labels_dic)
                p[0].labels_dic = p[1].labels_dic.copy()
                p[0].labels_dic[p[2].n_list[0]] = p[2].n_list[0] + " : " + "goto "

            p[0].labels_dic.update(p[3].labels_dic)
            p[0].n_list += p[1].n_list + p[2].n_list + p[3].n_list + p[3].ef_list

        elif not bool(p[3].labels_dic) and bool(p[4].labels_dic):
            for x in p[1].f_list:
                if x in p[1].n_list:
                    p[1].n_list.remove(x)

            if list(p[4].labels_dic.keys())[0][0] == "S":
                self.codeGenerator.back_patch(p[1].f_list, p[4].quad, p[1].labels_dic)
                p[0].labels_dic = p[1].labels_dic.copy()
                p[0].labels_dic[p[2].n_list[0]] = p[2].n_list[0] + " : " + "goto "
                p[0].labels_dic[p[4].quad] = p[4].quad + " : " + "\n"
                p[0].labels_dic.update(p[4].labels_dic)
                p[0].n_list += p[1].n_list + p[2].n_list + p[4].n_list

            elif p[4].quad in p[4].labels_dic:
                self.codeGenerator.back_patch(p[1].f_list, p[4].quad, p[1].labels_dic)
                p[0].labels_dic = p[1].labels_dic.copy()
                p[0].labels_dic[p[2].n_list[0]] = p[2].n_list[0] + " : " + "goto "
                p[0].labels_dic.update(p[4].labels_dic)
                p[0].n_list += p[1].n_list + p[2].n_list + p[4].n_list

            else:
                tmp1 = int(p[4].quad[1:]) + 1
                q = "L" + str(tmp1)
                self.codeGenerator.back_patch(p[1].f_list, q, p[1].labels_dic)
                p[0].labels_dic = p[1].labels_dic.copy()
                p[0].labels_dic[p[2].n_list[0]] = p[2].n_list[0] + " : " + "goto "
                p[0].labels_dic.update(p[4].labels_dic)
                p[0].n_list += p[1].n_list + p[2].n_list + p[4].n_list
        else:
            for x in p[1].f_list:
                if x in p[1].n_list:
                    p[1].n_list.remove(x)

            if p[3].code != "":
                tmp = list(p[3].labels_dic.keys())[0]
                self.codeGenerator.back_patch(p[1].f_list, tmp, p[1].labels_dic)
                p[0].labels_dic = p[1].labels_dic.copy()
                p[0].labels_dic[p[2].n_list[0]] = p[2].n_list[0] + " : " + "goto "

            else:
                e = self.new_elif()
                self.codeGenerator.back_patch(p[1].f_list, e, p[1].labels_dic)
                p[0].labels_dic = p[1].labels_dic.copy()
                p[0].labels_dic[p[2].n_list[0]] = p[2].n_list[0] + " : " + "goto "
                p[0].labels_dic.update({e: p[3].code})

            tmp_list = []
            tmp_list.append(p[3].f_list[len(p[3].f_list) - 1])

            if list(p[4].labels_dic.keys())[0][0] == "S":
                self.codeGenerator.back_patch(tmp_list, p[4].quad, p[3].labels_dic)
                p[0].labels_dic.update(p[3].labels_dic)
                p[0].labels_dic[p[3].quad] = p[3].quad + " : " + "goto "
                p[0].labels_dic[p[4].quad] = p[4].quad + " : " + "\n"

            elif p[4].quad in p[4].labels_dic:
                self.codeGenerator.back_patch(tmp_list, p[4].quad, p[3].labels_dic)
                p[0].labels_dic.update(p[3].labels_dic)
                p[0].labels_dic[p[3].quad] = p[3].quad + " : " + "goto "

            else:
                tmp1 = int(p[4].quad[1:]) + 1
                q = "L" + str(tmp1)
                self.codeGenerator.back_patch(tmp_list, q, p[3].labels_dic)
                p[0].labels_dic.update(p[3].labels_dic)
                p[0].labels_dic[p[3].quad] = p[3].quad + " : " + "goto "
            l = []
            l.append(p[3].quad)
            p[0].labels_dic.update(p[4].labels_dic)
            p[0].n_list += p[1].n_list + p[2].n_list + p[3].n_list + l + p[4].n_list

        pass

    def p_ifnoelse_ifnoelse(self, p):
        """ifnoelse :  IF LRB exp RRB m stmt"""
        p[0] = NonTerminal()
        if p[3].a_dic["S0"] != "":
            sc = self.codeGenerator.state_count()
            p[0].labels_dic.update({sc: p[3].a_dic["S0"]})
        p[0].labels_dic.update(p[3].labels_dic)
        tmp = p[5].quad
        p[0].n_list = p[3].f_list + p[6].n_list
        p[0].f_list = p[3].f_list.copy()

        if not bool(p[6].labels_dic):
            self.codeGenerator.back_patch(p[3].t_list, p[5].quad, p[0].labels_dic)
            p[0].labels_dic[tmp] = tmp + " : " + p[6].code

        else:
            if list(p[6].labels_dic.keys())[0][0] == "S":
                self.codeGenerator.back_patch(p[3].t_list, p[5].quad, p[0].labels_dic)
                p[0].labels_dic[p[5].quad] = p[5].quad + " : " + "\n"
                p[0].labels_dic.update(p[6].labels_dic)
            else:
                tmp1 = int(p[5].quad[1:]) + 1
                q = "L" + str(tmp1)
                self.codeGenerator.back_patch(p[3].t_list, q, p[0].labels_dic)
                p[0].labels_dic.update(p[6].labels_dic)
            '''
            dic = {}
            tmp1 = list(p[0].labels_dic.keys())[0]
            dic[tmp] = p[0].labels_dic.pop(tmp1)
            dic.update(p[0].labels_dic)
            p[0].labels_dic = dic.copy()
            '''
        pass

    def p_ifwithelse_else(self, p):
        """ifwithelse : ELSE m stmt"""
        p[0] = NonTerminal()
        p[0].quad = tmp = p[2].quad
        p[0].n_list = p[3].n_list

        if not bool(p[3].labels_dic):
            p[0].labels_dic[tmp] = tmp + " : " + p[3].code

        else:
            p[0].labels_dic.update(p[3].labels_dic)
        pass

    def p_ifwithelse_lambda(self, p):
        """ifwithelse : %prec IF"""
        p[0] = NonTerminal()
        pass

    def p_stmt_print(self, p):
        """stmt : PRINT LRB ID RRB SEMICOLON"""
        p[0] = NonTerminal()
        p[0].code = "printf" + p[2] + "%d" + ", " + p[3] + p[4] + p[5] + "\n"
        pass

    def p_elseiflist_elseiflist(self, p):
        """elseiflist : ELIF LRB exp RRB m stmt n elseiflist"""
        p[0] = NonTerminal()
        if p[3].a_dic["S0"] != "":
            p[0].code += p[3].a_dic["S0"] + "\n"
        p[0].ef_list = p[3].f_list
        p[0].labels_dic.update(p[3].labels_dic)
        p[0].labels_dic.update(p[8].labels_dic)
        p[0].f_list = p[3].f_list + p[8].f_list
        p[0].quad = p[7].n_list[0]
        tmp = p[5].quad

        if not bool(p[6].labels_dic):
            self.codeGenerator.back_patch(p[3].t_list, p[5].quad, p[0].labels_dic)
            p[0].labels_dic[tmp] = tmp + " : " + p[6].code

        else:
            if list(p[6].labels_dic.keys())[0][0] == "S":
                self.codeGenerator.back_patch(p[3].t_list, p[5].quad, p[0].labels_dic)
                p[0].labels_dic[p[5].quad] = p[5].quad + " : " + "\n"
                p[0].labels_dic.update(p[6].labels_dic)
            else:
                tmp1 = int(p[5].quad[1:]) + 1
                q = "L" + str(tmp1)
                self.codeGenerator.back_patch(p[3].t_list, q, p[0].labels_dic)
                p[0].labels_dic.update(p[6].labels_dic)

        if not bool(p[8].labels_dic):
            p[0].n_list = p[6].n_list
        else:
            p[0].n_list = p[6].n_list + p[7].n_list + p[8].n_list
            p[0].labels_dic[p[7].n_list[0]] = p[7].n_list[0] + " : " + "goto "
            if len(p[8].labels_dic.keys()) != 0:
                tmp1 = list(p[8].labels_dic.keys())[0]
                self.codeGenerator.back_patch(p[3].f_list, tmp1, p[0].labels_dic)
        d = {}
        list1 = []
        l = sorted(p[0].labels_dic)
        for key in range(len(l)):
            list1.append(int(l[key][1:]))
        l.clear()
        list1.sort()
        for key in range(len(list1)):
            l.append("L" + str(list1[key]))
        for key in l:
            d.update({key : p[0].labels_dic[key]})
        p[0].labels_dic = d.copy()
        #print(p[0].labels_dic, self.codeGenerator.lCount)
        pass

    def p_elseiflist_lambda(self, p):
        """elseiflist : %prec E"""
        p[0] = NonTerminal()
        pass

    def p_exp_lvalueassignexp(self, p):
        """exp : lvalue ASSIGN exp"""
        p[0] = NonTerminal()
        if p[1].code != "":
            p[0].code = p[1].code + "\n"
        if p[3].code != "":
            p[0].code += p[3].code + "\n"
        p[0].code += p[1].place + p[2] + p[3].get_value()
        p[0].a_dic.update({"S0": p[0].code})
        #print(p[3].code)
        pass

    def p_exp_expopexp(self, p):
        """exp : exp SUM exp"""
        self.codeGenerator.generate_arithmetic_code(p, self.codeGenerator.new_temp())
        pass

    def p_exp_expsumexp(self, p):
        """exp : exp SUB exp"""
        self.codeGenerator.generate_arithmetic_code(p, self.codeGenerator.new_temp())
        pass

    def p_exp_expsubexp(self, p):
        """exp : exp MUL exp"""
        self.codeGenerator.generate_arithmetic_code(p, self.codeGenerator.new_temp())
        pass

    def p_exp_expdivexp(self, p):
        """exp : exp DIV exp"""
        self.codeGenerator.generate_arithmetic_code(p, self.codeGenerator.new_temp())
        pass

    def p_exp_expmodexp(self, p):
        """exp : exp REMAINDER exp"""
        self.codeGenerator.generate_arithmetic_code(p, self.codeGenerator.new_temp())
        pass

    def p_exp_exporexp(self, p):
        """exp : exp OR m exp"""
        p[0] = NonTerminal()
        p[0].hascode = True
        self.codeGenerator.generate_logical_code(p)
        p[0].t_list = p[1].t_list + p[4].t_list
        p[0].f_list = p[4].f_list
        tmp = list(p[4].labels_dic.keys())[0]
        self.codeGenerator.back_patch(p[1].f_list, tmp, p[0].labels_dic)
        p[0].a_dic.update({"S0": p[0].code})
        pass

    def p_exp_expandexp(self, p):
        """exp : exp AND m exp"""
        p[0] = NonTerminal()
        p[0].hascode = True
        self.codeGenerator.generate_logical_code(p)
        p[0].t_list = p[4].t_list
        p[0].f_list = p[1].f_list + p[4].f_list

        tmp = list(p[4].labels_dic.keys())[0]
        self.codeGenerator.back_patch(p[1].t_list, tmp, p[0].labels_dic)

        p[0].a_dic.update({"S0": p[0].code})
        pass

    def p_exp_exprexp(self, p):
        """exp : exp relop exp %prec EQ"""
        p[0] = NonTerminal()
        t = self.codeGenerator.make_list()
        f = self.codeGenerator.make_list()
        p[0].t_list.append(t)
        p[0].f_list.append(f)
        s1 = p[0].t_list[0] + " : " + "if (" + p[1].get_value() + p[2].value + p[3].get_value() + ")" + " goto "
        s2 = p[0].f_list[0] + " : " + " goto "
        p[0].code = p[1].code
        if p[1].code != "":
            p[0].code += "\n"
        p[0].code += p[3].code
        if p[3].code != "":
            p[0].code += "\n"
        p[0].labels_dic.update([(t, s1), (f, s2)])
        p[0].a_dic.update({"S0": p[0].code})
        p[0].hascode = True
        #print(p[0].labels_dic)
        pass

    def p_exp_const(self, p):
        """exp : const"""
        p[0] = NonTerminal()
        p[0].value = p[1].value
        p[0].isBoolean = p[1].isBoolean
        pass

    def p_exp_lvalue(self, p):
        """exp : lvalue"""
        p[0] = NonTerminal()
        p[0].place = p[1].place
        if p[1].code != "":
            p[0].code = p[1].code
        pass

    def p_exp_explrb(self, p):
        """exp : LRB exp RRB"""
        p[0] = NonTerminal()
        p[0].code = p[2].code
        p[0].place = p[2].place
        p[0].t_list = p[2].t_list.copy()
        p[0].f_list = p[2].f_list.copy()
        p[0].a_dic = p[2].a_dic.copy()
        p[0].labels_dic = p[2].labels_dic.copy()
        #print(p[0].labels_dic,"eeeee")
        if p[2].hascode:
            p[0].hascode = True
        pass

    def p_exp_expnegative(self, p):
        """exp : SUB exp"""
        p[0] = NonTerminal()
        p[0].place = self.codeGenerator.new_temp()
        if p[2].code != "":
            p[0].code = p[2].code + "\n"
        p[0].code += p[0].place + "=" + p[1] + p[2].get_value()
        pass

    def p_exp_expnot(self, p):
        """exp : NOT exp"""
        p[0] = NonTerminal()
        p[0].t_list = p[2].t_list.copy()
        p[0].f_list = p[2].f_list.copy()
        p[0].place = self.codeGenerator.new_temp()
        if p[2].value != "":
            if type(p[2].value) == str:
                if p[2].value == "true":
                    p[2].value = "false"
                if p[2].value == "false":
                    p[2].value = "true"

            if type(p[2].value) == str:
                #print(int(p[2].value))
                if int(p[2].value) != 0:
                    p[2].value = 0
                elif int(p[2].value) == 0:
                    p[2].value = 1
        if p[2].code != "":
            p[0].code = p[2].code + "\n"

        if p[2].hascode:
            for key in p[2].labels_dic:
                if p[2].labels_dic[key][10] == ">":
                    p[2].labels_dic[key] = p[2].labels_dic[key].replace(">", "<")
                elif p[2].labels_dic[key][10] == "<":
                    p[2].labels_dic[key] = p[2].labels_dic[key].replace("<", ">")
                elif p[2].labels_dic[key][10] == "=":
                    p[2].labels_dic[key] = p[2].labels_dic[key].replace("=", "!",1)
                elif p[2].labels_dic[key][10] == "!":
                    p[2].labels_dic[key] = p[2].labels_dic[key].replace("!", "=")

        p[0].code += p[0].place + "=" + p[1] + str(p[2].get_value())
        p[0].a_dic = p[2].a_dic.copy()
        p[0].labels_dic = p[2].labels_dic.copy()
        pass

    def p_const_intnumber(self, p):
        """const : INTEGERNUMBER"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_const_true(self, p):
        """const : FALSE"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        p[0].isBoolean = True
        pass

    def p_const_false(self, p):
        """const : TRUE"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        p[0].isBoolean = True
        pass

    def p_relop_GT(self, p):
        """relop : GT"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_relop_LT(self, p):
        """relop : LT"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_relop_NE(self, p):
        """relop : NE"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_relop_EQ(self, p):
        """relop : EQ"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_relop_LE(self, p):
        """relop : LE"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    def p_relop_GE(self, p):
        """relop : GE"""
        p[0] = NonTerminal()
        p[0].value = p[1]
        pass

    precedence = (
        ('left', 'A'),
        ('left', 'ASSIGN'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE', 'GE', 'LE', 'GT', 'LT'),
        ('left', 'NOT'),
        ('left', 'LCB', 'LRB', 'LSB'),
        ('left', 'RCB', 'RRB', 'RSB'),
        ('left', 'SUM', 'SUB'),
        ('left', 'REMAINDER'),
        ('left', 'MUL', 'DIV'),
        ('left', 'ID', 'INTEGERNUMBER', 'FLOATNUMBER', 'FALSE', 'TRUE'),
        ('left', 'LRB', 'RRB'),
        ('left', 'IF'),
        ('left', 'E'),
        ('left', 'ELIF', 'ELSE'),
    )

    def new_elif(self):
        temp = "E" + str(self.eCount)
        self.eCount += 1
        return temp

    def p_error(self, p):
        print(p.value)
        print("hhhhhh", p.value)
        raise Exception('ParsingError: invalid grammar at ', p)

    def build(self, **kwargs):
        """build the parser"""
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser
