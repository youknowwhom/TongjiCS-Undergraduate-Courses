class Attribute:
    def __init__(self):
        self.type = ""          # 值类型 int float word tmp_word
        self.place = None       # 存储位置
        self.quad = None        # 下一条四元式位置
        self.truelist = []      # true条件跳转目标
        self.falselist = []     # false条件跳转目标
        self.nextlist = []      # 顺序执行下一目标
        self.queue = []         # 队列（用于函数参数）
        self.has_return = False # 是否有一个一定能执行到的return

    def __repr__(self):
        return f"<Attribute Object (Type:{self.type}, Place:{self.place}, Truelist:{self.truelist}, Falselist:{self.falselist}, Nextlist:{self.nextlist}, Quad:{self.quad})>"


class Word:
    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.type = ""

    def __repr__(self):
        return f"<Word Object (ID:{self.id}, Name:{self.name}, Type:{self.type})>"


class Quaternion:
    def __init__(self, op="", src1="", src2="", tar=""):
        self.op = op
        self.src1 = src1
        self.src2 = src2
        self.tar = tar

    def __repr__(self):
        return f"({self.op}, {self.src1}, {self.src2}, {self.tar})"


class Process:
    def __init__(self, start_address):
        self.name = ""
        self.return_type = ""
        self.actual_returns = []
        self.start_address = start_address
        self.words_table = [Word()]
        self.param = []

    def __repr__(self):
        return f"<Process Object (Name:{self.name}, Return Type:{self.return_type}, Start Address:{self.start_address}, Params:{self.param})>"


