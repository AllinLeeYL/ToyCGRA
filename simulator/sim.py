from controller import SimpleController
import helper
import argparse, os, yaml, datetime, logger, logging
from logger import logger as log

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pe_row_size', type=int, default=2,
                        help='*PE row size.')
    parser.add_argument('--pe_col_size', type=int, default=2,
                        help='*PE column size.')
    parser.add_argument('--scratchpad_mem_size', type=int, default=2**13,
                        help='*scratchpad memory size.')
    # TODO: design space exploration
    # parser.add_argument('--search_args', type=str, default=None,
    #                     help='searchable design arguments, can be \"pe_row_size,pe_col_size,cfg_mem_size\"')
    # path
    parser.add_argument('--exedir', type=str, default='test/dummy',
                        help='the directory where PE instructions locate.')
    # logging
    parser.add_argument('--log_fname', type=str, default='sim.log',
                        help='where the log file is stored.')
    parser.add_argument('--log_level', type=int, default=logging.DEBUG,
                        help='logging level (int): CRITICAL = 50, ERROR = 40, WARNING = 30, INFO = 20, DEBUG = 10, NOTSET = 0')
    args = parser.parse_args()
    return args

def load_PEInst(path):
    # load file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            PEInst = yaml.load(f, yaml.CLoader)
            # parse file
            for c in range(len(PEInst)):
                for i in range(len(PEInst[0])):
                    for j in range(len(PEInst[0][0])): # each PE
                        PEInst[c][i][j] = int(PEInst[c][i][j]) # each instruction
            return PEInst
    except:
        log.error('Please check if the file ' + path + ' exists or is in the right format.')
        exit()

def load_config(path):
    # load config file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f, yaml.CLoader)
            log.info('Using config file: ' + path)
            return config
    except:
        log.warning('Please check if the file ' + path + ' exists or is in the right format.' + ' Use the default config instead.')
        return {}
    
def apply_config(config: dict, args):
    for key, value in config.items():
        if isinstance(getattr(args, key), int):
            setattr(args, key, int(value))
        elif isinstance(getattr(args, key), float):
            setattr(args, key, float(value))
        else:
            pass
    return args

if __name__ == '__main__':
    args = parse_argument()
    # logger
    logger.setup_logger(args.log_fname, args.log_level)
    log.info(datetime.datetime.now())
    log.info('log file is ' + os.path.abspath(args.log_fname))
    # load config
    config = load_config(os.path.join(args.exedir, 'config.yml'))
    args = apply_config(config, args)
    # load PE instructions
    PEInst = load_PEInst(os.path.join(args.exedir, 'PEInstructions.bin'))
    # controller
    controller = SimpleController(args.pe_row_size, 
                                  args.pe_col_size, 
                                  args.scratchpad_mem_size)
    controller.setup_global_config_memory(PEInst)
    # execute
    while not controller.end():
        controller.tick()
        controller.log_state()