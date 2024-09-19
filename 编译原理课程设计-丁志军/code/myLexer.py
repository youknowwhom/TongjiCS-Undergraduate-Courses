from string import digits, ascii_letters
from tokenType import tokenType, tokenSymbols, tokenKeywords

'''
DFA有限自动机的状态
'''
class DFA_state(object):
    def __init__(self):
        self.transfer = {}
        self.tokenType = tokenType.UNKNOWN


'''
DFA有限自动机
'''
class DFA(object):
    def __init__(self) -> None:
        self.start_state = DFA_state() # DFA的起始状态
        self.cur = self.start_state    # 当前DFA所在的状态
        self.len = 0

        self.initAlpha()
        self.initDigit()
        self.initSymbol()

    # 为保留字和identifier添加对应的状态和转移
    def initAlpha(self):
        # 初始化所有的keyword对应的状态，并记录状态集合
        stateSet = set()
        for keyword in tokenKeywords:
            stateSet |= self.initToken(keyword, tokenKeywords[keyword])

        # 处理剩余的字母、数字转移，应该识别为identifier
        identifierState = DFA_state()
        identifierState.tokenType = tokenType.IDENTIFIER

        # 进入identifier state之后，再读入数字/字母都还是identifier
        for letter in ascii_letters + digits:
            identifierState.transfer[letter] = identifierState

        # 从初始状态到identifier state必须是读入字母
        for alpha in ascii_letters:
            if alpha not in self.start_state.transfer:
                self.start_state.transfer[alpha] = identifierState

        for state in stateSet:
            # 不是单词末尾，则类型为identifier
            # e.g. 关键字else，如果只读入前三个字母应该是identifier
            state.tokenType = (
                state.tokenType
                if state.tokenType != tokenType.UNKNOWN
                else tokenType.IDENTIFIER
            )
            # 其他转移应该回归到identifier state
            # e.g. else在读到els后，读入一个a，应该作为elsa被识别为identifier
            for alpha in ascii_letters:
                if alpha not in state.transfer:
                    state.transfer[alpha] = identifierState
            for d in digits:
                state.transfer[d] = identifierState

    # 为整型、浮点型常量添加对应的状态与转移
    def initDigit(self):
        # DFA的状态转移图详见报告
        states = {}

        # 建立6个新状态
        for i in range(7):
            if i == 0:
                states[i] = self.start_state
            else:
                states[i] = DFA_state()

        # 设置接受态
        states[1].tokenType = tokenType.INTEGER_CONSTANT
        states[3].tokenType = tokenType.FLOATING_POINT_CONSTANT
        states[6].tokenType = tokenType.FLOATING_POINT_CONSTANT

        # 添加所有0-9的转移
        for d in digits:
            states[0].transfer[d] = states[1]
            states[1].transfer[d] = states[1]
            states[2].transfer[d] = states[3]
            states[3].transfer[d] = states[3]
            states[4].transfer[d] = states[6]
            states[5].transfer[d] = states[6]
            states[6].transfer[d] = states[6]

        # 添加其余琐碎转移
        states[1].transfer["."] = states[2]
        states[1].transfer["e"] = states[4]
        states[1].transfer["E"] = states[4]
        states[3].transfer["e"] = states[4]
        states[3].transfer["E"] = states[4]
        states[4].transfer["+"] = states[5]
        states[4].transfer["-"] = states[5]

    # 为所有的符号添加对应的状态和转移
    def initSymbol(self):
        for symbol in tokenSymbols:
            self.initToken(symbol, tokenSymbols[symbol])

    # 对token串添加对应的状态和转移，返回新增加的状态集合
    def initToken(self, word: str, type):
        cur = self.start_state
        stateSet = set()
        for char in word:
            if char not in cur.transfer:
                cur.transfer[char] = DFA_state()
            cur = cur.transfer[char]
            stateSet.add(cur)
        cur.tokenType = type

        return stateSet

    # DFA读入一个字符，转移至对应状态
    def forward(self, ch: str):
        assert len(ch) == 1, "Expect a char, got a string"
        self.len += 1
        # 该状态不存在对应转移，重置DFA状态
        if ch not in self.cur.transfer:
            self.reset()
            return None, 0
        else:
            self.cur = self.cur.transfer[ch]
            return self.cur.tokenType, self.len

    # 重置DFA状态，从初始态重新开始
    def reset(self):
        self.cur = self.start_state
        self.len = 0

