from typing import List, Dict

"""
基本块
"""
class Block():
    def __init__(self):
        self.name:str   = ""
        self.start_addr = 0     # 基本块中第一个四元式的起始地址
        self.codes:List = []    # 属于该基本块的四元式
        self.next1:Block = None
        self.next2:Block = None
        # 以下是计算得到的信息
        self.use_set = set()    # 在基本块中首次出现是引用形式的变量
        self.def_set = set()    # 在基本块中首次出现是定值形式的变量
        self.in_set = set()
        self.out_set = set()
    
    def __repr__(self):
        next1_name = "None" if self.next1 is None else self.next1.name
        next2_name = "None" if self.next2 is None else self.next2.name
        return f"Block {self.name} <start_addr:{self.start_addr}, codes:{self.codes}, next1:{next1_name}, next2:{next2_name}>"


"""
四元式符号的待用与活跃信息
"""
class SymbolInfo():
    def __init__(self, use=None, active=False):
        self.use = use
        self.active = active

    def __repr__(self) -> str:
        return f"<{self.use}, {self.active}>"


"""
基本块划分器
"""
class BlockDivider():
    def __init__(self, quaternation_table, start_address = 100):
        self.quaternion_table = quaternation_table
        self.start_address = start_address
        self.block_cnt = 0                              # 用于为每个基本块分配唯一名称
        self.func_blocks:Dict[str, List[Block]] = {}

    def getBlockName(self):
        self.block_cnt += 1
        return f"block{self.block_cnt}"
    
    def divideBlocks(self, func_table: List):
        # 按照函数块划分基本块
        func_index = 0
        while func_index < len(func_table):
            func = func_table[func_index]
            block_enter = []    # 当前函数块的所有入口语句

            """
            第一步：找到所有入口语句的位置并记录
            """
            # 函数块的第一个语句是入口语句
            block_enter.append(func["enter"] - self.start_address)

            func_start = func["enter"] - self.start_address
            func_end = len(self.quaternion_table) if func == func_table[-1] \
                       else func_table[func_index + 1]["enter"] - self.start_address

            # 遍历当前函数块的四元式寻找入口语句
            for quar_index in range(func_start, func_end):
                quar = self.quaternion_table[quar_index]
                if quar.op[0] == "j":
                    # 无条件转移（转移到的语句是入口语句）
                    if quar.op == "j":
                        # return在最后可能没有回填，这样的j语句作废
                        if int(quar.tar) != 0:
                            block_enter.append(int(quar.tar) - self.start_address)
                    # 有条件转移（下一条/转移到的语句是入口语句）
                    else:
                        if quar_index < func_end - 1:
                            block_enter.append(quar_index + 1)
                        block_enter.append(int(quar.tar) - self.start_address)
                elif quar.op == "call":
                    if quar_index < func_end - 1:
                        block_enter.append(quar_index + 1)

            func_index += 1
            block_enter = sorted(list(set(block_enter)))  # 对入口语句去重并排序

            """
            第二步：压入每个基本块的代码（介于两个基本块起始地址之间 / 到一个转移语句停止）
            """
            self.func_blocks[func["name"]] = []
            for enter_index in range(len(block_enter)):
                block_start = block_enter[enter_index]
                block_end = block_enter[enter_index + 1] if enter_index < len(block_enter) - 1 else func_end
                block = Block()
                block.name = func["name"] if enter_index == 0 else self.getBlockName()
                block.start_addr = block_start
                # 压入每一个四元式
                for quar_index in range(block_start, block_end):
                    cur_quar = self.quaternion_table[quar_index]
                    block.codes.append(cur_quar)
                    # 包含到一个转移语句（可能是无条件转移） 该基本块停止
                    if cur_quar.op[0] == "j" or cur_quar.op in ["call", "ret"]:
                        break

                self.func_blocks[func["name"]].append(block)
            
            """
            第三步：建立基本块之间的转移关系
            """
            for block_index in range(len(self.func_blocks[func["name"]])):
                block = self.func_blocks[func["name"]][block_index]
                next_block = self.func_blocks[func["name"]][block_index + 1] if block_index < len(self.func_blocks[func["name"]]) - 1 else None
                if len(block.codes) == 0:
                    continue
                last_quar = block.codes[-1]
                if last_quar.op[0] == "j":
                    des_addr = int(last_quar.tar) - self.start_address
                    des_block = next((block for block in self.func_blocks[func["name"]] 
                                            if block.start_addr == des_addr), None)
                    # 无条件转移
                    if last_quar.op == "j":
                        block.next1 = des_block
                        block.next2 = None
                    # 有条件转移
                    else:
                        block.next1 = next_block
                        block.next2 = des_block
                    # 修改四元式跳转目标为标签
                    last_quar.tar = des_block.name
                elif last_quar.op == "ret":
                    block.next1 = None
                    block.next2 = None
                else:
                    block.next1 = next_block
                    block.next2 = None

    # 判断是否是变量
    def _is_var(self, name:str)->bool:
        return name[0].isalpha() or (name[0] == '-' and name != '-')

    # 计算变量的活跃和待用信息
    def computeBlocks(self, func_table: List):
        self.divideBlocks(func_table)

        # for func, blocks in self.func_blocks.items():
        #     print("function:", func)
        #     for block in blocks:
        #         print('\t' + block.name)
        #         for quar in block.codes:
        #             print('\t\t', quar)

        #         print('\t\tnext1:', block.next1.name if block.next1 else None)
        #         print('\t\tnext2:', block.next2.name if block.next2 else None)
    
        # 以函数为单位进行分析
        for func, blocks in self.func_blocks.items():
            # 下面对每个基本块进行分析
            # 计算每个基本块的Use和Def集合
            for block in blocks:
                # print(f'\t{block.name}\n\t\t{block.codes}')
                # 逐个四元式分析
                for quar in block.codes:
                    if quar.op == "j":
                        continue
                    if quar.op != "call":
                        if self._is_var(quar.src1) and quar.src1 not in block.def_set:
                            block.use_set.add(quar.src1)
                        if self._is_var(quar.src2) and quar.src2 not in block.def_set:
                            block.use_set.add(quar.src2)
                    if quar.op[0] != "j":    # 不是条件跳转
                        if self._is_var(quar.tar) and quar.tar not in block.use_set:
                            block.def_set.add(quar.tar)

                block.in_set  = set(block.use_set)
                block.out_set = set()

            # 更新每个基本块的In和Out活跃集
            changeFlag = True
            while changeFlag:
                changeFlag = False
                for block in blocks:
                    next1 = block.next1
                    next2 = block.next2
                    if next1:
                        # 将后继block的入口活跃集中的元素插入当前的出口活跃集中
                        # 若在def集中不存在，还需加到自己的入口活跃集中
                        # OUT = ∪IN(后继)     IN = USE ∪ (OUT - DEF)
                        for var in next1.in_set:
                            if var not in block.out_set:
                                block.out_set.add(var)
                                changeFlag = True
                                if var not in block.def_set:
                                    block.in_set.add(var)
                    if next2:
                        for var in next2.in_set:
                            if var not in block.out_set:
                                block.out_set.add(var)
                                changeFlag = True
                                if var not in block.def_set:
                                    block.in_set.add(var)

            # 记录当前每个基本块中变量的活跃、待用信息
            blockSymbolInfoTable = { }
            # 记录每个基本块的出口活跃变量的信息
            for block in blocks:
                symbolInfoTable = {}
                for var in block.out_set:
                    symbolInfoTable[var] = SymbolInfo(None, True)
                blockSymbolInfoTable[block] = symbolInfoTable


            # 倒推给每个四元式赋上活跃与待用信息
            for block in blocks:
                index = len(block.codes)
                for quar in reversed(block.codes):
                    index -= 1
                    # 不存在变量信息更新
                    if quar.op in ["j", "call"]:
                        continue
                    if self._is_var(quar.src1):
                        quar.info_src1 = blockSymbolInfoTable[block].get(quar.src1, SymbolInfo())
                        blockSymbolInfoTable[block][quar.src1] = SymbolInfo(index, True)
                    if self._is_var(quar.src2):
                        quar.info_src2 = blockSymbolInfoTable[block].get(quar.src2, SymbolInfo())
                        blockSymbolInfoTable[block][quar.src2] = SymbolInfo(index, True)
                    if quar.op[0] != "j":    # 不是条件跳转（tar是地址）
                        if self._is_var(quar.tar):
                            quar.info_tar = blockSymbolInfoTable[block].get(quar.tar, SymbolInfo())
                            blockSymbolInfoTable[block][quar.tar] = SymbolInfo(None, False)

        log = ""
        for func, blocks in self.func_blocks.items():
            log += f"function: {func}\n"
            for block in blocks:
                log += f"\t {block.name}\n"
                log += f"\t use {block.use_set}\n"
                log += f"\t def {block.def_set}\n"
                log += f"\t in  {block.in_set}\n"
                log += f"\t out {block.out_set}\n"
                for quar in block.codes:
                    log += f"\t\t {quar}\n"

                log += f"\t\tnext1: {block.next1.name if block.next1 else None}\n"
                log += f"\t\tnext2: {block.next2.name if block.next2 else None}\n"

        with open("blockinfo.txt", "w") as file:
            file.write(log)

        '''
        for func, blocks in self.func_blocks.items():
            print("function:", func)
            for block in blocks:
                print('\t' + block.name)
                for quar in block.codes:
                    print('\t\t', quar)


                print('\t\tuse:', block.use_set)
                print('\t\tdef:', block.def_set)
                print('\t\tin:', block.in_set)
                print('\t\tout:', block.out_set)
                print('\t\tnext1:', block.next1.name if block.next1 else None)
                print('\t\tnext2:', block.next2.name if block.next2 else None)
        '''