from collections import defaultdict

"""
寄存器分配与内存管理
"""
class RegManager:
    def __init__(self):
        self.RValue = defaultdict(set)
        self.AValue = defaultdict(set)
        self.num_registers = 8
        self.frame_size = 0          # 当前栈帧大小
        self.free_registers = []     # 当前空闲的寄存器
        self.memory = {}             # 记录变量在内存中临时存储的地址
        self.func_vars = {}          # 当前的局部变量
        self.data_vars = {}          # 全局变量（数据段）

    # 清空某变量所占用的寄存器
    def freeVarRegisters(self, var):
        # 全局变量不清空
        if var in self.data_vars - self.func_vars:
            return
        for pos in self.AValue[var]:
            if pos != "Memory":
                self.RValue[pos].remove(var)
                if len(self.RValue[pos]) == 0:
                    self.free_registers.append(pos)
        self.AValue[var].clear()
    
    # 清空所有寄存器（基本块开始前）
    def freeAllRegisters(self, in_set):
        self.RValue.clear()
        self.AValue.clear()
        for var in in_set:
            self.AValue[var].add("Memory")
        self.free_registers = [f"$s{self.num_registers - i - 1}" for i in range(self.num_registers)]

    # 将变量存储到内存中
    def storeVariable(self, var, reg, codes):
        if var not in self.memory:
            self.memory[var] = self.frame_size
            self.frame_size += 4
        self.AValue[var].add("Memory")
        # 局部变量或中间变量
        if var in self.func_vars or var[0] == 'T':
            codes.append(f"sw {reg}, {self.memory[var]}($sp)")
        elif var in self.data_vars:
            codes.append(f"sw {reg}, {var}")

    # 将当前基本块的出口活跃变量存储到内存中
    def storeOutSet(self, out_set, codes):
        for var in out_set:
            reg = None
            for pos in self.AValue[var]:
                # 已经在memory中则不用再存储
                if pos == "Memory":
                    reg = None
                    break
                else:
                    reg = pos

            if reg:
                self.storeVariable(var, reg, codes)

    # 分配一个新的寄存器
    def allocateFreeRegister(self, quars, cur_quar_index, out_set, codes):
        free_reg = ""
        # 有寄存器空闲，则直接分配
        if len(self.free_registers):
            free_reg = self.free_registers.pop()
            return free_reg
        
        # 若无，则需要寻找最远引用的变量让渡寄存器
        farest_usepos = float('-inf')
        for reg, vars in self.RValue.items():
            cur_usepos = float('inf')
            # 看看存在这个reg中引用最近的那个var
            for var in vars:
                # 如果存在别的地方，则很好
                if len(self.AValue[var]) > 0:
                    continue

                for idx in range(cur_quar_index, len(quars)):
                    quar = quars[idx]
                    if var in [quar.src1, quar.src2]:
                        cur_usepos = min(cur_usepos, idx - cur_quar_index)
                        break
                    if var == quar.tar:
                        break
            
            if cur_usepos == float('inf'):
                free_reg = reg
                break
            elif cur_usepos > farest_usepos:
                farest_usepos = cur_usepos
                free_reg = reg
        
        # 释放寄存器，保存数据
        for var in self.RValue[free_reg]:
            self.AValue[var].remove(free_reg)
            # 若无其他地方存法数据，才需要sw
            if len(self.AValue[var]) == 0:
                need_store = None
                for idx in range(cur_quar_index, len(quars)):
                    quar = quars[idx]
                    if var in [quar.src1, quar.src2]:
                        need_store = True
                        break
                    if var == quar.tar:
                        break
                if need_store == None:  # 没有被引用、定值，检查是不是出口活跃
                    need_store = True if var in out_set else False
                if need_store:
                    self.storeVariable(var, free_reg, codes)

        self.RValue[free_reg].clear()

        return free_reg
    
    def _is_variable(self, name) -> bool:
        return name[0].isalpha() or (name[0] == '-' and name != '-')
    
    # 为四元式的src获取寄存器
    def getSrcRegister(self, src, quars, cur_quar_index, out_set, codes):
        reg = ""
        # 先查AValue有无现成
        for pos in self.AValue[src]:
           if pos != "Memory":
               return pos

        # 没有则分配一个
        reg = self.allocateFreeRegister(quars, cur_quar_index, out_set, codes)

        if self._is_variable(src):
            # 局部变量或中间变量
            if src in self.func_vars or src[0] == 'T':
                codes.append(f"lw {reg}, {self.memory[src]}($sp)")
            elif src in self.data_vars:
                codes.append(f"lw {reg}, {src}")
            # 更新AValue RValue
            self.AValue[src].add(reg)
            self.RValue[reg].add(src)
        else:   # 立即数
            codes.append(f"li {reg}, {src}")

        return reg
    
    # 为四元式的tar获取寄存器
    def getTarRegister(self, tar, quars, cur_quar_index, out_set, codes):
        quar = quars[cur_quar_index]
        src1 = quar.src1
        # 看能否复用操作数的寄存器
        # 首先保证src1不是数字
        # 其次不抢占全局变量的寄存器
        if self._is_variable(src1) and src1 not in (self.data_vars - self.func_vars):
            for pos in self.AValue[src1]:
                if pos != "Memory" and len(self.RValue[pos]) == 1:
                    if not quar.info_src1.active:
                        self.RValue[pos].remove(src1)
                        self.RValue[pos].add(tar)
                        self.AValue[src1].remove(pos)
                        self.AValue[tar].add(pos)
                        return pos

        # 重新分配
        reg = self.allocateFreeRegister(quars, cur_quar_index, out_set, codes)
        self.RValue[reg].add(tar)
        self.AValue[tar].add(reg)
        
        return reg