'''
词法分析器
'''
class Lexer(object):
    def __init__(self, lines=None):
        self.dfa = DFA()
        self.lines = lines          # 以行为字符串的代码
        self.row = 0                # 当前读到的行位置 
        self.col = 0                # 当前读到的列位置
        self.id = 0                 # token的序号
        self.annotation = False     # 是否在读注释 /* */
        self.token = None           # 上一次读到一半的token
        self.token_len = 0          # 上一次读的token长度


    # 由Parser调用，每次得到一个token
    def getNextToken(self):    
        while self.row < len(self.lines):     
            while self.col < len(self.lines[self.row]) + 1:
                ch = (self.lines[self.row] + '#')[self.col]
                newtoken, newlength = self.dfa.forward(ch)
                
                if self.token and not newtoken:
                    if self.token == tokenType.S_COMMENT:
                        break
                    elif self.token == tokenType.LM_COMMENT:
                        self.annotation = True

                    if not self.annotation:
                        item = {}
                        item["id"] = self.id
                        self.id += 1
                        item["content"] = self.lines[self.row][self.col - self.token_len : self.col]
                        item["prop"] = self.token
                        item["loc"] = {"row": self.row, "col": self.col - self.token_len + 1}
                        self.dfa.reset()
                        self.token = None
                        self.token_len = 0
                        return item

                    if self.token == tokenType.RM_COMMENT:
                        self.annotation = False

                    self.dfa.reset()

                else:
                    self.token, self.token_len = newtoken, newlength

                self.col += 1

            self.row += 1
            self.col = 0
            self.dfa.reset()
            self.token = None
            self.token_len = 0
        
        return {"id": self.id, "content": "#", "prop": tokenType.EOF, "loc": {"row": self.row, "col": 1},}


    # 原先词法、语法两遍的逻辑，保留在此处用于编辑器的语法高亮
    def getLex(self):
        ret = []
        row = 1
        id = 1
        annotation = False
        success = True
        for line in self.lines:
            self.dfa.reset()
            token = None
            length = 0
            col = 0
            for ch in line + "#":  # 行末加一个字符以确认每一行最后一个输入DFA的串
                newtoken, newlength = self.dfa.forward(ch)

                if token and not newtoken:
                    if token == tokenType.S_COMMENT:
                        break
                    elif token == tokenType.LM_COMMENT:
                        annotation = True

                    if not annotation:
                        item = {}
                        item["id"] = id
                        id += 1
                        item["content"] = line[col - length : col]
                        item["prop"] = token
                        item["loc"] = {"row": row, "col": col - length + 1}
                        ret.append(item)

                    if token == tokenType.RM_COMMENT:
                        annotation = False

                    self.dfa.reset()
                    token, length = self.dfa.forward(ch)
                    # 重读依然失败
                    if not token and not annotation and ch not in [" ", "\t", "\n"]:
                        success = False
                        item = {}
                        item["prop"] = tokenType.UNKNOWN
                        item["loc"] = {"row": row, "col": col + 1}
                        ret.append(item)
                elif not token and not newtoken:
                    if not annotation and ch not in [" ", "\t", "\n"]:
                        # 无法解析的字符
                        success = False
                        item = {}
                        item["prop"] = tokenType.UNKNOWN
                        item["loc"] = {"row": row, "col": col + 1}
                        ret.append(item)
                else:
                    token, length = newtoken, newlength
                col += 1
            row += 1

        ret.append(
            {
                "id": id,
                "content": "#",
                "prop": tokenType.EOF,
                "loc": {"row": row, "col": 1},
            }
        )

        print(f"Lexer {'done successfully' if success else 'failed'}")

        return ret, success
