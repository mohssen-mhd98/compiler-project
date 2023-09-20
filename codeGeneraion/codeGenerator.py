from d1.nonTerminal import NonTerminal



class CodeGenerator:

    def __init__(self):
        self.lCount = 0
        self.sCount = 0
        self.id = ""
        self.a = False
        self.tempCount = 0
        pass

    def generate_arithmetic_code(self, p, temp):
        p[0] = NonTerminal()
        p[0].place = temp

        if p[1].hascode or p[3].hascode:
            if p[1].hascode:
                ltrue = self.make_list()
                jump = self.state_count()
                lfalse = self.make_list()
                op2_label = self.make_list()
                self.back_patch(p[1].t_list, ltrue, p[1].labels_dic)
                self.back_patch(p[1].f_list, lfalse, p[1].labels_dic)
                v = self.new_temp()
                s1 = ltrue + ":" + "\n" + v + "=" + "1"
                s2 = lfalse + ":" + "\n" + v + "=" + "0"
                p[1].labels_dic.update({ltrue: s1})

                if p[3].code != "":
                    p[3].code = op2_label + ":" + p[3].code
                    p[1].labels_dic.update({jump: "goto " + op2_label})
                p[1].labels_dic.update({lfalse: s2})

                for k in p[1].labels_dic:
                    p[1].code += p[1].labels_dic[k] + "\n"

                p[0].code += p[1].code
                p[0].code += p[3].code + "\n"
                p[0].code += p[0].place + " = "
                p[0].code += v + " " + p[2] + " " + str(p[3].get_value()) + ";"

            if p[3].hascode:
                ltrue = self.make_list()
                jump = self.state_count()
                lfalse = self.make_list()
                op2_label = self.make_list()
                self.back_patch(p[3].t_list, ltrue, p[3].labels_dic)
                self.back_patch(p[3].f_list, lfalse, p[3].labels_dic)
                v = self.new_temp()
                s1 = ltrue + ":" + "\n" + v + "=" + "1"
                s2 = lfalse + ":" + "\n" + v + "=" + "0"
                p[3].labels_dic.update({ltrue: s1})

                if p[1].code != "":
                    p[3].labels_dic.update({jump: "goto " + op2_label})
                p[3].labels_dic.update({lfalse: s2})

                p[3].code += "\n"
                for k in p[3].labels_dic:
                    p[3].code += p[3].labels_dic[k] + "\n"

                p[0].code += p[1].code + "\n"
                p[0].code += p[3].code
                p[0].code += p[0].place + " = "
                p[0].code += str(p[1].get_value()) + " " + p[2] + " " + v + ";"
        else:
            if p[1].code != "":
                p[0].a_dic.update(p[1].a_dic)
                p[0].code += p[1].code + str("\n")
            if p[3].code != "":
                p[0].a_dic.update(p[3].a_dic)
                p[0].code += p[3].code + str("\n")
            if p[1].isBoolean or p[1].isBoolean:
                v1, v2 = self.change_value(p)
                p[0].code += p[0].place + " = "
                p[0].code += v1 + " " + p[2] + " " + v2 + ";"
            else:
                p[0].code += p[0].place + " = "
                p[0].code += str(p[1].get_value()) + " " + p[2] + " " + str(p[3].get_value()) + ";"
        p[0].a_dic.update({"S0": p[0].code})


    def make_list(self):
        temp = "L" + str(self.lCount)
        self.lCount += 1
        return temp

    def state_count(self):
        temp = "S" + str(self.sCount)
        self.sCount += 1
        return temp

    def back_patch(self, list, quad, dic):
        for l in list:
            for d in dic:
                if l == d:
                    dic[l] += quad

    def generate_logical_code(self, p):

        if not p[1].hascode and not p[4].hascode:
            t1 = self.make_list()
            f1 = self.make_list()
            t2 = self.make_list()
            f2 = self.make_list()
            p[1].t_list.append(t1)
            p[1].f_list.append(f1)
            p[4].t_list.append(t2)
            p[4].f_list.append(f2)
            s1 = p[1].t_list[0] + " : " + "if (" + p[1].get_value() + " != 0" + ")" + " goto "
            s2 = "\n" + p[1].f_list[0] + " : " + " goto "
            s3 = p[4].t_list[0] + " : " + "if (" + p[4].get_value() + " != 0" + ")" + " goto "
            s4 = "\n" + p[4].f_list[0] + " : " + " goto "
            p[1].labels_dic.update([(t1, s1), (f1, s2)])
            p[4].labels_dic.update([(t2, s3), (f2, s4)])
            p[0].labels_dic.update([(t1, s1), (f1, s2), (t2, s3), (f2, s4)])
            p[0].code = p[1].code + "\n" + p[4].code

        elif not p[1].hascode and p[4].hascode:
            t1 = self.make_list()
            f1 = self.make_list()
            p[1].t_list.append(t1)
            p[1].f_list.append(f1)
            s1 = p[1].t_list[0] + " : " + "if (" + p[1].get_value() + " != 0" + ")" + " goto "
            s2 = p[1].f_list[0] + " : " + " goto "
            p[0].labels_dic.update([(t1, s1), (f1, s2)])
            p[1].labels_dic.update([(t1, s1), (f1, s2)])
            p[0].labels_dic.update(p[4].labels_dic)
            p[0].code = p[1].code + "\n" + p[4].code

        elif p[1].hascode and not p[4].hascode:
            t1 = self.make_list()
            f1 = self.make_list()
            p[4].t_list.append(t1)
            p[4].f_list.append(f1)
            s1 = p[4].t_list[0] + " : " + "if (" + p[4].get_value() + " != 0" + ")" + " goto "
            s2 = p[4].f_list[0] + " : " + " goto "
            p[0].labels_dic.update(p[1].labels_dic)
            p[0].labels_dic.update([(t1, s1), (f1, s2)])
            p[4].labels_dic.update([(t1, s1), (f1, s2)])
            p[0].code = p[1].code + "\n" + p[4].code

        else:
            p[0].labels_dic.update(p[1].labels_dic)
            p[0].labels_dic.update(p[4].labels_dic)
            p[0].code = p[1].code + "\n" + p[4].code

    def change_value(self, p):
        v1 = ""
        v2 = ""
        if p[1].value == "true":
            v1 = "1"
        if p[1].value == "false":
            v1 = "0"
        if p[3].value == "true":
            v2 = "1"
        if p[3].value == "false":
            v2 = "0"
        return (v1, v2)

    def new_temp(self):
        temp = "T" + str(self.tempCount)
        self.tempCount += 1
        if self.id != "":
            self.id = self.id.replace(";", ",")
        self.id += temp + ";"
        return temp