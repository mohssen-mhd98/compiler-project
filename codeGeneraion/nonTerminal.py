class NonTerminal:

    def __init__(self):
        self.value = ""
        self.code = ""
        self.place = ""
        self.quad = ""
        self.hascode = False
        self.isBoolean = False
        self.t_list = []
        self.f_list = []
        self.n_list = []
        self.ef_list = []
        self.labels_dic = {}
        self.a_dic = {}
    def get_value(self):
        if self.value == "":
            return self.place
        return self.value

