from typing import List

class Attribute:
    def __init__(self):
        self.type = ""          # 值类型 int float word tmp_word
        self.place= None        # 如果是word/tmp_word，则存放在此处
        self.quad = None        # 下一条四元式位置
        self.truelist = []      # true条件跳转目标
        self.falselist = []     # false条件跳转目标
        self.nextlist = []      # 顺序执行下一目标
        self.queue = []         # 队列（用于函数参数）
        self.has_return = False # 是否有一个一定能执行到的return（用于错误分析）

    def __repr__(self):
        return f"<Attribute Object (Type:{self.type}, Place:{self.place}, Truelist:{self.truelist}, Falselist:{self.falselist}, Nextlist:{self.nextlist}, Quad:{self.quad})>"

'''
代码中声明的变量
'''
class Word:
    def __init__(self, id=0, name=""):
        self.id = id
        self.name = name
        self.type = ""

    def __eq__(self, other):
        if isinstance(other, Word):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            return False

    def __repr__(self):
        return f"<Word Object (ID:{self.id}, Name:{self.name}, Type:{self.type})>"

'''
四元式
'''
class Quaternion:
    def __init__(self, op="", src1="", src2="", tar=""):
        self.op = op
        self.src1 = src1
        self.src2 = src2
        self.tar = tar
        # 基本块划分后记录上待用与活跃信息
        self.info_src1 = None
        self.info_src2 = None
        self.info_tar  = None

    def __repr__(self):
        ret = f"({self.op}, {self.src1}, {self.src2}, {self.tar})".ljust(20)
        if self.info_src1 is not None:
            ret += f"\tsrc1{self.info_src1}"
        if self.info_src2 is not None:
            ret += f"\tsrc2{self.info_src2}"
        if self.info_tar is not None:
            ret += f"\ttar{self.info_tar}"
        return ret

'''
函数Process表项
'''
class Process:
    def __init__(self, start_address):
        self.name = ""
        self.return_type = ""
        self.actual_returns = []
        self.start_address = start_address
        self.words_table = []
        self.param = []

    def __repr__(self):
        return f"<Process Object (Name:{self.name}, Return Type:{self.return_type}, Start Address:{self.start_address}, Params:{self.param})>"


