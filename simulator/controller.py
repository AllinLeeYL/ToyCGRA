from DMA import DMA
from scratchpad import ScratchPadMemory
from PE import SimplePEArray
from logger import logger as log

class SimpleController:
    def __init__(self, pe_row_size, pe_col_size, scratchpad_mem_size) -> None:
        """
        Simple controller, top module of the architecture.
        :param pe_row_size: PE array row size
        :param pe_col_size: PE array column size
        :param scratchpad_mem_size: scratchpad memory size
        """
        self.count = 0
        self.totalCount = 0
        self.scratchPadMem = ScratchPadMemory(scratchpad_mem_size)
        self.PEArray = SimplePEArray(pe_row_size, 
                                     pe_col_size)
        log.info('PE row size: ' + str(pe_row_size) + '\tPE col size: ' + str(pe_col_size))

    def setup_global_config_memory(self, globalCfgMem) -> None:
        """
        Set up global config memory.
        :param cfgMem: config memory content with PE instructions
        """
        self.globalCfgMem = globalCfgMem
        self.totalCount = len(globalCfgMem)

    def setup_scratchpad_memory(self, scratchPadMem):
        """
        Set up scratchpad Memory
        :param scratchPadMem: scratchpad memory storing the data
        """
        self.scratchPadMem.setup(scratchPadMem)

    def tick(self) -> None:
        """
        Clock ticks once.
        """
        try:
            assert(self.count < self.totalCount)
        except:
            logger.logger.error('no more instructions to execute!')
            exit()
        inst = self.globalCfgMem[self.count] # fetch instruction
        self.PEArray.tick(inst, self.scratchPadMem)
        self.count += 1

    def log_state(self) -> None:
        self.PEArray.log_state()

    def end(self) -> bool:
        """
        Determine if the end has been reached
        """
        return self.count == self.totalCount