"""
目标代码生成器
"""
class CodeGenerator:
    def __init__(self, func_blocks, func_info, data_words):
        self.func_blocks = func_blocks
        self.func_words = {func.name:func.words_table for func in func_info}        # 各函数定义的局部变量
        self.data_words = {word.name for word in data_words}                        # 全局变量 存放在data段
        self.param_list = []                                                        # param传递的参数 每个基本块都要清空
        self.regManager = RegManager()
        self.regManager.data_vars = {word.name for word in data_words}
        self.codes = []                                                             # 最终生成的目标代码
        self.error_occur = False
        self.error_msg = []

    def getObjectCode(self):
        self.codes.append(".data")
        for var in sorted(list(self.data_words)):
            self.codes.append(f"{var}: .word 0")
        self.codes.append("")

        self.codes.append(".text")
        self.codes.append("lui $sp, 0x1004")
        self.codes.append("j main") # 跳转到main函数
        
        for func, blocks in self.func_blocks.items():
            self.getFuncObjectCode(func, blocks)
        self.codes.append("end:")

        # 为可读性加一下缩进
        for cindex in range(len(self.codes)):
            code = self.codes[cindex]
            if len(code) and code[0] != "." and code[-1] != ":":
                self.codes[cindex] = "\t" + code

        return self.codes

    def getFuncObjectCode(self, func_name, blocks):
        self.regManager.memory.clear()
        self.regManager.func_vars = {var.name for var in self.func_words[func_name]}
        for bindex in range(len(blocks)):
            block = blocks[bindex]
            self.codes.append(f"{block.name}:")
            if bindex == 0:
                if func_name != "main":
                    self.codes.append("sw $ra, 4($sp)")  # 压栈返回地址，防止多层调用
                # 2分别是存储的ra返回地址和此前的sp值
                self.regManager.frame_size = 2 * 4 if func_name != "main" else 0
                self.regManager.memory.clear()
                # 为局部变量（和传入参数）预留空间
                for word in self.func_words[func_name]:
                    self.regManager.memory[word.name] = self.regManager.frame_size
                    self.regManager.AValue[word.name].add("Memory")
                    self.regManager.frame_size += 4
            self.getBlockObjectCode(block, func_name)

    def getBlockObjectCode(self, block, func_name):
        # 清空寄存器使用情况，AValue记入入口活跃变量
        self.regManager.freeAllRegisters(block.in_set)
        self.param_list = []
        for qindex in range(len(block.codes)):
            quad = block.codes[qindex]
            # 将出口活跃变量存到内存中
            if qindex == len(block.codes) - 1:
                # 如果有数据段全局变量在此基本块定值，也进行保存
                outset = block.out_set | ((self.regManager.data_vars - self.regManager.func_vars))
                if quad.op in ["j", "jnz", "ret"]:
                    self.regManager.storeOutSet(outset, self.codes)
                    self.getQuarObjectCode(quad, qindex, block, func_name)
                elif quad.op == "call":
                    self.regManager.storeOutSet(outset - {quad.tar}, self.codes)
                    self.getQuarObjectCode(quad, qindex, block, func_name)
                    self.regManager.storeOutSet({quad.tar}, self.codes)
                else:
                    self.getQuarObjectCode(quad, qindex, block, func_name)
                    self.regManager.storeOutSet(outset, self.codes)
            else:
                self.getQuarObjectCode(quad, qindex, block, func_name)

    def getQuarObjectCode(self, quad, qindex, block, func_name):
        if self.error_occur:
            return
        
        if quad.op == "=":
            reg = self.regManager.getSrcRegister(quad.src1, block.codes, qindex, block.out_set, self.codes)
            self.regManager.freeVarRegisters(quad.tar)
            self.regManager.RValue[reg].add(quad.tar)
            self.regManager.AValue[quad.tar].add(reg)

        elif quad.op == "ret":
            if self.regManager._is_variable(quad.src1):
                reg = None
                for pos in self.regManager.AValue[quad.src1]:
                    if pos != "Memory":
                        reg = pos
                        break
                if reg:
                    self.codes.append(f"add $v0, {pos}, $zero")
                else:
                    self.codes.append(f"lw $v0, {self.regManager.memory[quad.src1]}($sp)")
            elif quad.src1 != "_":
                self.codes.append(f"li $v0, {quad.src1}")

            if func_name == "main":
                self.codes.append("j end")
            else:
                self.codes.append(f"lw $ra, 4($sp)")  # 取返回地址到ra中跳转
                self.codes.append("jr $ra")

        elif quad.op == "j":
            self.codes.append(f"j {quad.tar}")

        elif quad.op == "jnz":
            rs = self.regManager.getSrcRegister(quad.src1, block.codes, qindex, block.out_set, self.codes)
            self.codes.append(f"bnez {rs}, {quad.tar}")
            if not self.regManager._is_variable(quad.src1):
                self.regManager.free_registers.append(rs)
            elif not quad.info_src1.active:
                self.regManager.freeVarRegisters(quad.src1)

        elif quad.op =="param":
           self.param_list.append({'name': quad.src1, 'active': quad.info_src1.active if quad.info_src1 else False})

        elif quad.op == "call":
            top = 0
            for param in self.param_list:
               reg = self.regManager.getSrcRegister(param['name'], block.codes, qindex, block.out_set, self.codes)
               self.codes.append(f"sw {reg}, {2*4 + top + self.regManager.frame_size}($sp)") # 同样的，2个位置分别存ra和sp
               top += 4
               if not param['active']:
                   self.regManager.freeVarRegisters(param['name'])
            # sp存储并指向新位置
            self.codes.append(f"sw $sp, {self.regManager.frame_size}($sp)")
            self.codes.append(f"addi $sp, $sp, {self.regManager.frame_size}")

            # 跳转新函数
            self.codes.append(f"jal {quad.src1}")

            # 跳转回来后，恢复sp
            self.codes.append("lw $sp, 0($sp)")
            # 将$v0中的返回值填写到对应临时变量
            if quad.tar != "_":
                rd = self.regManager.getTarRegister(quad.tar, block.codes, qindex, block.out_set, self.codes)
                self.codes.append(f"add {rd}, $v0, $zero")

        elif quad.op in ["<", ">", "<=", ">=", "==", "!="]:
            op = {
                "<": "slt",
                ">": "sgt",
                "<=": "sle",
                ">=": "sge",
                "==": "seq",
                "!=": "sne"
            }
            rs = self.regManager.getSrcRegister(quad.src1, block.codes, qindex, block.out_set, self.codes)
            rt = self.regManager.getSrcRegister(quad.src2, block.codes, qindex, block.out_set, self.codes)
            rd = self.regManager.getTarRegister(quad.tar , block.codes, qindex, block.out_set, self.codes)
            self.codes.append(f"{op[quad.op]} {rd}, {rs}, {rt}")

            if not self.regManager._is_variable(quad.src1):
                self.regManager.free_registers.append(rs)
            elif not quad.info_src1.active and quad.src1 != quad.tar:
                self.regManager.freeVarRegisters(quad.src1)
            if not self.regManager._is_variable(quad.src2):
                self.regManager.free_registers.append(rt)
            elif not quad.info_src2.active and quad.src2 != quad.tar:
                self.regManager.freeVarRegisters(quad.src2)
                        
        
        elif quad.op in ["int+", "int-", "int*", "int/"]:
            rs = self.regManager.getSrcRegister(quad.src1, block.codes, qindex, block.out_set, self.codes)
            rt = self.regManager.getSrcRegister(quad.src2, block.codes, qindex, block.out_set, self.codes)
            rd = self.regManager.getTarRegister(quad.tar , block.codes, qindex, block.out_set, self.codes)
            if quad.op == "int+":
                self.codes.append(f"add {rd}, {rs}, {rt}")
            elif quad.op == "int-":
                self.codes.append(f"sub {rd}, {rs}, {rt}")
            elif quad.op == "int*":
                self.codes.append(f"mul {rd}, {rs}, {rt}")
            elif quad.op == "int/":
                self.codes.append(f"div {rs}, {rt}")
                self.codes.append(f"mflo {rd}")
                
            if not self.regManager._is_variable(quad.src1):
                self.regManager.free_registers.append(rs)
            elif not quad.info_src1.active and quad.src1 != quad.tar:
                self.regManager.freeVarRegisters(quad.src1)

            if not self.regManager._is_variable(quad.src2):
                self.regManager.free_registers.append(rt)
            elif not quad.info_src2.active and quad.src2 != quad.tar:
                self.regManager.freeVarRegisters(quad.src2)

        elif "float" in quad.op or "into" in quad.op:
            self.error_occur = True
            self.error_msg = ["Error: 目标代码生成暂不支持浮点数运算"]