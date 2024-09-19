import re
import os
import json
import copy
from typing import List, Set, Dict
from tokenType import *
from myLexer import *
from mySemantic import *

'''
从配置文件中读取到的产生式
    - id: 在所有产生式中的编号
    - lhs: 产生式左部
    - rhs(list): 产生式右部
'''
class Production:
    def __init__(self):
        self.id = 0
        self.lhs = ""
        self.rhs = []

    def __repr__(self):
        return f"<{self.lhs} -> {' '.join(self.rhs)}>"

    def __lt__(self, other):
        return self.id < other.id
    
'''
组成项目集的LR(1)项目
'''
class Item:
    def __init__(self, production_id, dot_pos, forw):
        self.production_id = production_id      # 产生式编号
        self.dot_pos = dot_pos                  # 点的位置
        self.forw: str = forw                   # 前瞻终结符

    def __lt__(self, other):
        return (self.production_id, self.dot_pos, self.forw) < (
            other.production_id, other.dot_pos, other.forw)

    def __eq__(self, other):
        return (self.production_id, self.dot_pos, self.forw) == (
            other.production_id, other.dot_pos, other.forw)
    
    def __hash__(self):
        return hash((self.production_id, self.dot_pos, self.forw))
    
'''
项目集的闭包
'''
class Closure:
    def __init__(self):
        self.id = 0                         # 闭包编号
        self.items: List[Item] = []         # 项目集
        self.go: Dict[str, int] = {}        # 闭包的转移

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return set(self.items) == set(other.items)        

