import re
import os
import json
from tokenType import tokenType_to_terminal
from mySemantic import Semantic

ACTION_ACC = 0
ACTION_S = 1
ACTION_R = 2
ActionType = ["acc", "s", "r"]


class Production:
    def __init__(self):
        self.cnt = 0
        self.from_id = 0
        self.to_ids = []

    def __lt__(self, other):
        return self.cnt < other.cnt


class Item:
    def __init__(self, production_id, dot_pos, terminal_id):
        self.production_id = production_id  # 产生式编号
        self.dot_pos = dot_pos  # 点的位置
        self.terminal_id = terminal_id  # 终结符ID

    def __lt__(self, other):
        return (self.production_id, self.dot_pos, self.terminal_id) < (
            other.production_id,
            other.dot_pos,
            other.terminal_id,
        )

    def __eq__(self, other):
        return (self.production_id, self.dot_pos, self.terminal_id) == (
            other.production_id,
            other.dot_pos,
            other.terminal_id,
        )


class Closure:
    def __init__(self):
        self.cnt = 0  # 编号
        self.items = []  # 项目集

    def __lt__(self, other):
        return self.cnt < other.cnt

    def __eq__(self, other):
        t1 = sorted(self.items)
        t2 = sorted(other.items)
        if len(t1) != len(t2):
            return False
        for i in range(len(t1)):
            if t1[i] != t2[i]:
                return False
        return True


