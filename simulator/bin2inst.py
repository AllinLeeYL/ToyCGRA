import yaml
import helper
import sys
import os

def load_pe_inst(path):
    with open(path, 'r', encoding='utf-8') as f:
        PEInst = yaml.load(f, yaml.CLoader)
    return PEInst

def op2bin(op):
    if op == 'ADD':
        return helper.OP_ADD
    elif op == 'SUB':
        return helper.OP_SUB
    elif op == 'SHIFT_LEFT':
        return helper.OP_SHIFT_LEFT
    elif op == 'SHIFT_RIGHT':
        return helper.OP_SHIFT_RIGHT
    elif op == 'MUL':
        return helper.OP_MUL
    elif op == 'DIV':
        return helper.OP_DIV
    elif op == 'ABS':
        return helper.OP_ABS
    elif op == 'ACTIVATION':
        return helper.OP_ACTIVATION
    else:
        raise Exception

def src2bin(src):
    if src == 'EAST':
        return helper.SRC_EAST
    elif src == 'SOUTH':
        return helper.SRC_SOUTH
    elif src == 'WEST':
        return helper.SRC_WEST
    elif src == 'NORTH':
        return helper.SRC_NORTH
    elif src == 'WESTSOUTH':
        return helper.SRC_WESTSOUTH
    elif src == 'WESTNORTH':
        return helper.SRC_WESTNORTH
    elif src == 'SELF':
        return helper.SRC_SELF
    elif src == 'NONE':
        return helper.SRC_NONE
    else:
        raise Exception

def process_single_inst(inst):
    try:
        if inst[-1] == 'IDLE':
            return helper.FUNC_IDLE
        elif inst[-1] == 'LS':
            ls = helper.OP_LOAD if inst[-2] == 'LOAD' else helper.OP_STORE
            addr = int(inst[-3])
            return helper.assemble_ls_inst(addr, ls)
        elif inst[-1] == 'R':
            op = op2bin(inst[-2])
            src1 = src2bin(inst[-3])
            src2 = src2bin(inst[-4])
            return helper.assemble_r_inst(src2, src1, op)
        elif inst[-1] == 'I':
            op = op2bin(inst[-2])
            src1 = src2bin(inst[-3])
            imm = int(inst[-4])
            return helper.assemble_i_inst(imm, src1, op)
        else:
            raise Exception
    except:
        print('not recognized instruction:', inst)
        exit()

def convert2bin(PEInst):
    for c in range(len(PEInst)): # every clock
        for i in range(len(PEInst[0])): # every row
            for j in range(len(PEInst[0][0])): # every column
                inst = PEInst[c][i][j].replace(' ', '').split(',')
                PEInst[c][i][j] = process_single_inst(inst)
    return PEInst

def write2file(PEInst, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(PEInst, f)

if __name__ == '__main__':
    inputFilePath = sys.argv[1]
    inputDirName = os.path.dirname(inputFilePath)
    outputFileName = inputFilePath[:-4]+'.bin'
    PEInst = load_pe_inst(sys.argv[1])
    PEInst = convert2bin(PEInst)
    # print(PEInst)
    write2file(PEInst, outputFileName)