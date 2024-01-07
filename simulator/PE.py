import helper
import logger

class PE():
    def __init__(self) -> None:
        """
        Simple PE without config memory.
        """
        self.reg = 0 # storing the value to be written into the regfile
        self.lastCycleReg = 0 # storing last cycle's regfile value

    def tick(self):
        pass

    def get_val(self):
        """
        Get the value of current PE.
        """
        return self.lastCycleReg

    def update(self):
        """
        Write current cycle's result into regfile.
        """
        self.lastCycleReg = self.reg



class SimplePE(PE):
    def __init__(self) -> None:
        """
        Simple PE without config memory.
        """
        self.reg = 0 # storing the value to be written into the regfile
        self.lastCycleReg = 0 # storing last cycle's regfile value

    def tick(self, inst, east, south, west, north, scratchPadMem) -> None:
        """
        Clock ticks once.
        :param inst: single instruction
        :param east: PE value to the east
        :param south: PE value to the south
        :param west: PE value to the west
        :param north: PE value to the north
        """
        func, fields = helper.decode(inst)
        if func == helper.FUNC_IDLE:
            return None
        elif func == helper.FUNC_LS:
            self.execute_ls_inst(fields, scratchPadMem)
        elif func == helper.FUNC_R:
            self.execute_r_inst(fields, east, south, west, north)
        elif func == helper.FUNC_I:
            self.execute_i_inst(fields, east, south, west, north)
        else:
            log.error('func codec ' + str(func) + ' is not right!')
            exit()

    def execute_ls_inst(self, fields, scratchPadMem):
        """
        Execute load/store instruction
        :param fields: instruction fields
        :param scratchPadMem: scratchpad memory
        """
        addr = fields['addr']
        if fields['l/s'] == helper.OP_LOAD:
            self.reg = scratchPadMem.read(addr)
        else:
            scratchPadMem.write(addr, self.reg)

    def execute_r_inst(self, fields, east, south, west, north):
        """
        Execute R type instruction
        :param fields: instruction fields
        :param east: PE value to the east
        :param south: PE value to the south
        :param west: PE value to the west
        :param north: PE value to the north
        """
        op = fields['op']
        src1 = self.decide_src(fields['src1'], east, south, west, north)
        src2 = self.decide_src(fields['src2'], east, south, west, north)
        self.execute_2src_op(op, src1, src2)

    def execute_i_inst(self, fields, east, south, west, north):
        """
        Execute I type instruction
        :param fields: instruction fieldsr
        :param east: PE value to the east
        :param south: PE value to the south
        :param west: PE value to the west
        :param north: PE value to the north
        """
        op = fields['op']
        src1 = self.decide_src(fields['src1'], east, south, west, north)
        src2 = fields['imm']
        self.execute_2src_op(op, src1, src2)

    def execute_2src_op(self, op, src1, src2):
        """
        Execute 2-source operand type instruction
        :param op: operation
        :param src1: source operand 1
        :param src2: source operand 2
        """
        if op == helper.OP_ADD:
            self.reg = src1 + src2
        elif op == helper.OP_SUB:
            self.reg = src1 - src2
        elif op == helper.OP_SHIFT_LEFT:
            self.reg = src1 << src2
        elif op == helper.OP_SHIFT_RIGHT:
            self.reg = src1 >> src2
        elif op == helper.OP_MUL:
            self.reg = src1 * src2
        elif op == helper.OP_DIV:
            self.reg = src1 / src2
        elif op == helper.OP_ABS:
            self.reg = abs(src1) 
        elif op == helper.OP_ACTIVATION:
            self.reg = max(src1, 0)
        else:
            log.error('unsupported operation ' + str(op))
            exit()

    def decide_src(self, src, east, south, west, north):
        """
        Decide which source operand to use and return it.\
        :param op: operation code
        :param east: PE value to the east
        :param south: PE value to the south
        :param west: PE value to the west
        :param north: PE value to the north
        """
        if src == helper.SRC_NONE:
            return 0
        elif src == helper.SRC_SELF:
            return self.get_val()
        elif src == helper.SRC_EAST:
            return east
        elif src == helper.SRC_SOUTH:
            return south
        elif src == helper.SRC_WEST:
            return west
        elif src == helper.SRC_NORTH:
            return north
        else:
            log.error('not supported source operand ' + bin(src))
            exit()



class SimplePEArray:
    def __init__(self,
                 rowSize: int,
                 colSize: int) -> None:
        """
        Simple PE array.
        :param rowSize: row size of PE array
        :param colSize: column size of PE array
        """
        self.rowSize = rowSize
        self.colSize = colSize
        self.PEArray = [[SimplePE() for j in range(colSize)] for i in range(rowSize)]

    def tick(self, PEInst, scratchPadMem):
        """
        Execute the inst for every PE.
        :param inst: instructions for every PE to execute
        """
        # execute operation
        for i in range(self.rowSize):
            for j in range(self.colSize):
                inst = PEInst[i][j] # fetch instruction
                # fetch neighboring nodes' value
                east = self.PEArray[i][j+1].get_val() if j < self.colSize - 1 else None
                south = self.PEArray[i+1][j].get_val() if i < self.rowSize - 1 else None
                west = self.PEArray[i][j-1].get_val() if j >= 1 else None
                north = self.PEArray[i-1][j].get_val() if i >= 1 else None

                self.PEArray[i][j].tick(inst, east, south, west, north, scratchPadMem) # execute
        # update regfile
        for i in range(self.rowSize):
            for j in range(self.colSize):
                self.PEArray[i][j].update()

    def log_state(self):
        """
        Write PE array's state into log file.
        """
        string = ''
        for i in range(self.rowSize):
            string += '--'
        logger.logger.debug(string)
        for i in range(self.rowSize):
            string = ''
            for j in range(self.colSize):
                string += str(self.PEArray[i][j].get_val()) + ' '
            logger.logger.debug(string)