class Semantic:
    def __init__(self, productions, start_address=100):
        self.words_table = []                               # 全局变量
        self.tmp_words_table = []                           # 所有的临时变量
        self.process_table:List[Process] = []               # 记录函数的Process表
        self.quaternion_table = []                          # 生成四元式的表格
        self.productions = productions                      # 从Parser获取到的所有产生式
        self.start_address = start_address                  # 四元式开始地址默认为100）
        self.error_occur = False                            # 是否出错（出错则不再分析）
        self.error_msg = []                                 # 错误信息列表

    # 创建一个函数Process表项
    def createProcess(self, start_address):
        self.process_table.append(Process(start_address))

    # 在当前进程符号表中创建Word
    def createWord(self, word):
        proc_words_table = self.process_table[-1].words_table
        word.id = len(proc_words_table)
        proc_words_table.append(word)

    # 依次在当前进程符号表和全局变量符号表中查找Word并返回
    def getWord(self, word_name):
        proc_words_table = self.process_table[-1].words_table
        # 低层屏蔽高层，先在作用域内找
        if word_name in proc_words_table:
            return next((word for word in proc_words_table if word == word_name), None)
        # 寻找全局变量
        else:
            return next((word for word in self.words_table if word == word_name), None)

    # 根据attribute获取类型
    def getType(self, item):
        attr = item["attribute"]
        if attr.type in ["int", "float"] :
            return attr.type
        elif attr.type in ["word", "tmp_word"]:
            return attr.place.type

    # 获取名称（如果是常量，则就是字面量；如果是word，是对应的名称）
    def getName(self, item):
        if item["attribute"].type in ["int", "float"]:
            return str(item["content"])
        elif item["attribute"].type in ["word", "tmp_word"]:
            return item["attribute"].place.name

    # 记录错误信息（若为Error，之后不再进行语义分析）
    def raiseError(self, type, loc, msg):
        if type == "Error":
            self.error_occur = True
        self.error_msg.append(f"{type} at ({loc['row']},{loc['col']}): {msg}")

    # 进行一次语义分析
    # loc表示当前的定位，用于报错信息中的位置确认
    # item表示当前的语法分析树节点，用于获取当前节点的信息
    # rhs_list表示当前节点的子结点列表，即产生式的rhs
    def analyse(self, production_id, loc, item, rhs_list) -> None:
        # 已经有错误则不再分析了，否则可能导致语义分析程序出错
        if self.error_occur:
            return

        # VarStatement -> int ID | float ID
        if self.productions[production_id].lhs == "VarStatement":
            # 检查是否重复定义
            var_name = rhs_list[1]["content"]
            # 在当前函数的变量表才报错，全局变量允许低层屏蔽
            if var_name in self.process_table[-1].words_table:
                self.raiseError("Error", loc, f"变量{var_name}重定义")

            # 添加新的变量
            new_word = Word(name=var_name)
            new_word.type = self.productions[production_id].rhs[0]
            self.createWord(new_word)

            attr = Attribute()
            attr.type = new_word.type
            item["tree"]["attribute"] = attr

        # FactorExpression -> identifier | integer_constant | floating_point_constant
        # | ( RelopExpression ) | FactorExpression / FactorExpression | FactorExpression * FactorExpression | FunctionCallExpression
        elif self.productions[production_id].lhs == "FactorExpression":
            attr = Attribute()

            # FactorExpression -> FunctionCallExpression | identifier | integer_constant | floating_point_constant
            if len(self.productions[production_id].rhs) == 1:
                if self.productions[production_id].rhs[0] == "FunctionCallExpression":
                    ret_attr = rhs_list[0]["attribute"]
                    if ret_attr.type != "tmp_word":
                        self.raiseError("Error", loc, "void类型的操作数非法")
                    attr.type = ret_attr.type
                    attr.place = ret_attr.place

                elif self.productions[production_id].rhs[0] == "identifier":
                    var_name = rhs_list[0]["content"]
                    word = self.getWord(var_name)
                    if not word:
                        self.raiseError("Error", loc, f"{var_name}: 未声明的标识符")
                    attr.type = "word"
                    attr.place = word

                elif self.productions[production_id].rhs[0] == "integer_constant":  # integer_constant
                    attr.type = "int"

                else:  # floating_point_constant
                    attr.type = "float"

                attr.quad = len(self.quaternion_table)
                attr.truelist.append(len(self.quaternion_table))
                attr.falselist.append(len(self.quaternion_table) + 1)

            # FactorExpression -> ( RelopExpression )
            elif self.productions[production_id].rhs[0] == "(":
                attr = rhs_list[1]["attribute"]

            # FactorExpression -> FactorExpression / FactorExpression | FactorExpression * FactorExpression
            else:
                # 语义检查
                src1_type = self.getType(rhs_list[0])
                src2_type = self.getType(rhs_list[2])
                src1_name = self.getName(rhs_list[0])
                src2_name = self.getName(rhs_list[2])

                # 类型转换
                if src1_type == "int" and src2_type == "float":
                    tmp_word = Word(len(self.tmp_words_table), "")
                    tmp_word.name = f"T{tmp_word.id}"
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion = Quaternion("intofloat", src1_name, "_", tmp_word.name)
                    self.quaternion_table.append(tmp_quaternion)
                    src1_name = tmp_word.name
                    tar_type = "float"
                elif src2_type == "int" and src1_type == "float":
                    tmp_word = Word(len(self.tmp_words_table), "")
                    tmp_word.name = f"T{tmp_word.id}"
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion = Quaternion("intofloat", src2_name, "_", tmp_word.name)
                    self.quaternion_table.append(tmp_quaternion)
                    src2_name = tmp_word.name
                    tar_type = "float"
                else:
                    tar_type = src1_type
                
                tmp_word = Word(len(self.tmp_words_table), "")
                tmp_word.name = f"T{tmp_word.id}"
                tmp_word.type = tar_type
                self.tmp_words_table.append(tmp_word)

                tmp_quaternion = Quaternion("", src1_name, src2_name, tmp_word.name)
                tmp_quaternion.op = tar_type + rhs_list[1]["content"]
                self.quaternion_table.append(tmp_quaternion)

                attr.type = "tmp_word"
                attr.place = tmp_word
                attr.quad = len(self.quaternion_table)
                attr.truelist.append(len(self.quaternion_table))
                attr.falselist.append(len(self.quaternion_table) + 1)
            
            item["tree"]["attribute"] = attr

        # AddExpression -> AddExpression + AddExpression | AddExpression - AddExpression | FactorExpression
        elif self.productions[production_id].lhs == "AddExpression":
            attr = Attribute()
            # AddExpression -> FactorExpression
            if len(self.productions[production_id].rhs) == 1:
                attr = rhs_list[0]["attribute"]
                
            # AddExpression -> AddExpression + AddExpression | AddExpression - AddExpression
            else:
                attr.type = "tmp_word"  # tmp_word

                # 语义检查
                src1_type = self.getType(rhs_list[0])
                src2_type = self.getType(rhs_list[2])
                src1_name = self.getName(rhs_list[0])
                src2_name = self.getName(rhs_list[2])

                # 类型转换
                if src1_type == "int" and src2_type == "float":
                    tmp_word = Word(len(self.tmp_words_table), "")
                    tmp_word.name = f"T{tmp_word.id}"
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion = Quaternion("intofloat", src1_name, "_", tmp_word.name)
                    self.quaternion_table.append(tmp_quaternion)
                    src1_name = tmp_word.name
                    tar_type = "float"
                elif src2_type == "int" and src1_type == "float":
                    tmp_word = Word(len(self.tmp_words_table), "")
                    tmp_word.name = f"T{tmp_word.id}"
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion = Quaternion("intofloat", src2_name, "_", tmp_word.name)
                    self.quaternion_table.append(tmp_quaternion)
                    src2_name = tmp_word.name
                    tar_type = "float"
                else:
                    tar_type = src1_type

                tmp_word = Word()
                tmp_word.id = len(self.tmp_words_table)
                tmp_word.name = f"T{len(self.tmp_words_table)}"
                tmp_word.type = tar_type

                attr.place = tmp_word
                self.tmp_words_table.append(tmp_word)

                tmp_quaternion = Quaternion("", src1_name, src2_name, tmp_word.name)
                tmp_quaternion.op = tar_type + rhs_list[1]["content"]

                self.quaternion_table.append(tmp_quaternion)

                attr.quad = len(self.quaternion_table)
                attr.truelist.append(len(self.quaternion_table))
                attr.falselist.append(len(self.quaternion_table) + 1)
            item["tree"]["attribute"] = attr

        # RelopExpression -> RelopExpression < RelopExpression | RelopExpression > RelopExpression | RelopExpression == RelopExpression | RelopExpression <= RelopExpression | RelopExpression >= RelopExpression | RelopExpression != RelopExpression | AddExpression
        elif self.productions[production_id].lhs == "RelopExpression":
            attr = Attribute()

            # RelopExpression -> AddExpression
            if len(self.productions[production_id].rhs) == 1:
                attr = rhs_list[0]["attribute"]

            else:
                # 语义检查
                src1_type = self.getType(rhs_list[0])
                src2_type = self.getType(rhs_list[2])
                if src1_type != src2_type:
                    self.raiseError("Error", loc, f"变量类型不匹配：{tmp_quaternion1.src1}{rhs_list[1]['tree']['content']}{tmp_quaternion1.src2}")

                tmp_word = Word(len(self.tmp_words_table), "")
                tmp_word.name = "T" + str(tmp_word.id)
                tmp_word.type = "int"  # int
                self.tmp_words_table.append(tmp_word)

                tmp_quaternion1 = Quaternion(rhs_list[1]["content"], self.getName(rhs_list[0]), self.getName(rhs_list[2]), tmp_word.name)
                self.quaternion_table.append(tmp_quaternion1)

                attr.type = "tmp_word"
                attr.place = tmp_word
                attr.quad = len(self.quaternion_table)
            item["tree"]["attribute"] = attr

        # AssignStatement -> ID = RelopExpression ;
        elif self.productions[production_id].lhs == "AssignStatement":
            tmp_quaternion = Quaternion()
            tmp_quaternion.op = "="
            tmp_quaternion.src2 = "_"

            word = self.getWord(rhs_list[0]["content"])
            tar_type = word.type if word else None

            if tar_type is None:
                self.raiseError("Error", loc, f"{rhs_list[0]['content']}: 未声明的标识符")
            else:
                tmp_quaternion.tar = rhs_list[0]["content"]

            src_type = self.getType(rhs_list[2])
            src_name = self.getName(rhs_list[2])

            # 类型检查与转换
            if tar_type != src_type:
                tmp_word = Word(len(self.tmp_words_table), "")
                tmp_word.name = "T" + str(tmp_word.id)
                if tar_type == "int":
                    tmp_word.type = "int"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion2 = Quaternion("intoint", src_name, "_", tmp_word.name)
                    self.quaternion_table.append(tmp_quaternion2)
                    src_name = tmp_word.name
                    self.raiseError("Warning", loc, f"从{src_type}转换到{tar_type}，可能丢失数据")
                elif tar_type == "float":
                    tmp_word.type = "float"
                    self.tmp_words_table.append(tmp_word)
                    tmp_quaternion2 = Quaternion("intofloat", src_name, "_", tmp_word.name)
                    self.quaternion_table.append(tmp_quaternion2)
                    src_name = tmp_word.name

            tmp_quaternion.src1 = src_name
            self.quaternion_table.append(tmp_quaternion)

            attr = Attribute()
            attr.quad = len(self.quaternion_table)
            item["tree"]["attribute"] = attr

        # Block -> { InnerStatement StatementString } |  { InnerStatement } |  { StatementString }
        elif self.productions[production_id].lhs == "Block":
            attr = Attribute()

            # Block -> { InnerStatement StatementString }
            if len(self.productions[production_id].rhs) == 4:
                # S.nextlist := L.nextlist
                attr.nextlist = rhs_list[2]["attribute"].nextlist
                attr.has_return = rhs_list[2]["attribute"].has_return
            elif self.productions[production_id].rhs[1] == "StatementString":
                attr.nextlist = rhs_list[1]["attribute"].nextlist
                attr.has_return = rhs_list[1]["attribute"].has_return

            item["tree"]["attribute"] = attr

        # StatementString -> StatementString M Statement | Statement
        elif self.productions[production_id].lhs == "StatementString":
            attr = Attribute()
            # StatementString -> Statement
            if len(self.productions[production_id].rhs) == 1:
                # L.nextlist := S.nextlist
                attr.nextlist = rhs_list[0]["attribute"].nextlist
                attr.has_return = rhs_list[0]["attribute"].has_return
            else:
                # backpatch(L1.nextlist, M.quad)
                for list_item in rhs_list[0]["attribute"].nextlist:
                    self.quaternion_table[int(list_item)].tar = (rhs_list[1]["attribute"].quad + self.start_address)
                # L.nextlist := S.nextlist
                attr.nextlist = rhs_list[2]["attribute"].nextlist
                attr.has_return = rhs_list[0]["attribute"].has_return or rhs_list[2]["attribute"].has_return

            item["tree"]["attribute"] = attr
        
        # FunctionCallStatement -> FunctionCallExpression ;
        elif self.productions[production_id].lhs == "FunctionCallStatement":
            item["tree"]["attribute"] = Attribute()

        # Statement -> IfStatement | WhileStatement | ReturnStatement | AssignStatement | FunctionCallStatement
        elif self.productions[production_id].lhs == "Statement":
            attr = Attribute()
            attr.nextlist = rhs_list[0]["attribute"].nextlist
            attr.has_return = rhs_list[0]["attribute"].has_return
            item["tree"]["attribute"] = attr

        # M -> epsilon
        elif self.productions[production_id].lhs == "M":
            attr = Attribute()
            attr.quad = len(self.quaternion_table)
            item["tree"]["attribute"] = attr

        # N -> epsilon
        elif self.productions[production_id].lhs == "N":
            attr = Attribute()
            attr.nextlist.append(len(self.quaternion_table))
            tmp_quaternion = Quaternion("j", "_", "_", "0")
            self.quaternion_table.append(tmp_quaternion)
            item["tree"]["attribute"] = attr

        # A -> epsilon
        elif self.productions[production_id].lhs == "A":
            attr = Attribute()
            attr.truelist.append(len(self.quaternion_table))
            attr.falselist.append(len(self.quaternion_table) + 1)
            tmp_quaternion = Quaternion("jnz", "_", "_", "0")  # 判断条件待回填 地址待回填
            tmp_quaternion2 = Quaternion("j", "_", "_", "0")   # 跳转地址待回填
            self.quaternion_table.append(tmp_quaternion)
            self.quaternion_table.append(tmp_quaternion2)
            item["tree"]["attribute"] = attr

        # S -> epsilon
        elif self.productions[production_id].lhs == "S":
            pass
            # 起始时插入跳转到main处的语句，待回填！（交给目标代码生成完成）
            # tmp_quaternion = Quaternion("j", "_", "_", "_")
            # self.quaternion_table.append(tmp_quaternion)

        # P -> epsilon
        elif self.productions[production_id].lhs == "P":
            # 插入新的process
            self.createProcess(start_address=len(self.quaternion_table) + self.start_address)

        # IfStatement -> if ( RelopExpression A ) M Block N else M Block | if ( RelopExpression A ) M Block
        elif self.productions[production_id].lhs == "IfStatement":
            attr = Attribute()

            # IfStatement -> if ( RelopExpression A ) M Block N else M Block
            if len(self.productions[production_id].rhs) == 11:
                # backpatch (A.truelist, M1.quad)
                for list_item in rhs_list[3]["attribute"].truelist:
                    self.quaternion_table[int(list_item)].src1 = self.getName(rhs_list[2])
                    self.quaternion_table[int(list_item)].tar = str(rhs_list[5]["attribute"].quad + self.start_address)

                # backpatch (A.falselist, M2.quad)
                for list_item in rhs_list[3]["attribute"].falselist:
                    self.quaternion_table[int(list_item)].tar = str(rhs_list[9]["attribute"].quad + self.start_address)

                # S.nextlist := merge(S1.nextlist, N.nextlist, S2.nextlist)
                attr.nextlist = rhs_list[6]["attribute"].nextlist
                attr.nextlist += rhs_list[7]["attribute"].nextlist
                attr.nextlist += rhs_list[10]["attribute"].nextlist

                # 两个出口都要求有return
                attr.has_return = rhs_list[6]["attribute"].has_return and rhs_list[10]["attribute"].has_return

            # IfStatement -> if ( RelopExpression A ) M Block
            else:
                # backpatch (A.truelist, M.quad)
                for list_item in rhs_list[3]["attribute"].truelist:
                    self.quaternion_table[int(list_item)].src1 = self.getName(rhs_list[2])
                    self.quaternion_table[int(list_item)].tar = str(rhs_list[5]["attribute"].quad + self.start_address)

                # S.nextlist := merge(A.falselist, S1.nextlist)
                attr.nextlist = rhs_list[3]["attribute"].falselist
                attr.nextlist += rhs_list[5]["attribute"].nextlist

            item["tree"]["attribute"] = attr

        # WhileStatement -> while M ( RelopExpression A ) M Block
        elif self.productions[production_id].lhs == "WhileStatement":
            attr = Attribute()
            # backpatch (S1.nextlist, M1.quad)
            for list_item in rhs_list[6]["attribute"].falselist:
                self.quaternion_table[int(list_item)].tar = str(rhs_list[1]["attribute"].quad + self.start_address)

            # backpatch (A.truelist, M2.quad)
            for list_item in rhs_list[4]["attribute"].truelist:
                self.quaternion_table[int(list_item)].src1 = self.getName(rhs_list[3])
                self.quaternion_table[int(list_item)].tar = str(rhs_list[6]["attribute"].quad + self.start_address)

            # S.nextlist := A.falselist
            attr.nextlist = rhs_list[4]["attribute"].falselist

            # emit(j, _, _, M1.quad)
            tmp_quaternion = Quaternion("j", "_", "_", "")
            tmp_quaternion.tar = str(rhs_list[1]["attribute"].quad + self.start_address)
            self.quaternion_table.append(tmp_quaternion)

            item["tree"]["attribute"] = attr

        # DeclarationType -> VarDeclaration | P FunctionDeclaration
        elif self.productions[production_id].lhs == "DeclarationType":
            attr = Attribute()

            # DeclarationType -> P FunctionDeclaration
            if len(self.productions[production_id].rhs) == 2:
                attr.declaration_type = "func"
                attr.queue = rhs_list[1]["attribute"].queue          # 向上传递参数列表
                attr.nextlist = rhs_list[1]["attribute"].nextlist
                attr.has_return = rhs_list[1]["attribute"].has_return
            # DeclarationType -> VarDeclaration
            else:
                attr.declaration_type = "var"
            item["tree"]["attribute"] = attr

        # Declaration -> int identifier DeclarationType | float identifier DeclarationType | void identifier P FunctionDeclaration
        elif self.productions[production_id].lhs == "Declaration":
            attr = Attribute()
            # func ( void identifier P FunctionDeclaration )
            if len(self.productions[production_id].rhs) == 4:
                func_name = rhs_list[1]["content"]
                if func_name in [func.name for func in self.process_table]:
                    self.raiseError("Error", loc, f"函数{func_name}已被定义")
                elif func_name == "main":
                    # 回填开始跳转到main入口的第一句（现在不做，目标代码生成时再指定）
                    # self.quaternion_table[0].tar = str(self.process_table[-1].start_address)
                    self.raiseError("Warning", loc, "main的返回类型应为int而非void")
                # 其他函数没有return要多加上return
                elif not rhs_list[3]["attribute"].has_return:   
                    for list_item in rhs_list[-1]["attribute"].nextlist:
                        self.quaternion_table[int(list_item)].tar = str(self.start_address + len(self.quaternion_table))
                    self.quaternion_table.append(Quaternion('ret', '_', '_', '_'))
                
                # process表中补充函数信息
                self.process_table[-1].name = func_name
                self.process_table[-1].param = rhs_list[3]["attribute"].queue
                self.process_table[-1].return_type = rhs_list[0]["content"]

                # 检查return语句是否有错
                if len(self.process_table[-1].actual_returns):
                    self.raiseError("Error", self.process_table[-1].actual_returns[0][0],
                                      f"返回值类型{self.process_table[-1].actual_returns[0][1]}与函数类型void不匹配")

            # func ( int / float )
            elif rhs_list[2]["attribute"].declaration_type == "func":
                return_type = rhs_list[0]["content"]
                func_name = rhs_list[1]["content"]
                if func_name in [func.name for func in self.process_table]:
                    self.raiseError("Error", loc, f"函数{func_name}已被定义")
                elif func_name == "main":
                    # 回填开始跳转到main入口的第一句（现在不做，目标代码生成时再指定）
                    # self.quaternion_table[0].tar = str(self.process_table[-1].start_address)
                    if return_type == "int":
                        pass
                    else:
                        self.raiseError("Warning", loc, f"main的返回类型应为int而非{return_type}")
                # 其他函数没有return
                elif len(self.process_table[-1].actual_returns) != 0 and not rhs_list[2]["attribute"].has_return:   
                    self.raiseError('Error', loc, f'{func_name}: 不是所有的控件路径都返回值')
                self.process_table[-1].name = func_name
                self.process_table[-1].param = rhs_list[2]["attribute"].queue
                self.process_table[-1].return_type = return_type

                # 检查return语句是否有错
                if len(self.process_table[-1].actual_returns) == 0:
                    self.raiseError("Error", loc, f"函数{func_name}必须返回一个值")

                for actual_return in self.process_table[-1].actual_returns:
                    if actual_return[1] != self.process_table[-1].return_type:
                        self.raiseError("Error", actual_return[0],
                                         f"返回值类型{actual_return[1]}与函数类型{self.process_table[-1].return_type}不匹配")

            # var（声明全局变量）
            else:
                new_word = Word()
                new_word.id = len(self.words_table)
                new_word.name = rhs_list[1]["content"]
                new_word.type = rhs_list[0]["content"]
                self.words_table.append(new_word)

        # HeadVarStatements -> HeadVarStatements , VarStatement | VarStatement
        elif self.productions[production_id].lhs == "HeadVarStatements":
            attr = Attribute()
            # HeadVarStatements -> VarStatement
            if self.productions[production_id].rhs[0] == "VarStatement":
                attr.queue.append(rhs_list[0]["attribute"].type)
            # HeadVarStatements -> HeadVarStatements , VarStatement
            else:
                attr.queue = rhs_list[0]["attribute"].queue + [rhs_list[2]["attribute"].type]
            item["tree"]["attribute"] = attr

        # FunctionDeclaration -> ( HeadVarStatements ) Block | ( ) Block | ( void ) Block
        elif self.productions[production_id].lhs == "FunctionDeclaration":
            attr = Attribute()
            # FunctionDeclaration -> ( HeadVarStatements ) Block
            if self.productions[production_id].rhs[1] == "HeadVarStatements":
                attr.queue = rhs_list[1]["attribute"].queue

            attr.nextlist = rhs_list[-1]["attribute"].nextlist
            attr.has_return = rhs_list[-1]["attribute"].has_return

            item["tree"]["attribute"] = attr

        # Arguments -> Arguments , RelopExpression | RelopExpression
        elif self.productions[production_id].lhs == "Arguments":
            attr = Attribute()

            # Arguments -> RelopExpression
            if self.productions[production_id].rhs[0] == "RelopExpression":
                expression_name = self.getName(rhs_list[0])
                expression_type = self.getType(rhs_list[0])
                attr.queue.append((expression_type, expression_name))
            # Arguments -> Arguments , RelopExpression
            elif len(self.productions[production_id].rhs) > 1:
                expression_name = self.getName(rhs_list[2])
                expression_type = self.getType(rhs_list[2])
                attr.queue = rhs_list[0]["attribute"].queue + [(expression_type, expression_name)]

            item["tree"]["attribute"] = attr

        # FunctionCallExpression -> identifier ( Arguments ) | identifier ( )
        elif self.productions[production_id].lhs == "FunctionCallExpression":
            attr = Attribute()
            func_name = rhs_list[0]["content"]
            func = next((func for func in self.process_table if func.name == func_name), None)
            if not func:
                self.raiseError("Error", loc, f"函数{func_name}找不到标识符")
            else:
                # 含参
                if len(self.productions[production_id].rhs) == 4:
                    queue = rhs_list[2]["attribute"].queue
                    arg_queue = [item[1] for item in queue]
                    type_queue = [item[0] for item in queue]
                    # 这里不考虑类型转换了，不一样就报错
                    if type_queue != func.param:
                        self.raiseError("Error", loc, f"函数{func_name}调用与声明不匹配")
                    # param
                    for param in arg_queue:
                        tmp_quaternion = Quaternion("param", param, "_", "_")
                        self.quaternion_table.append(tmp_quaternion)
                # 无参
                else:
                    if len(func.param) != 0:
                        self.raiseError("Error", loc, f"函数{func_name}调用与声明不匹配")

                if func.return_type != "void":
                    new_word = Word()
                    new_word.id = len(self.tmp_words_table)
                    new_word.name = f"T{new_word.id}"
                    new_word.type = func.return_type
                    self.tmp_words_table.append(new_word)
                    
                    # 这里四元式直接跳转到函数名称，方便目标代码生成使用jal
                    tmp_quaternion = Quaternion("call", func_name, "_", new_word.name)
                    self.quaternion_table.append(tmp_quaternion)
                    attr.type = "tmp_word"
                    attr.place = new_word
                else:
                    tmp_quaternion = Quaternion("call", func_name, "_", "_")
                    self.quaternion_table.append(tmp_quaternion)

            item["tree"]["attribute"] = attr

        # ReturnStatement -> return RelopExpression ; | return ;
        elif self.productions[production_id].lhs == "ReturnStatement":
            attr = Attribute()
            attr.has_return = True
            tmp_quaternion = Quaternion("ret", "_", "_", "_")

            # 不是很规范的写法，把返回值写在ret语句
            if len(self.productions[production_id].rhs) == 3:
                tmp_quaternion.src1 = self.getName(rhs_list[1])
                ret_type = self.getType(rhs_list[1])
                self.process_table[-1].actual_returns.append((loc, ret_type))

            self.quaternion_table.append(tmp_quaternion)

            item["tree"]["attribute"] = attr

    def getFuncTable(self):
        return [{"name": proc.name, "enter": proc.start_address} for proc in self.process_table]

    def getQuaternationTable(self):
        ret = [["地址", "四元式"]]
        for i, instr in enumerate(self.quaternion_table):
            ret.append([str(i + self.start_address), str(instr)])
        return ret
