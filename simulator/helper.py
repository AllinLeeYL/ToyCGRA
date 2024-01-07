# PE Instructions

FUNC_IDLE = 0b00
FUNC_LS = 0b01
FUNC_R = 0b10
FUNC_I = 0b11

OP_LOAD = 0b0
OP_STORE = 0b1

OP_ADD = 0b0000
OP_SUB = 0b0001
OP_SHIFT_LEFT = 0b0010
OP_SHIFT_RIGHT = 0b0011
OP_MUL = 0b0100
OP_DIV = 0b0101
OP_ABS = 0b0110
OP_ACTIVATION = 0b0111

SRC_EAST = 0b000
SRC_SOUTH = 0b001
SRC_WEST = 0b010
SRC_NORTH = 0b011
SRC_WESTSOUTH = 0b100 # not used
SRC_WESTNORTH = 0b101 # not used
SRC_SELF = 0b110
SRC_NONE = 0b111

def func_field(inst):
    return inst & 0b0000_0000_0000_0011

def op_field(inst):
    return (inst & 0b0000_0000_0011_1100) >> 2

def lsop_field(inst):
    return (inst & 0b0000_0000_0000_0100) >> 2

def src1R_field(inst):
    return (inst & 0b0001_1100_0000_0000) >> 10

def src2R_field(inst):
    return (inst & 0b1110_0000_0000_0000) >> 13

def src1I_field(inst):
    return (inst & 0b0000_0001_1100_0000) >> 6

def imm_field(inst):
    return (inst & 0b1111_1110_0000_0000) >> 9

def addr_field(inst):
    return (inst & 0b1111_1111_1111_1000) >> 3

def decode(inst) -> tuple:
    """
    Decode inst into (func, yields) tuple format
    """
    func = func_field(inst)
    if func == FUNC_IDLE:
        return func, None
    elif func == FUNC_LS:
        return func, {'addr':addr_field(inst), 'l/s':lsop_field(inst)}
    elif func == FUNC_R:
        return func, {'src2':src2R_field(inst), 'src1':src1R_field(inst), 'op':op_field(inst)}
    else:
        return func, {'imm':imm_field(inst), 'src1':src1I_field(inst), 'op':op_field(inst)}

def assemble_ls_inst(addr, ls):
    return (addr << 3) + (ls << 2) + FUNC_LS

def assemble_r_inst(src2, src1, op):
    return (src2 << 13) + (src1 << 10) + (op << 2) + FUNC_R

def assemble_i_inst(imm, src1, op):
    return (imm << 9) + (src1 << 6) + (op << 2) + FUNC_I