class Semantic:
    def __init__(
        self, productions, non_terminal_symbols, terminal_symbols, start_address=100
    ):
        self.words_table = [Word()]  # 全局变量
        self.tmp_words_table = []  # 所有的临时变量
        self.process_table = []
        self.quaternion_table = []
        self.productions = productions
        self.non_terminal_symbols = non_terminal_symbols
        self.terminal_symbols = terminal_symbols
        self.start_address = start_address
        self.error_occur = False
        self.error_msg = []

    def create_process(self, start_address):
        self.process_table.append(Process(start_address))

    def checkup_word(self, word_name):
        words_table = self.process_table[-1].words_table
        # 在作用域内找到
        for i, word in enumerate(words_table):
            if word.name == word_name:
                return i
        # 全局变量
        for i, word in enumerate(self.words_table):
            if word.name == word_name:
                return -i
        return 0

    def checkup_word_type(self, word_name):
        words_table = self.process_table[-1].words_table
        word_type = next(
            (word.type for word in words_table if word.name == word_name), None
        )
        # 低层屏蔽高层，再去全局变量找
        if word_type is None:
            word_type = next(
                (word.type for word in self.words_table if word.name == word_name), None
            )
        return word_type

    def get_word(self, place):
        if place > 0:
            return self.process_table[-1].words_table[place]
        else:
            return self.words_table[-place]

    def create_word(self, word):
        words_table = self.process_table[-1].words_table
        word.id = len(words_table)
        words_table.append(word)

    def raise_error(self, type, loc, msg):
        if type == "Error":
            self.error_occur = True
        self.error_msg.append(f"{type} at ({loc['row']},{loc['col']}): {msg}")

    def analyse(self, production_id, loc, item, tmp_symbol_stack):
        # VarStatement -> int ID | float ID
        if (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "VarStatement"
        ):
            # 检查是否重复定义
            var_name = tmp_symbol_stack[1]["tree"]["content"]
            if self.checkup_word(var_name) > 0:
                self.raise_error("Error", loc, f"变量{var_name}重定义")

            # 添加新的变量
            new_word = Word(name=var_name)
            new_word.type = self.terminal_symbols[
                self.productions[production_id].to_ids[0]
            ]
            tmp = Attribute()
            tmp.type = new_word.type
            self.create_word(new_word)
            item["attribute"] = tmp

        # FactorExpression -> identifier | integer_constant | floating_point_constant
        # | ( RelopExpression ) | FactorExpression / FactorExpression | FactorExpression * FactorExpression | FunctionCallExpression
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "FactorExpression"
        ):
            tmp = Attribute()
            if len(self.productions[production_id].to_ids) == 1:
                if (
                    self.productions[production_id].to_ids[0]
                    >= len(self.terminal_symbols)
                    and self.non_terminal_symbols[
                        self.productions[production_id].to_ids[0]
                        - len(self.terminal_symbols)
                    ]
                    == "FunctionCallExpression"
                ):
                    tmp = Attribute()
                    ret_attr = tmp_symbol_stack[0]["attribute"]
                    if ret_attr.type != "tmp_word":
                        self.raise_error("Error", loc, "void类型的操作数非法")
                    tmp.type = ret_attr.type
                    tmp.place = ret_attr.place

                elif (
                    self.terminal_symbols[self.productions[production_id].to_ids[0]]
                    == "identifier"
                ):  # ID
                    var_name = tmp_symbol_stack[0]["tree"]["content"]
                    i = self.checkup_word(var_name)
                    if i == 0:
                        self.raise_error("Error", loc, f"{var_name}: 未声明的标识符")
                    tmp.type = "word"
                    tmp.place = i

                elif (
                    self.terminal_symbols[self.productions[production_id].to_ids[0]]
                    == "integer_constant"
                ):  # integer_constant
                    tmp.type = "int"

                else:  # floating_point_constant
                    tmp.type = "float"

                tmp.quad = len(self.quaternion_table)
                tmp.truelist.append(len(self.quaternion_table))
                tmp.falselist.append(len(self.quaternion_table) + 1)

            # FactorExpression -> ( RelopExpression )

            elif self.productions[production_id].to_ids[0] < len(self.terminal_symbols):
                tmp.type = tmp_symbol_stack[1]["attribute"].type
                tmp.place = tmp_symbol_stack[1]["attribute"].place
                tmp.quad = tmp_symbol_stack[1]["attribute"].quad
                tmp.truelist = tmp_symbol_stack[1]["attribute"].truelist
                tmp.falselist = tmp_symbol_stack[1]["attribute"].falselist

            # FactorExpression -> FactorExpression / FactorExpression | FactorExpression * FactorExpression
            else:
                tmp.type = "tmp_word"  # tmp_word
                tmp.place = len(self.tmp_words_table)

                # 语义检查
                src1_type = (
                    "int"
                    if tmp_symbol_stack[0]["attribute"].type == "int"
                    else "float"
                    if tmp_symbol_stack[0]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[0]["attribute"].place).type
                    if tmp_symbol_stack[0]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[0]["attribute"].place
                    ].type
                )
                src2_type = (
                    "int"
                    if tmp_symbol_stack[2]["attribute"].type == "int"
                    else "float"
                    if tmp_symbol_stack[2]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[2]["attribute"].place).type
                    if tmp_symbol_stack[2]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[2]["attribute"].place
                    ].type
                )

                src1_name = (
                    str(tmp_symbol_stack[0]["tree"]["content"])
                    if tmp_symbol_stack[0]["attribute"].type == "int"
                    else str(tmp_symbol_stack[0]["tree"]["content"])
                    if tmp_symbol_stack[0]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[0]["attribute"].place).name
                    if tmp_symbol_stack[0]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[0]["attribute"].place
                    ].name
                )

                src2_name = (
                    str(tmp_symbol_stack[2]["tree"]["content"])
                    if tmp_symbol_stack[2]["attribute"].type == "int"
                    else str(tmp_symbol_stack[2]["tree"]["content"])
                    if tmp_symbol_stack[2]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[2]["attribute"].place).name
                    if tmp_symbol_stack[2]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[2]["attribute"].place
                    ].name
                )

                # 类型转换
                if src1_type == "int" and src2_type == "float":
                    tmp_word = Word(len(self.tmp_words_table), "")
                    tmp_word.name = f"T{tmp_word.id}"
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion = Quaternion(
                        "intofloat", src1_name, "_", tmp_word.name
                    )
                    self.quaternion_table.append(tmp_quaternion)
                    src1_name = tmp_word.name
                    tar_type = "float"
                elif src2_type == "int" and src1_type == "float":
                    tmp_word = Word(len(self.tmp_words_table), "")
                    tmp_word.name = f"T{tmp_word.id}"
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion = Quaternion(
                        "intofloat", src2_name, "_", tmp_word.name
                    )
                    self.quaternion_table.append(tmp_quaternion)
                    src2_name = tmp_word.name
                    tar_type = "float"
                else:
                    tar_type = src1_type

                tmp_word = Word(len(self.tmp_words_table), "")
                tmp_word.name = f"T{tmp_word.id}"
                tmp_word.type = tar_type
                self.tmp_words_table.append(tmp_word)

                tmp_quaternion = Quaternion()
                tmp_quaternion.op = tar_type + tmp_symbol_stack[1]["tree"]["content"]
                tmp_quaternion.src1 = src1_name
                tmp_quaternion.src2 = src2_name
                tmp_quaternion.tar = f"{tmp_word.name}"

                self.quaternion_table.append(tmp_quaternion)
                tmp.quad = len(self.quaternion_table)
                tmp.truelist.append(len(self.quaternion_table))
                tmp.falselist.append(len(self.quaternion_table) + 1)
            item["attribute"] = tmp

        # AddExpression -> AddExpression + AddExpression | AddExpression - AddExpression | FactorExpression
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "AddExpression"
        ):
            tmp = Attribute()
            if len(self.productions[production_id].to_ids) == 1:
                tmp.type = tmp_symbol_stack[0]["attribute"].type
                tmp.place = tmp_symbol_stack[0]["attribute"].place
                tmp.quad = tmp_symbol_stack[0]["attribute"].quad
                tmp.truelist = tmp_symbol_stack[0]["attribute"].truelist
                tmp.falselist = tmp_symbol_stack[0]["attribute"].falselist
            else:
                tmp.type = "tmp_word"  # tmp_word

                # 语义检查
                src1_type = (
                    "int"
                    if tmp_symbol_stack[0]["attribute"].type == "int"
                    else "float"
                    if tmp_symbol_stack[0]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[0]["attribute"].place).type
                    if tmp_symbol_stack[0]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[0]["attribute"].place
                    ].type
                )
                src2_type = (
                    "int"
                    if tmp_symbol_stack[2]["attribute"].type == "int"
                    else "float"
                    if tmp_symbol_stack[2]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[2]["attribute"].place).type
                    if tmp_symbol_stack[2]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[2]["attribute"].place
                    ].type
                )

                src1_name = (
                    str(tmp_symbol_stack[0]["tree"]["content"])
                    if tmp_symbol_stack[0]["attribute"].type == "int"
                    else str(tmp_symbol_stack[0]["tree"]["content"])
                    if tmp_symbol_stack[0]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[0]["attribute"].place).name
                    if tmp_symbol_stack[0]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[0]["attribute"].place
                    ].name
                )

                src2_name = (
                    str(tmp_symbol_stack[2]["tree"]["content"])
                    if tmp_symbol_stack[2]["attribute"].type == "int"
                    else str(tmp_symbol_stack[2]["tree"]["content"])
                    if tmp_symbol_stack[2]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[2]["attribute"].place).name
                    if tmp_symbol_stack[2]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[2]["attribute"].place
                    ].name
                )

                # 类型转换
                if src1_type == "int" and src2_type == "float":
                    tmp_word = Word(len(self.tmp_words_table), "")
                    tmp_word.name = f"T{tmp_word.id}"
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion = Quaternion(
                        "intofloat", src1_name, "_", tmp_word.name
                    )
                    self.quaternion_table.append(tmp_quaternion)
                    src1_name = tmp_word.name
                    tar_type = "float"
                elif src2_type == "int" and src1_type == "float":
                    tmp_word = Word(len(self.tmp_words_table), "")
                    tmp_word.name = f"T{tmp_word.id}"
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion = Quaternion(
                        "intofloat", src2_name, "_", tmp_word.name
                    )
                    self.quaternion_table.append(tmp_quaternion)
                    src2_name = tmp_word.name
                    tar_type = "float"
                else:
                    tar_type = src1_type

                tmp_word = Word()
                tmp_word.id = len(self.tmp_words_table)
                tmp_word.name = f"T{len(self.tmp_words_table)}"
                tmp_word.type = tar_type

                tmp.place = len(self.tmp_words_table)
                self.tmp_words_table.append(tmp_word)

                tmp_quaternion = Quaternion()
                tmp_quaternion.op = tar_type + tmp_symbol_stack[1]["tree"]["content"]
                tmp_quaternion.src1 = src1_name
                tmp_quaternion.src2 = src2_name
                tmp_quaternion.tar = tmp_word.name

                self.quaternion_table.append(tmp_quaternion)

                tmp.quad = len(self.quaternion_table)
                tmp.truelist.append(len(self.quaternion_table))
                tmp.falselist.append(len(self.quaternion_table) + 1)
            item["attribute"] = tmp

        # RelopExpression -> RelopExpression < RelopExpression | RelopExpression > RelopExpression | RelopExpression == RelopExpression | RelopExpression <= RelopExpression | RelopExpression >= RelopExpression | RelopExpression != RelopExpression | AddExpression
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "RelopExpression"
        ):
            tmp = Attribute()
            # RelopExpression -> AddExpression
            if len(self.productions[production_id].to_ids) == 1:
                tmp.type = tmp_symbol_stack[0]["attribute"].type
                tmp.place = tmp_symbol_stack[0]["attribute"].place
            else:
                tmp.type = "tmp_word"  # tmp_word
                tmp.place = len(self.tmp_words_table)

                tmp_word = Word(len(self.tmp_words_table), "")
                tmp_word.name = "T" + str(tmp_word.id)
                tmp_word.type = "int"  # int
                self.tmp_words_table.append(tmp_word)

                tmp_quaternion1 = Quaternion()
                tmp_quaternion1.op = "j" + tmp_symbol_stack[1]["tree"]["content"]
                tmp_quaternion1.src1 = (
                    str(tmp_symbol_stack[0]["tree"]["content"])
                    if tmp_symbol_stack[0]["attribute"].type == "int"
                    else str(tmp_symbol_stack[0]["tree"]["content"])
                    if tmp_symbol_stack[0]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[0]["attribute"].place).name
                    if tmp_symbol_stack[0]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[0]["attribute"].place
                    ].name
                )
                tmp_quaternion1.src2 = (
                    str(tmp_symbol_stack[2]["tree"]["content"])
                    if tmp_symbol_stack[2]["attribute"].type == "int"
                    else str(tmp_symbol_stack[2]["tree"]["content"])
                    if tmp_symbol_stack[2]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[2]["attribute"].place).name
                    if tmp_symbol_stack[2]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[2]["attribute"].place
                    ].name
                )
                tmp_quaternion1.tar = str(
                    len(self.quaternion_table) + self.start_address + 3
                )

                # 语义检查
                src1_type = (
                    "int"
                    if tmp_symbol_stack[0]["attribute"].type == "int"
                    else "float"
                    if tmp_symbol_stack[0]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[0]["attribute"].place).type
                    if tmp_symbol_stack[0]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[0]["attribute"].place
                    ].type
                )
                src2_type = (
                    "int"
                    if tmp_symbol_stack[2]["attribute"].type == "int"
                    else "float"
                    if tmp_symbol_stack[2]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[2]["attribute"].place).type
                    if tmp_symbol_stack[2]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[2]["attribute"].place
                    ].type
                )
                if src1_type != src2_type:
                    self.raise_error(
                        "Error",
                        loc,
                        f"变量类型不匹配：{tmp_quaternion1.src1}{tmp_symbol_stack[1]['tree']['content']}{tmp_quaternion1.src2}",
                    )

                self.quaternion_table.append(tmp_quaternion1)

                tmp_quaternion2 = Quaternion()
                tmp_quaternion2.op = "="
                tmp_quaternion2.src1 = "0"
                tmp_quaternion2.src2 = "_"
                tmp_quaternion2.tar = tmp_word.name
                self.quaternion_table.append(tmp_quaternion2)

                tmp_quaternion3 = Quaternion()
                tmp_quaternion3.op = "j"
                tmp_quaternion3.src1 = "_"
                tmp_quaternion3.src2 = "_"
                tmp_quaternion3.tar = str(
                    len(self.quaternion_table) + self.start_address + 2
                )
                self.quaternion_table.append(tmp_quaternion3)

                tmp_quaternion4 = Quaternion()
                tmp_quaternion4.op = "="
                tmp_quaternion4.src1 = "1"
                tmp_quaternion4.src2 = "_"
                tmp_quaternion4.tar = tmp_word.name
                self.quaternion_table.append(tmp_quaternion4)

                tmp.quad = len(self.quaternion_table)
            item["attribute"] = tmp

        # AssignStatement -> ID = RelopExpression ;
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "AssignStatement"
        ):
            tmp_quaternion = Quaternion()
            tmp_quaternion.op = "="
            tmp_quaternion.src2 = "_"

            tar_type = self.checkup_word_type(tmp_symbol_stack[0]["tree"]["content"])

            if tar_type is None:
                self.raise_error(
                    "Error",
                    loc,
                    f"{tmp_symbol_stack[0]['tree']['content']}: 未声明的标识符",
                )
            else:
                tmp_quaternion.tar = tmp_symbol_stack[0]["tree"]["content"]

            src_type = (
                "int"
                if tmp_symbol_stack[2]["attribute"].type == "int"
                else "float"
                if tmp_symbol_stack[2]["attribute"].type == "float"
                else self.checkup_word(tmp_symbol_stack[2]["attribute"].place).type
                if tmp_symbol_stack[2]["attribute"].type == "word"
                else self.tmp_words_table[tmp_symbol_stack[2]["attribute"].place].type
            )

            src_name = (
                tmp_symbol_stack[2]["tree"]["content"]
                if tmp_symbol_stack[2]["attribute"].type == "int"
                else tmp_symbol_stack[2]["tree"]["content"]
                if tmp_symbol_stack[2]["attribute"].type == "float"
                else self.tmp_words_table[tmp_symbol_stack[2]["attribute"].place].name
                if tmp_symbol_stack[2]["attribute"].type == "tmp_word"
                else self.checkup_word(tmp_symbol_stack[2]["attribute"].place).name
            )

            # 类型检查与转换
            if tar_type != src_type:
                tmp_word = Word(len(self.tmp_words_table), "")
                tmp_word.name = "T" + str(tmp_word.id)
                if tar_type == "int":
                    tmp_word.type = "int"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion2 = Quaternion(
                        "intoint", src_name, "_", tmp_word.name
                    )
                    self.quaternion_table.append(tmp_quaternion2)
                    src_name = tmp_word.name
                    self.raise_error(
                        "Warning", loc, f"从{src_type}转换到{tar_type}，可能丢失数据"
                    )
                elif tar_type == "float":
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion2 = Quaternion(
                        "intofloat", src_name, "_", tmp_word.name
                    )
                    self.quaternion_table.append(tmp_quaternion2)
                    src_name = tmp_word.name

            tmp_quaternion.src1 = src_name

            self.quaternion_table.append(tmp_quaternion)

            tmp = Attribute()
            tmp.quad = len(self.quaternion_table)
            item["attribute"] = tmp

        # Block -> { InnerStatement StatementString } |  { InnerStatement } |  { StatementString }
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "Block"
        ):
            tmp = Attribute()

            if len(self.productions[production_id].to_ids) == 4:
                # S.nextlist := L.nextlist
                tmp.nextlist = tmp_symbol_stack[2]["attribute"].nextlist
                tmp.has_return = tmp_symbol_stack[2]["attribute"].has_return
            elif tmp_symbol_stack[1]["tree"]["root"] == "StatementString":
                tmp.nextlist = tmp_symbol_stack[1]["attribute"].nextlist
                tmp.has_return = tmp_symbol_stack[1]["attribute"].has_return

            item["attribute"] = tmp

        # StatementString -> StatementString M Statement | Statement
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "StatementString"
        ):
            tmp = Attribute()
            # StatementString -> Statement
            if len(self.productions[production_id].to_ids) == 1:
                # L.nextlist := S.nextlist
                tmp.nextlist = tmp_symbol_stack[0]["attribute"].nextlist
                tmp.has_return = tmp_symbol_stack[0]["attribute"].has_return
            else:
                # backpatch(L1.nextlist, M.quad)
                for list_item in tmp_symbol_stack[0]["attribute"].nextlist:
                    self.quaternion_table[int(list_item)].tar = (
                        tmp_symbol_stack[1]["attribute"].quad + self.start_address
                    )
                # L.nextlist := S.nextlist
                tmp.nextlist = tmp_symbol_stack[2]["attribute"].nextlist
                tmp.has_return = tmp_symbol_stack[0]["attribute"].has_return or tmp_symbol_stack[2]["attribute"].has_return

            item["attribute"] = tmp
        
        # FunctionCallStatement -> FunctionCallExpression ;
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "FunctionCallStatement"
        ):
            item["attribute"] = Attribute()

        # Statement -> IfStatement | WhileStatement | ReturnStatement | AssignStatement | FunctionCallStatement
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "Statement"
        ):
            tmp = Attribute()
            tmp.nextlist = tmp_symbol_stack[0]["attribute"].nextlist
            tmp.has_return = tmp_symbol_stack[0]["attribute"].has_return
            item["attribute"] = tmp

        # M -> epsilon
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "M"
        ):
            tmp = Attribute()
            tmp.quad = len(self.quaternion_table)
            item["attribute"] = tmp

        # N -> epsilon
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "N"
        ):
            tmp = Attribute()
            tmp.nextlist.append(len(self.quaternion_table))
            tmp_quaternion = Quaternion("j", "_", "_", "0")
            self.quaternion_table.append(tmp_quaternion)
            item["attribute"] = tmp

        # A -> epsilon
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "A"
        ):
            tmp = Attribute()
            tmp.truelist.append(len(self.quaternion_table))
            tmp.falselist.append(len(self.quaternion_table) + 1)
            tmp_quaternion = Quaternion(
                "jnz", "_", "_", "0"
            )  # 判断条件待回填 地址待回填
            tmp_quaternion2 = Quaternion("j", "_", "_", "0")  # 跳转地址待回填
            self.quaternion_table.append(tmp_quaternion)
            self.quaternion_table.append(tmp_quaternion2)
            item["attribute"] = tmp

        # S -> epsilon
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "S"
        ):
            # 起始时插入跳转到main处的语句，待回填！
            tmp_quaternion = Quaternion("j", "_", "_", "_")
            self.quaternion_table.append(tmp_quaternion)

        # P -> epsilon
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "P"
        ):
            # 插入新的process
            self.create_process(
                start_address=len(self.quaternion_table) + self.start_address
            )

        # IfStatement -> if ( RelopExpression A ) M Block N else M Block | if ( RelopExpression A ) M Block
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "IfStatement"
        ):
            tmp = Attribute()

            # IfStatement -> if ( RelopExpression A ) M Block N else M Block
            if len(self.productions[production_id].to_ids) == 11:
                # backpatch (A.truelist, M1.quad)
                for list_item in tmp_symbol_stack[3]["attribute"].truelist:
                    self.quaternion_table[int(list_item)].src1 = (
                        tmp_symbol_stack[2]["tree"]["content"]
                        if tmp_symbol_stack[2]["attribute"].type == "int"
                        else tmp_symbol_stack[2]["tree"]["content"]
                        if tmp_symbol_stack[2]["attribute"].type == "float"
                        else self.tmp_words_table[
                            tmp_symbol_stack[2]["attribute"].place
                        ].name
                        if tmp_symbol_stack[2]["attribute"].type == "tmp_word"
                        else self.checkup_word(
                            tmp_symbol_stack[2]["attribute"].place
                        ).name
                    )
                    self.quaternion_table[int(list_item)].tar = str(
                        tmp_symbol_stack[5]["attribute"].quad + self.start_address
                    )

                # backpatch (A.falselist, M2.quad)
                for list_item in tmp_symbol_stack[3]["attribute"].falselist:
                    self.quaternion_table[int(list_item)].tar = str(
                        tmp_symbol_stack[9]["attribute"].quad + self.start_address
                    )

                # S.nextlist := merge(S1.nextlist, N.nextlist, S2.nextlist)
                tmp.nextlist = tmp_symbol_stack[6]["attribute"].nextlist
                tmp.nextlist += tmp_symbol_stack[7]["attribute"].nextlist
                tmp.nextlist += tmp_symbol_stack[10]["attribute"].nextlist

                # 两个出口都要求有return
                tmp.has_return = tmp_symbol_stack[6]["attribute"].has_return and tmp_symbol_stack[10]["attribute"].has_return

            # IfStatement -> if ( RelopExpression A ) M Block
            else:
                # backpatch (A.truelist, M.quad)
                for list_item in tmp_symbol_stack[3]["attribute"].truelist:
                    self.quaternion_table[int(list_item)].src1 = (
                        tmp_symbol_stack[2]["tree"]["content"]
                        if tmp_symbol_stack[2]["attribute"].type == "int"
                        else tmp_symbol_stack[2]["tree"]["content"]
                        if tmp_symbol_stack[2]["attribute"].type == "float"
                        else self.tmp_words_table[
                            tmp_symbol_stack[2]["attribute"].place
                        ].name
                        if tmp_symbol_stack[2]["attribute"].type == "tmp_word"
                        else self.checkup_word(
                            tmp_symbol_stack[2]["attribute"].place
                        ).name
                    )
                    self.quaternion_table[int(list_item)].tar = str(
                        tmp_symbol_stack[5]["attribute"].quad + self.start_address
                    )

                # S.nextlist := merge(A.falselist, S1.nextlist)
                tmp.nextlist = tmp_symbol_stack[3]["attribute"].falselist
                tmp.nextlist += tmp_symbol_stack[5]["attribute"].nextlist

            item["attribute"] = tmp

        # WhileStatement -> while M ( RelopExpression A ) M Block
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "WhileStatement"
        ):
            tmp = Attribute()
            # backpatch (S1.nextlist, M1.quad)
            for list_item in tmp_symbol_stack[6]["attribute"].falselist:
                self.quaternion_table[int(list_item)].tar = str(
                    tmp_symbol_stack[1]["attribute"].quad + self.start_address
                )

            # backpatch (A.truelist, M2.quad)
            for list_item in tmp_symbol_stack[4]["attribute"].truelist:
                self.quaternion_table[int(list_item)].src1 = (
                    tmp_symbol_stack[3]["tree"]["content"]
                    if tmp_symbol_stack[3]["attribute"].type == "int"
                    else tmp_symbol_stack[3]["tree"]["content"]
                    if tmp_symbol_stack[3]["attribute"].type == "float"
                    else self.tmp_words_table[
                        tmp_symbol_stack[3]["attribute"].place
                    ].name
                    if tmp_symbol_stack[3]["attribute"].type == "tmp_word"
                    else self.checkup_word(tmp_symbol_stack[3]["attribute"].place).name
                )
                self.quaternion_table[int(list_item)].tar = str(
                    tmp_symbol_stack[6]["attribute"].quad + self.start_address
                )

            # S.nextlist := A.falselist
            tmp.nextlist = tmp_symbol_stack[4]["attribute"].falselist

            # emit(j, _, _, M1.quad)
            tmp_quaternion = Quaternion()
            tmp_quaternion.op = "j"
            tmp_quaternion.src1 = "_"
            tmp_quaternion.src2 = "_"
            tmp_quaternion.tar = str(
                tmp_symbol_stack[1]["attribute"].quad + self.start_address
            )
            self.quaternion_table.append(tmp_quaternion)

            item["attribute"] = tmp

        # DeclarationType -> VarDeclaration | P FunctionDeclaration
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "DeclarationType"
        ):
            tmp = Attribute()

            # DeclarationType -> P FunctionDeclaration
            if len(self.productions[production_id].to_ids) == 2:
                tmp.declaration_type = "func"
                tmp.queue = tmp_symbol_stack[1]["attribute"].queue          # 向上传递参数列表
                tmp.nextlist = tmp_symbol_stack[1]["attribute"].nextlist
                tmp.has_return = tmp_symbol_stack[1]["attribute"].has_return
            # DeclarationType -> VarDeclaration
            else:
                tmp.declaration_type = "var"
            item["attribute"] = tmp

        # Declaration -> int identifier DeclarationType | float identifier DeclarationType | void identifier P FunctionDeclaration
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "Declaration"
        ):
            tmp = Attribute()
            # func ( void identifier P FunctionDeclaration )
            if len(self.productions[production_id].to_ids) == 4:
                func_name = tmp_symbol_stack[1]["tree"]["content"]
                if func_name in [func.name for func in self.process_table]:
                    self.raise_error("Error", loc, f"函数{func_name}已被定义")
                elif func_name == "main":
                    # 回填开始跳转到main入口的第一句
                    self.quaternion_table[0].tar = str(
                        self.process_table[-1].start_address
                    )
                    self.raise_error("Warning", loc, "main的返回类型应为int而非void")
                elif not tmp_symbol_stack[3]["attribute"].has_return:   # 其他函数没有return要多加上return
                    for list_item in tmp_symbol_stack[-1]["attribute"].nextlist:
                        self.quaternion_table[int(list_item)].tar = str(self.start_address + len(self.quaternion_table))
                        self.quaternion_table.append(Quaternion('ret', '_', '_', '_'))
                        
                self.process_table[-1].name = func_name
                self.process_table[-1].param = tmp_symbol_stack[3]["attribute"].queue
                self.process_table[-1].return_type = tmp_symbol_stack[0]["tree"]["content"]

                # 检查return语句是否有错
                if len(self.process_table[-1].actual_returns):
                    self.raise_error(
                        "Error",
                        self.process_table[-1].actual_returns[0][0],
                        f"返回值类型{self.process_table[-1].actual_returns[0][1]}与函数类型void不匹配",
                    )

            # func ( int / float )
            elif tmp_symbol_stack[2]["attribute"].declaration_type == "func":
                return_type = tmp_symbol_stack[0]["tree"]["content"]
                func_name = tmp_symbol_stack[1]["tree"]["content"]
                if func_name in [func.name for func in self.process_table]:
                    self.raise_error("Error", loc, f"函数{func_name}已被定义")
                elif func_name == "main":
                    # 回填开始跳转到main入口的第一句
                    self.quaternion_table[0].tar = str(
                        self.process_table[-1].start_address
                    )
                    if return_type == "int":
                        pass
                    else:
                        self.raise_error(
                            "Warning", loc, f"main的返回类型应为int而非{return_type}"
                        )
                elif len(self.process_table[-1].actual_returns) != 0 and not tmp_symbol_stack[2]["attribute"].has_return:   # 其他函数没有return
                    self.raise_error('Error', loc, f'{func_name}: 不是所有的控件路径都返回值')
                self.process_table[-1].name = func_name
                self.process_table[-1].param = tmp_symbol_stack[2]["attribute"].queue
                self.process_table[-1].return_type = return_type

                # 检查return语句是否有错
                if len(self.process_table[-1].actual_returns) == 0:
                    self.raise_error("Error", loc, f"函数{func_name}必须返回一个值")

                for actual_return in self.process_table[-1].actual_returns:
                    if actual_return[1] != self.process_table[-1].return_type:
                        self.raise_error(
                            "Error",
                            actual_return[0],
                            f"返回值类型{actual_return[1]}与函数类型{self.process_table[-1].return_type}不匹配",
                        )

            # var
            else:
                new_word = Word()
                new_word.id = len(self.words_table)
                new_word.name = tmp_symbol_stack[1]["tree"]["content"]
                new_word.type = tmp_symbol_stack[0]["tree"]["content"]
                self.words_table.append(new_word)

        # HeadVarStatements -> HeadVarStatements , VarStatement | VarStatement
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "HeadVarStatements"
        ):
            tmp = Attribute()
            if (
                self.non_terminal_symbols[
                    self.productions[production_id].to_ids[0]
                    - len(self.terminal_symbols)
                ]
                == "VarStatement"
            ):
                tmp.queue.append(tmp_symbol_stack[0]["attribute"].type)
            else:
                tmp.queue = tmp_symbol_stack[0]["attribute"].queue + [
                    tmp_symbol_stack[2]["attribute"].type
                ]
            item["attribute"] = tmp

        # FunctionDeclaration -> ( HeadVarStatements ) Block | ( ) Block | ( void ) Block
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "FunctionDeclaration"
        ):
            tmp = Attribute()
            # FunctionDeclaration -> ( HeadVarStatements ) Block
            if self.productions[production_id].to_ids[1] > len(self.terminal_symbols):
                tmp.queue = tmp_symbol_stack[1]["attribute"].queue

            tmp.nextlist = tmp_symbol_stack[-1]["attribute"].nextlist
            tmp.has_return = tmp_symbol_stack[-1]["attribute"].has_return

            item["attribute"] = tmp

        # Arguments -> Arguments , RelopExpression | RelopExpression
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "Arguments"
        ):
            tmp = Attribute()
            if (
                self.non_terminal_symbols[
                    self.productions[production_id].to_ids[0]
                    - len(self.terminal_symbols)
                ]
                == "RelopExpression"
            ):
                expression_name = (
                    str(tmp_symbol_stack[0]["tree"]["content"])
                    if tmp_symbol_stack[0]["attribute"].type == "int"
                    else str(tmp_symbol_stack[0]["tree"]["content"])
                    if tmp_symbol_stack[0]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[0]["attribute"].place).name
                    if tmp_symbol_stack[0]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[0]["attribute"].place
                    ].name
                )

                expression_type = (
                    "int"
                    if tmp_symbol_stack[0]["attribute"].type == "int"
                    else "float"
                    if tmp_symbol_stack[0]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[0]["attribute"].place).type
                    if tmp_symbol_stack[0]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[0]["attribute"].place
                    ].type
                )

                tmp.queue.append((expression_type, expression_name))

            elif len(self.productions[production_id].to_ids) > 1:
                expression_name = (
                    str(tmp_symbol_stack[2]["tree"]["content"])
                    if tmp_symbol_stack[2]["attribute"].type == "int"
                    else str(tmp_symbol_stack[2]["tree"]["content"])
                    if tmp_symbol_stack[2]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[2]["attribute"].place).name
                    if tmp_symbol_stack[2]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[2]["attribute"].place
                    ].name
                )

                expression_type = (
                    "int"
                    if tmp_symbol_stack[2]["attribute"].type == "int"
                    else "float"
                    if tmp_symbol_stack[2]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[2]["attribute"].place).type
                    if tmp_symbol_stack[2]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[2]["attribute"].place
                    ].type
                )
                tmp.queue = tmp_symbol_stack[0]["attribute"].queue + [
                    (expression_type, expression_name)
                ]

            item["attribute"] = tmp

        # FunctionCallExpression -> identifier ( Arguments ) | identifier ( )
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "FunctionCallExpression"
        ):
            tmp = Attribute()
            func_name = tmp_symbol_stack[0]["tree"]["content"]
            found = False
            for i, word in enumerate(self.process_table):
                if word.name == func_name:
                    found = True
                    break
            if not found:
                self.raise_error("Error", loc, f"函数{func_name}找不到标识符")
            else:
                func = self.process_table[i]
                # 含参
                if len(self.productions[production_id].to_ids) == 4:
                    queue = tmp_symbol_stack[2]["attribute"].queue
                    arg_queue = [item[1] for item in queue]
                    type_queue = [item[0] for item in queue]
                    # 这里不考虑类型转换了，不一样就报错
                    if type_queue != func.param:
                        self.raise_error(
                            "Error", loc, f"函数{func_name}调用与声明不匹配"
                        )

                    # param
                    for param in arg_queue:
                        tmp_quaternion = Quaternion("param", param, "_", "_")
                        self.quaternion_table.append(tmp_quaternion)
                # 无参
                else:
                    if len(self.process_table[i].param) != 0:
                        self.raise_error(
                            "Error", loc, f"函数{func_name}调用与声明不匹配"
                        )

                if func.return_type != "void":
                    new_word = Word()
                    new_word.id = len(self.tmp_words_table)
                    new_word.name = f"T{new_word.id}"
                    new_word.type = func.return_type
                    self.tmp_words_table.append(new_word)

                    tmp_quaternion = Quaternion(
                        "call", str(func.start_address), "_", new_word.name
                    )
                    self.quaternion_table.append(tmp_quaternion)
                    tmp.type = "tmp_word"
                    tmp.place = new_word.id
                else:
                    tmp_quaternion = Quaternion(
                        "call", str(func.start_address), "_", "_"
                    )
                    self.quaternion_table.append(tmp_quaternion)

            item["attribute"] = tmp

        # ReturnStatement -> return RelopExpression ; | return ;
        elif (
            self.non_terminal_symbols[
                self.productions[production_id].from_id - len(self.terminal_symbols)
            ]
            == "ReturnStatement"
        ):
            tmp = Attribute()
            tmp.has_return = True
            tmp_quaternion = Quaternion("ret", "_", "_", "_")

            # 不是很规范的写法，把返回值写在ret语句
            if len(self.productions[production_id].to_ids) == 3:
                tmp_quaternion.src1 = (
                    str(tmp_symbol_stack[1]["tree"]["content"])
                    if tmp_symbol_stack[1]["attribute"].type == "int"
                    else str(tmp_symbol_stack[1]["tree"]["content"])
                    if tmp_symbol_stack[1]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[1]["attribute"].place).name
                    if tmp_symbol_stack[1]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[1]["attribute"].place
                    ].name
                )

                ret_type = (
                    "int"
                    if tmp_symbol_stack[1]["attribute"].type == "int"
                    else "float"
                    if tmp_symbol_stack[1]["attribute"].type == "float"
                    else self.get_word(tmp_symbol_stack[1]["attribute"].place).type
                    if tmp_symbol_stack[1]["attribute"].type == "word"
                    else self.tmp_words_table[
                        tmp_symbol_stack[1]["attribute"].place
                    ].type
                )

                self.process_table[-1].actual_returns.append((loc, ret_type))

            self.quaternion_table.append(tmp_quaternion)

            item["attribute"] = tmp

    def getQuaternationTable(self):
        ret = [["地址", "四元式"]]
        for i, instr in enumerate(self.quaternion_table):
            ret.append([str(i + self.start_address), str(instr)])
        return ret
