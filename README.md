# ToyCGRA

## Introduction

This repository's object is to build a framework make test, evaluate and implement CGRA easier. 

Currently the simulator supports only 1 architecture as below. Each PE is able to finish ALU function and Load/Store Function. 

```
 ┌──┐   ┌──┐   ┌──┐   ┌──┐ 
 │PE│ - │PE│ - │PE│ - │PE│ 
 └──┘   └──┘   └──┘   └──┘ 
  |      |      |      |    
 ┌──┐   ┌──┐   ┌──┐   ┌──┐ 
 │PE│ - │PE│ - │PE│ - │PE│ 
 └──┘   └──┘   └──┘   └──┘ 
  |      |      |      |   
 ┌──┐   ┌──┐   ┌──┐   ┌──┐ 
 │PE│ - │PE│ - │PE│ - │PE│ 
 └──┘   └──┘   └──┘   └──┘ 
  |      |      |      |   
 ┌──┐   ┌──┐   ┌──┐   ┌──┐ 
 │PE│ - │PE│ - │PE│ - │PE│ 
 └──┘   └──┘   └──┘   └──┘ 
```

## Usage

Example: `python3 simulator/sim.py --exedir test/dummy`

```
usage: sim.py [-h] [--pe_row_size PE_ROW_SIZE] [--pe_col_size PE_COL_SIZE] [--scratchpad_mem_size SCRATCHPAD_MEM_SIZE]
              [--exedir EXEDIR] [--log_fname LOG_FNAME] [--log_level LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --pe_row_size PE_ROW_SIZE
                        *PE row size.
  --pe_col_size PE_COL_SIZE
                        *PE column size.
  --scratchpad_mem_size SCRATCHPAD_MEM_SIZE
                        *scratchpad memory size.
  --exedir EXEDIR       the directory where PE instructions locate.
  --log_fname LOG_FNAME
                        where the log file is stored.
  --log_level LOG_LEVEL
                        logging level (int): CRITICAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10, NOTSET =
                        0
```

## PE ISA Definition

- 16bit
- 3 types instruction: load/store instruction and R type instruction and I type instruction

### Instruction Types

- load/store inst

| 15:3 | 2 | 1:0 |
| --- | --- | --- |
| address | load/store operation | function |

- R type inst

| 15:13 | 12:10 | 9:6 | 5:2 | 1:0 |
| --- | --- | --- | --- | --- |
| src2 | src1 | unused | operation | function |

- I type inst

| 15:9 | 8:6 | 5:2 | 1:0 |
| --- | --- | --- | --- |
| immediate | src1 | operation | function |

### Codec Description

Function Codec

| value | description |
| --- | --- |
| 00 | Idle |
| 01 | load/store inst |
| 10 | R type inst |
| 11 | I type inst |

Operation Codec

| Bits | Description |
| --- | --- |
| 0000 | add |
| 0001 | sub |
| 0010 | shift left |
| 0011 | shift right |
| 0100 | mul |
| 0101 | div |
| 0110 | abs |
| 0111 | activation |

Source Codec

| Bits | Description |
| --- | --- |
| 000 | east |
| 001 | south |
| 010 | west |
| 011 | north |
| 100 | westsouth |
| 101 | westnorth |
| 110 | self |
| 111 | none |

Load/Store Codec

| Bits | Description |
| --- | --- |
| 0 | load |
| 1 | store |