class Parser:
    def __init__(self):
        self.terminal_symbols = [
            "int",
            "float",
            "void",
            "if",
            "else",
            "while",
            "return",
            "identifier",
            "integer_constant",
            "floating_point_constant",
            "=",
            "+=",
            "-=",
            "*=",
            "/=",
            "%=",
            ">>=",
            "<<=",
            "+",
            "-",
            ">>",
            "<<",
            "*",
            "/",
            "%",
            "==",
            ">",
            ">=",
            "<",
            "<=",
            "!=",
            ";",
            ",",
            "(",
            ")",
            "{",
            "}",
            "#",
        ]
        self.non_terminal_symbols = ["epsilon"]
        self.firsts = []
        self.productions = []
        self.closures = []
        self.gos = []
        self.goto_table = []
        self.action_table = []
        self.lr1_analysis_table = []

        self.read_productions()
        if not os.path.exists("cache"):
            os.makedirs("cache")
        # 文件的完整路径
        action_file_path = os.path.join("cache", "actiontable.json")
        goto_file_path = os.path.join("cache", "gototable.json")
        # 检查文件是否存在，如果不存在则创建并写入内容
        flag = False
        if not os.path.exists(action_file_path):
            with open(action_file_path, "w") as file:
                self.find_firsts()
                self.find_gos()
                self.find_gotos()
                flag = True
                json.dump(self.action_table, file, ensure_ascii=False)
                # file.write(file_content)
        with open(action_file_path, "r") as file:
            self.action_table = json.load(file)

        if not os.path.exists(goto_file_path):
            with open(goto_file_path, "w") as file:
                if not flag:
                    self.find_firsts()
                    self.find_gos()
                    self.find_gotos()
                json.dump(self.goto_table, file, ensure_ascii=False)
        with open(goto_file_path, "r") as file:
            self.goto_table = json.load(file)

        self.semantic_quaternation = []
        self.semantic_error_occur = False
        self.semantic_error_message = []

    # 根据symbol获取对应的id
    def get_id_by_str(self, symbol: str) -> int:
        try:
            return self.terminal_symbols.index(symbol)
        except BaseException:
            try:
                return self.non_terminal_symbols.index(symbol)
            except BaseException:
                assert Exception("Invalid symbol!")

    def get_str_by_id(self, cnt: int) -> str:
        if 0 <= cnt < len(self.terminal_symbols):
            return self.terminal_symbols[cnt]
        elif cnt < len(self.terminal_symbols) + len(self.non_terminal_symbols):
            return self.non_terminal_symbols[cnt - len(self.terminal_symbols)]
        else:
            assert Exception("Invalid terminal cnt!")

    def read_productions(self, filename="Productions.cfg"):
        # 读取产生式配置文件
        """
        从产生式配置文件中读取产生式规则。

        参数：
        - filename: 产生式配置文件的路径，默认为"production.cfg"。

        返回：
        - success: 如果成功读取配置文件并处理产生式规则，则返回True；如果文件不存在，返回False。
        """
        try:
            with open(filename, "r") as fin:  # 打开配置文件进行读取
                for line in fin.readlines():  # 逐行读取文件内容
                    tmp = None
                    match = re.match(
                        r"\s*([^->]+)\s*->\s*(.*)", line
                    )  # 用正则表达式匹配产生式规则的格式
                    if match:
                        left_side = match.group(
                            1
                        ).strip()  # 获取产生式左侧（非终结符）并去除空格
                        right_side = match.group(
                            2
                        ).strip()  # 获取产生式右侧（可能包含多个替代项）并去除空格
                        alternatives = [
                            alt.strip() for alt in right_side.split("|")
                        ]  # 将右侧的替代项分割成列表

                        # 处理非终结符
                        if left_side not in self.non_terminal_symbols:
                            self.non_terminal_symbols.append(left_side)

                        from_id = self.non_terminal_symbols.index(left_side) + len(
                            self.terminal_symbols
                        )  # 计算产生式左侧非终结符的索引

                        # 处理每个替代项
                        for alt in alternatives:
                            tmp = Production()
                            tmp.cnt = len(self.productions)
                            tmp.from_id = from_id

                            # 处理替代项中的每个符号
                            alt_split = [x for x in alt.split(" ")]
                            for symbol in alt_split:
                                if symbol in self.terminal_symbols:
                                    to_id = self.terminal_symbols.index(symbol)
                                elif symbol in self.non_terminal_symbols:
                                    to_id = self.non_terminal_symbols.index(
                                        symbol
                                    ) + len(self.terminal_symbols)
                                else:
                                    # 如果符号不是终结符也不是非终结符，将其添加到非终结符列表中
                                    self.non_terminal_symbols.append(symbol)
                                    to_id = self.non_terminal_symbols.index(
                                        symbol
                                    ) + len(self.terminal_symbols)

                                tmp.to_ids.append(
                                    to_id
                                )  # 将产生式右侧每个符号的索引添加到产生式对象的to_ids列表中

                            self.productions.append(
                                tmp
                            )  # 将产生式对象添加到产生式列表中
        except FileNotFoundError:
            return False  # 如果文件不存在，返回False
        return True  # 如果成功读取配置文件并处理产生式规则，返回True

    def find_firsts(self):
        # 找first集的实现
        """
        计算文法的First集合。

        First集合是文法中每个非终结符的一个集合，包含其能推导出的所有可能的首终结符（终结符或epsilon）。

        返回：无，直接更新self.firsts列表。

        注意：
        - self.terminal_symbols: 终结符列表
        - self.non_terminal_symbols: 非终结符列表
        - self.productions: 产生式规则列表
        - self.firsts: 存储First集合的列表，每个元素是一个集合，对应一个非终结符的First集合。
        """
        # 初始化终结符
        for i in range(len(self.terminal_symbols)):
            self.firsts.append({i})
        # 初始化非终结符
        for i in range(len(self.terminal_symbols)):
            self.firsts.append(set())
        flag = False  # 判断在一次循环中是否有新的元素加入了first集合
        while True:
            flag = False
            for production in self.productions:
                from_id = production.from_id
                for i in range(len(production.to_ids)):
                    if production.to_ids[i] <= len(
                        self.terminal_symbols
                    ):  # 是终结符或epsilon
                        if (
                            production.to_ids[i] not in self.firsts[from_id]
                        ):  # 不在first集中
                            flag = True
                            self.firsts[from_id].add(production.to_ids[i])
                        break
                    else:
                        for cnt in self.firsts[production.to_ids[i]]:
                            if (
                                cnt != len(self.terminal_symbols)
                                and cnt not in self.firsts[from_id]
                            ):  # 以前没放进去
                                flag = True
                                self.firsts[from_id].add(cnt)
                        if (
                            len(self.terminal_symbols)
                            not in self.firsts[production.to_ids[i]]
                        ):  # epsilon不在非终结符的first集中
                            break
                        elif (
                            i == len(production.to_ids) - 1
                            and len(self.terminal_symbols) not in self.firsts[from_id]
                        ):  # 本次是最后一次，且epsilon以前没放进去
                            flag = True
                            self.firsts[from_id].add(len(self.terminal_symbols))
            if not flag:
                break

    def find_firsts_alpha(self, alpha, firsts):
        """
        找句子的First集合。

        参数：
        - alpha: 包含整数的列表，表示句子中的符号序列。
        - firsts: 用于存储句子First集合的集合，该集合将被清空并更新。

        注意：
        - self.firsts: 存储文法非终结符First集合的列表。
        - self.terminal_symbols: 终结符列表。
        """
        firsts.clear()  # 清空传入的firsts集合

        for i in range(len(alpha)):
            for cnt in self.firsts[alpha[i]]:
                if cnt != len(self.terminal_symbols):
                    firsts.add(cnt)  # 将文法非终结符的First集合添加到句子First集合中
            if len(self.terminal_symbols) not in self.firsts[alpha[i]]:
                break  # 如果epsilon不在当前符号的First集合中，终止循环
            if (
                i == len(alpha) - 1
                and len(self.terminal_symbols) in self.firsts[alpha[i]]
            ):
                firsts.add(
                    len(self.terminal_symbols)
                )  # 如果是句子的最后一个符号，并且epsilon在其First集合中，添加epsilon到句子First集合中

    def find_closures(self, closure):
        """
        找闭包的实现，若有项目[A→α·Bβ,a ]属于CLOSURE(I)，B→γ是文法中的产生式，β∈V*，b∈FIRST(βa)，则[B→·γ,b]也属于CLOSURE(I)中。

        参数：
        - closure: 闭包对象，其中包含项目的集合。

        注意：
        - self.productions: 存储文法产生式的列表。
        - self.terminal_symbols: 存储终结符的列表。
        """
        # 对于给定闭包中的每个项目
        i = 0
        while i < len(closure.items):
            # 如果项目的点位置已经到达产生式右侧的末尾，跳过
            if closure.items[i].dot_pos >= len(
                self.productions[closure.items[i].production_id].to_ids
            ):
                i += 1
                continue
            # 获取项目点后的符号的 ID
            symbol_id = self.productions[closure.items[i].production_id].to_ids[
                closure.items[i].dot_pos
            ]
            # 如果该符号是终结符或epsilon，跳过
            if symbol_id <= len(self.terminal_symbols):
                i += 1
                continue
            # 对于每个产生式
            for j in range(len(self.productions)):
                # 如果产生式的左侧是当前符号 ID
                if self.productions[j].from_id == symbol_id:
                    # 创建新的项目
                    alpha = []
                    # 从当前产生式符号的下一个开始遍历，如果不是epsilon
                    for k in range(
                        closure.items[i].dot_pos + 1,
                        len(self.productions[closure.items[i].production_id].to_ids),
                    ):
                        if self.productions[closure.items[i].production_id].to_ids[
                            k
                        ] != len(self.terminal_symbols):
                            alpha.append(
                                self.productions[closure.items[i].production_id].to_ids[
                                    k
                                ]
                            )
                    alpha.append(closure.items[i].terminal_id)
                    # 计算后继符号的first集
                    firsts = set()
                    self.find_firsts_alpha(alpha, firsts)
                    # 对于每个first集合中的符号，创建新的项目并加入闭包
                    for first in firsts:
                        item = Item(j, 0, first)
                        if item not in closure.items:
                            closure.items.append(item)
            i += 1

    def find_gos(self):
        """
        找Go表的实现。

        注意：
        - self.productions: 存储文法产生式的列表。
        - self.terminal_symbols: 存储终结符的列表。
        - self.non_terminal_symbols: 存储非终结符的列表。
        - self.closures: 存储闭包的列表。
        - self.gos: 存储Go表的列表，每个元素是一个字典，表示一个闭包的后继闭包及其映射。
        """
        # 创建新的产生式 S'->Program，并将其添加到产生式列表中
        new_production = Production()
        new_production.cnt = len(self.productions)
        new_production.from_id = len(self.terminal_symbols) + len(
            self.non_terminal_symbols
        )  # S
        new_production.to_ids.append(len(self.terminal_symbols) + 1)  # Program
        self.productions.append(new_production)  # S -> Program

        # 创建初始项，表示S->.Program,#
        new_item = Item(len(self.productions) - 1, 0, len(self.terminal_symbols) - 1)

        # 创建初始闭包，包含初始项
        start_closure = Closure()
        start_closure.items.append(new_item)

        # 找初始闭包的闭包
        self.find_closures(start_closure)

        # 将初始闭包及其映射加入闭包列表和映射列表
        self.closures.append(start_closure)
        self.gos.append({})

        # 初始化当前闭包标识
        now_closure_id = 0

        # 遍历闭包列表，构建闭包的后继闭包及其映射
        while now_closure_id < len(self.closures):
            # 遍历所有终结符和非终结符的编号
            for i in range(
                len(self.terminal_symbols) + len(self.non_terminal_symbols) + 1
            ):
                if i == len(self.terminal_symbols):  # epsilon
                    continue

                # 创建新的闭包
                tmp = Closure()

                # 遍历当前闭包中的每个项
                for item in self.closures[now_closure_id].items:
                    # 如果项的点位置已经到达产生式右侧的末尾，跳过
                    if len(self.productions[item.production_id].to_ids) == item.dot_pos:
                        continue

                    # 如果产生式右侧的下一位符号的编号是当前遍历的编号
                    if self.productions[item.production_id].to_ids[item.dot_pos] == i:
                        # 创建新的项，表示将点向后移动一位
                        new_item = Item(
                            item.production_id, item.dot_pos + 1, item.terminal_id
                        )
                        tmp.items.append(new_item)

                # 如果新的闭包中有项
                if tmp.items:
                    # 找新闭包的闭包
                    self.find_closures(tmp)

                    # 如果找到相同的闭包，更新映射
                    if tmp in self.closures:
                        self.gos[now_closure_id][i] = self.closures.index(tmp)
                    # 如果未找到相同的闭包，添加新的闭包及其映射
                    else:
                        tmp.cnt = len(self.closures)
                        self.closures.append(tmp)
                        self.gos.append({})
                        self.gos[now_closure_id][i] = tmp.cnt

            now_closure_id += 1

    def find_gotos(self):
        """
        goto和action表的实现

        注意：
        - self.terminal_symbols: 存储终结符的列表
        - self.non_terminal_symbols: 存储非终结符的列表
        - self.closures: 存储闭包的列表
        - self.gos: 存储Go表的列表，每个元素是一个字典，表示一个闭包的后继闭包及其映射
        - self.productions: 存储文法产生式的列
        - self.goto_table: 存储Goto表的列表，每个元素是一个字典，表示一个闭包的后继闭包及其映射
        - self.action_table: 存储Action表的列表，每个元素是一个字典，表示一个闭包的后继闭包及其映射
        """

        for i in range(len(self.closures)):
            self.goto_table.append({})
            self.action_table.append({})

            # 处理Goto表
            for tmp in self.gos[i].items():
                # 如果是非终结符
                # if tmp[0] >= len(self.terminal_symbols):
                self.goto_table[i][tmp[0]] = tmp[1]

            # 处理Action表
            for item in self.closures[i].items:
                if item.dot_pos == 0 and self.productions[item.production_id].to_ids[
                    0
                ] == len(self.terminal_symbols):
                    action = (ACTION_R, item.production_id)
                    self.action_table[i][item.terminal_id] = action
                # 如果·在末尾
                elif len(self.productions[item.production_id].to_ids) == item.dot_pos:
                    if self.productions[item.production_id].from_id != len(
                        self.terminal_symbols
                    ) + len(self.non_terminal_symbols):
                        # 如果[A->α· , a]在Ii中，且A≠S，那么置action[i, a]为reduce j
                        action = (ACTION_R, item.production_id)
                        self.action_table[i][item.terminal_id] = action
                    else:
                        # 如果[S->Program·, #]在Ii中，那么置action[i, #] = acc
                        if item.terminal_id == len(self.terminal_symbols) - 1:
                            action = (ACTION_ACC, 0)
                            self.action_table[i][item.terminal_id] = action
                else:
                    item_behind_dot = self.productions[item.production_id].to_ids[
                        item.dot_pos
                    ]

                    if item_behind_dot < len(self.terminal_symbols):
                        # 如果[A->α·aß, b]在Ii中，且GO(Ii, a) = Ij ，那么置action[i, a]为shift j
                        if item_behind_dot in self.gos[i]:
                            action = (ACTION_S, self.gos[i][item_behind_dot])
                            self.action_table[i][item_behind_dot] = action

    def get_action_table(self):
        action_table = []
        action_table.append(["Status"] + self.terminal_symbols)
        for i in range(len(self.action_table)):
            action_table.append([str(i)] + [""] * len(self.terminal_symbols))
            for j in range(len(self.terminal_symbols)):
                if str(j) in self.action_table[i].keys():
                    tmp = self.action_table[i][str(j)]
                    action_table[i + 1][j + 1] = ActionType[tmp[0]] + (
                        str(tmp[1]) if tmp[0] != ACTION_ACC else ""
                    )
        return action_table

    def get_goto_table(self):
        goto_table = []
        goto_table.append(["Status"] + self.non_terminal_symbols)
        for i in range(len(self.goto_table)):
            goto_table.append([str(i)] + [""] * len(self.non_terminal_symbols))
            for j in range(len(self.non_terminal_symbols)):
                if str(j) in self.goto_table[i].keys():
                    goto_table[i + 1][j + 1] = str(self.goto_table[i][str(j)])
        return goto_table

    # 语法分析函数的实现
    def getParse(self, lex):
        """
        执行语法分析

        参数：
        - lex: 词法分析的输出结果，包含词法单元的信息

        返回：
        - 树形结构，表示语法分析的结果
        """
        mySemantic = Semantic(
            self.productions, self.non_terminal_symbols, self.terminal_symbols
        )
        stack = []
        item = {"state": 0, "tree": {"root": "#"}}
        stack.append(item)
        self.parse_process_display = []
        self.parse_process_display.append(
            ["步骤", "状态栈", "符号栈", "待规约串", "动作说明"]
        )
        pending_string = [cur["prop"].value for cur in lex]
        pending_string = ", ".join(pending_string)
        self.parse_process_display.append(["0", "0", "#", pending_string, "初始状态"])

        index = 0
        cnt = 0
        last_loc = { "row":0, "col": 0 }    # 规约出错时应该报上一次的last_loc，故记录
        
        while index < len(lex):
            cnt += 1
            cur = lex[index]
            cur_token = tokenType_to_terminal(cur["prop"])
            cur_loc = cur["loc"]
            cur_content = cur["content"]
            token_id = self.get_id_by_str(cur_token)

            # 用于展示
            new_display_item = [None] * 5
            new_display_item[0] = str(cnt)

            current_state = self.action_table[stack[-1]["state"]]

            if str(token_id) not in current_state:
                self.semantic_quaternation = '代码中包含 Error ，中间代码暂不可用'
                self.semantic_error_occur = True
                self.semantic_error_message = [f"Error at ({cur_loc['row']},{cur_loc['col']}): 代码不符合语法规则"]     
                return {"root": "语法错误/代码不完整，无法解析", "err": cur["loc"]}

            if current_state[str(token_id)][0] == ACTION_S:
                next_state_id = current_state[str(token_id)][1]
                item = {
                    "state": next_state_id,
                    "tree": {"root": cur_token, "content": cur_content, "children": []},
                }
                stack.append(item)
                index += 1  # 当前输入串移动到下一个字符

                new_display_item[4] = f"移进“{cur_token}”, 状态{next_state_id}压栈"

            elif current_state[str(token_id)][0] == ACTION_R:
                production = self.productions[current_state[str(token_id)][1]]
                production_id = current_state[str(token_id)][1]
                tmp_symbol_stack = []
                from_pos = len(stack) - (
                    0
                    if production.to_ids[0] == len(self.terminal_symbols)
                    else len(production.to_ids)
                )
                for i in range(from_pos, len(stack)):
                    tmp_symbol_stack.append(stack[i])

                production_literal = self.get_str_by_id(production.from_id) + "->"
                children = []
                cur_content = ""
                for id in production.to_ids:
                    if id != len(self.terminal_symbols):
                        child = stack.pop()["tree"]
                        cur_content = child["content"] + cur_content
                        children.insert(0, child)
                        production_literal += self.get_str_by_id(id) + " "

                current_state = self.goto_table[stack[-1]["state"]]
                next_state_id = current_state[str(production.from_id)]
                item = {
                    "state": next_state_id,
                    "tree": {
                        "root": self.get_str_by_id(production.from_id),
                        "content": cur_content,
                        "children": children,
                    },
                }
                
                if not mySemantic.error_occur:
                    mySemantic.analyse(production_id, last_loc, item, tmp_symbol_stack)
                stack.append(item)

                new_display_item[
                    4
                ] = f"使用产生式({production_literal[:-1]})进行规约"  # 去除末尾多的空格

            elif current_state[str(token_id)][0] == ACTION_ACC:
                self.semantic_quaternation = mySemantic.getQuaternationTable()
                self.semantic_error_occur = mySemantic.error_occur
                self.semantic_error_message = mySemantic.error_msg
                print(self.semantic_quaternation)
                print(self.semantic_error_occur)
                print(self.semantic_error_message)
                return stack[-1]["tree"]

            else:
                self.semantic_quaternation = '代码中包含 Error ，中间代码暂不可用'
                self.semantic_error_occur = True
                self.semantic_error_message = [f"Error at ({last_loc['row']},{last_loc['col']}): 代码不符合语法规则"]      
                return {"root": "语法错误/代码不完整，无法解析", "err": "parser_error"}
            
            last_loc = cur_loc

            state_stack = [str(item["state"]) for item in stack]
            state_stack = " ".join(state_stack)

            symbol_stack = [str(item["tree"]["root"]) for item in stack]
            symbol_stack = " ".join(symbol_stack)

            pending_string = [cur["prop"].value for cur in lex[index:]]
            pending_string = ", ".join(pending_string)

            new_display_item[1] = state_stack
            new_display_item[2] = symbol_stack
            new_display_item[3] = pending_string
            self.parse_process_display.append(new_display_item)

            