'''
语法分析器
'''
class Parser:
    def __init__(self):
        self.productions = []   # 记录所有的产生式

        self.terminals = [key for d in (tokenSymbols, tokenKeywords, tokenOthers) 
                          for key in d.keys()] + ["epsilon"]    # 终结符
        self.none_terminals = []                                # 非终结符，需从配置文件中读取

        self.firsts = {}                    # 非终结符的First集
        self.closures:List[Closure] = []    # 项目集的闭包

        self.goto_table = []
        self.action_table = []

        # 读入配置文件中的产生式
        self.readProductions()

        self.lexer = Lexer()    # 词法分析器，一遍扫描，故作为子程序调用

        self.semantic = Semantic(self.productions)   # 语义分析器，每次由语法分析器调用
        self.semantic_quaternation = []
        self.semantic_error_occur = False
        self.semantic_error_message = []

        # 保存在缓存中，第二次就无需反复计算闭包
        action_file_path = os.path.join("__pycache__", "action_table.json")
        goto_file_path = os.path.join("__pycache__", "goto_table.json")

        if not os.path.exists(action_file_path) or not os.path.exists(goto_file_path):
            self.getFirsts()
            self.getItemsets()
            self.getTable()
            if not os.path.exists("__pycache__"):
                os.makedirs("__pycache__")
            with open(action_file_path, "w") as file:
                json.dump(self.action_table, file, ensure_ascii=False)
            with open(goto_file_path, "w") as file:
                json.dump(self.goto_table, file, ensure_ascii=False)
        else:
            with open(action_file_path, "r") as file:
                self.action_table = json.load(file)
            with open(goto_file_path, "r") as file:
                self.goto_table = json.load(file)


    # 读取产生式配置文件
    def readProductions(self, filename="productions.cfg"):
        with open(filename, "r") as fin:
            for line in fin.readlines():
                match = re.match(r"\s*([^->]+)\s*->\s*(.*)", line)
                if match:
                    lhs = match.group(1).strip()
                    rhs = match.group(2).strip()

                    # 产生式右部可能有多种 通过"|"分隔
                    alternatives = [alt.strip() for alt in rhs.split("|")]  

                    # 记录左侧的非终结符
                    if lhs not in self.none_terminals:
                        self.none_terminals.append(lhs)

                    # 处理右侧的每一种产生式
                    for alt in alternatives:
                        prod = Production()
                        prod.id = len(self.productions)
                        prod.lhs = lhs

                        # 逐项push到production的rhs中
                        alt_split = [x for x in alt.split(" ")]
                        for symbol in alt_split:
                            if symbol not in self.terminals and \
                               symbol not in self.none_terminals:
                                self.none_terminals.append(symbol)
                            prod.rhs.append(symbol)

                        self.productions.append(prod) 
    
    # 构造每个（非）终结符的First集
    def getFirsts(self):
        # 对于终结符，First集就是本身
        self.firsts = {term: {term} for term in self.terminals}
        # 对于非终结符，初始化空集合
        for non_term in self.none_terminals:
            self.firsts[non_term] = set()
        while True:
            changeFlag = False      # 记录本次循环是否有First变化
            for prod in self.productions:
                lhs = prod.lhs
                for item in prod.rhs:
                    # 如果是终结符（包含epsilon）
                    if item in self.terminals:
                        # 还没有添加到左侧的First集
                        if item not in self.firsts[lhs]:
                            self.firsts[lhs].add(item)
                            changeFlag = True
                        break   # 遇到了终结符，不必再往后看了
                    else:
                        # 当前非终结符的First没有被左侧完全涵盖 还得继续循环
                        if not self.firsts[item] - {"epsilon"} <= self.firsts[lhs]:
                            changeFlag = True
                            self.firsts[lhs].update(self.firsts[item] - {"epsilon"})
                        # 没有epsilon，不必再往后看了
                        if "epsilon" not in self.firsts[item]:
                            break
                        # 遍历到产生式最右侧了 该加入epsilon
                        elif item == prod.rhs[-1] and "epsilon" not in self.firsts[lhs]:
                            changeFlag = True
                            self.firsts[lhs].add("epsilon")
 
            # First集固定 不再循环
            if not changeFlag:
                break

    # 辅助函数，计算句子的first集合
    def getStrFirst(self, str_list: List[str]) -> Set[str]:
        first = set()
        for item in str_list:
            # 加入当前的First集（除epsilon）
            first.update(self.firsts[item] - {"epsilon"})
            # 如果不含epsilon，则不必要继续了
            if "epsilon" not in self.firsts[item]:
                break
            # 句子遍历完毕，加上epsilon
            elif item == str_list[-1]:
                first.add("epsilon")
        return first
    
    # 给定项目集I，计算闭包
    def getClosure(self, closure: Closure):
        for item in closure.items:
            # · 已经在最右侧，不会带来闭包增加
            if item.dot_pos == len(self.productions[item.production_id].rhs):
                continue
            # 若是终结符（含epsilon），则不会带来闭包增加
            elif self.productions[item.production_id].rhs[item.dot_pos] in self.terminals:
                continue
            # · 的下一个是非终结符，找对应的项目加入
            else:
                next = self.productions[item.production_id].rhs[item.dot_pos]
                for prod in self.productions:
                    if prod.lhs != next:
                        continue
                    else:
                        # 建立新的项目，加入闭包
                        str_list = [item for item in \
                                    self.productions[item.production_id].rhs[item.dot_pos+1:] + [item.forw] \
                                    if item != "epsilon"]
                        forws = self.getStrFirst(str_list)
                        for forw in forws:                            
                            new_item = Item(prod.id, 0, forw)
                            if new_item not in closure.items:
                                closure.items.append(new_item)
    
    # 计算项目集族
    def getItemsets(self):
        # 拓广文法，加上S'->Program
        prod = Production()
        prod.id = len(self.productions)
        prod.lhs = "S'"
        prod.rhs = [self.none_terminals[0]]     # 即'Program'
        self.none_terminals.append("S'")
        self.productions.append(prod)

        # 创建项目：S'->.Program, #
        new_item = Item(prod.id, 0, "#")

        # 创建初始闭包以及项目集族
        root_closure = Closure()
        root_closure.id = 0
        root_closure.items.append(new_item)
        self.getClosure(root_closure)                   # 计算闭包
        self.closures.append(root_closure)              # 加入项目集族

        id = 0
        # 遍历每个闭包去看有没有新的转移带来新闭包的产生
        while id < len(self.closures):
            closure = self.closures[id]

            # 对于每个可能转移的文法符号X构建一个新的closure，然后勾连GO(I,X)
            for symbol in self.terminals + self.none_terminals:
                # 排除epsilon
                if symbol == "epsilon":
                    continue

                tmp_closure = Closure()

                # 遍历每一个项目
                for item in closure.items:
                    # · 已经在最右侧，不会带来闭包增加
                    if item.dot_pos == len(self.productions[item.production_id].rhs):
                        continue
                    # 下一个符号就是当前文法符号
                    elif symbol == self.productions[item.production_id].rhs[item.dot_pos]:
                        new_item = Item(self.productions[item.production_id].id, item.dot_pos + 1, item.forw)
                        tmp_closure.items.append(new_item)

                # 项目集非空
                if tmp_closure.items:
                    # 计算闭包
                    self.getClosure(tmp_closure)

                    # 如果找到相同的闭包，则更新映射
                    if tmp_closure in self.closures:
                        closure.go[symbol] = self.closures.index(tmp_closure)
                    else:
                        tmp_closure.id = len(self.closures)
                        self.closures.append(tmp_closure)
                        closure.go[symbol] = tmp_closure.id

            id += 1

    # 填充GOTO & ACTION表
    def getTable(self):
        for closure in self.closures:
            self.goto_table.append({})
            self.action_table.append({})

            # 处理GOTO表
            for key, value in closure.go.items():
                if key in self.none_terminals:
                    self.goto_table[-1][key] = value

            # 处理ACTION表
            for item in closure.items:
                # 特别处理epsilon
                if  item.dot_pos == 0 \
                    and self.productions[item.production_id].rhs[0] == "epsilon":
                    self.action_table[-1][item.forw] = ("r", item.production_id)
                # · 在末尾，规约
                elif item.dot_pos == len(self.productions[item.production_id].rhs):
                    # S'->Program·,# 特别情况acc
                    if self.productions[item.production_id].lhs == "S'":
                        self.action_table[-1][item.forw] = ("acc", None)
                    else:
                        self.action_table[-1][item.forw] = ("r", item.production_id)
                # · 在中间，移进
                else:
                    behind_dot = self.productions[item.production_id].rhs[item.dot_pos]
                    if behind_dot in self.terminals:
                        self.action_table[-1][behind_dot] = ("s", closure.go[behind_dot])


    def getParse(self, codes):
        # 重新构造lexer和semantic（reset或许更好）
        self.lexer = Lexer(codes)
        self.semantic = Semantic(self.productions)

        stack = []          # 用于移进规约分析的栈
        stack.append({"state": 0, "tree": {"token": "#"}})

        last_loc = { "row":0, "col": 0 }    # 规约出错时应该报上一次的last_loc，故记录
        cur = self.lexer.getNextToken()     # 当前规约的token
        cnt = 0                             # 为了打印规约步骤的标号

        self.parse_process_display = []
        self.parse_process_display.append(["步骤", "状态栈", "符号栈", "待规约token", "动作说明"])
        self.parse_process_display.append(["0", "0", "#", f"{cur}", "初始状态"])

        while True:
            cnt += 1
            cur_token = tokenType_to_terminal(cur["prop"])  # 根据token类型取出对应字符串
            cur_loc = cur["loc"]                            # 当前分析到代码中的位置（用于报错）
            cur_content = cur["content"]                    # 当前的内容（即代码中的字面量）

            action = self.action_table[stack[-1]["state"]]

            # 用于展示
            new_display_item = [None] * 5
            new_display_item[0] = str(cnt)
            
            if cur_token not in action:
                self.semantic_quaternation = '代码中包含 Error，中间代码暂不可用'
                self.semantic_error_occur = True
                self.semantic_error_message = [f"Error at ({cur_loc['row']},{cur_loc['col']}): 代码不符合语法规则"]     
                return {"token": "语法错误/代码不完整，无法解析", "err": "parser_error"}

            # 移进
            if action[cur_token][0] == "s":
                next_state_id = action[cur_token][1]
                stack.append({"state": next_state_id, "tree": {"token": cur_token, "content": cur_content, "children": []}})
                cur = self.lexer.getNextToken()  # 移动到下一个token
                new_display_item[4] = f"移进“{cur_token}”, 状态{next_state_id}压栈"
            # 规约
            elif action[cur_token][0] == "r":
                prod_id = action[cur_token][1]
                prod = self.productions[prod_id]
                
                children = []       
                content = ""        # 当前节点对应的代码字面量
                for item in prod.rhs:
                    if item == "epsilon":
                        continue
                    else:
                        child = stack.pop()["tree"]
                        content = f"{child['content']}{content}"
                        children.insert(0, child)
              
                next_state_id = self.goto_table[stack[-1]["state"]][prod.lhs]
                item = {"state": next_state_id, "tree": {"token": prod.lhs, "content": content, "children": children}}
                self.semantic.analyse(prod_id, last_loc, item, children)
                stack.append(item)
                new_display_item[4] = f"使用产生式({prod.lhs} -> {' '.join(prod.rhs)})进行规约"
            # acc
            elif action[cur_token][0] == "acc":
                self.semantic_quaternation = copy.deepcopy(self.semantic.getQuaternationTable())
                self.semantic_error_occur = self.semantic.error_occur
                self.semantic_error_message = self.semantic.error_msg
            
                # 返回时不带上content和attribute这两个中间信息 
                def removeRedundancy(dictionary):
                    if isinstance(dictionary, dict):
                        if 'content' in dictionary:
                            del dictionary['content']
                        if 'attribute' in dictionary:
                            del dictionary['attribute']
                        for key, value in dictionary.items():
                            dictionary[key] = removeRedundancy(value)
                    elif isinstance(dictionary, list):
                        for i in range(len(dictionary)):
                            dictionary[i] = removeRedundancy(dictionary[i])
                    return dictionary
                return removeRedundancy(stack[-1]["tree"])
            
            last_loc = cur_loc

            state_stack = " ".join([str(item["state"]) for item in stack])
            symbol_stack = " ".join([str(item["tree"]["token"]) for item in stack])
            pending_token = f"{cur}"
            new_display_item[1:4] = state_stack, symbol_stack, pending_token
            self.parse_process_display.append(new_display_item)

    def getGotoTable(self):
        ret = [["状态"] + self.none_terminals]
        for i in range(len(self.goto_table)):
            row = [f"{i}"]
            for j in self.none_terminals:
                row.append(self.goto_table[i].get(j, ""))
            ret.append(row)

        return ret

    def getActionTable(self):
        ret = [["状态"] + self.terminals]
        for i in range(len(self.action_table)):
            row = [f"{i}"]
            for j in self.terminals:
                item = self.action_table[i].get(j, None)
                if item:
                    row.append("acc" if item[0] == "acc" else f"{item[0]}{item[1]}")
                else:
                    row.append("")
            ret.append(row)
        
        return ret