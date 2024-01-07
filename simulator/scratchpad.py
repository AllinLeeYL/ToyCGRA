
class ScratchPadMemory:
    def __init__(self, size: int) -> None:
        """
        On-chip memory
        :param size: size of scratchpad memory
        """
        self.size: int = size
        self.data: list = [0 for i in range(0, self.size)]

    def setup(self, data: list) -> None:
        """
        Fill in scratchpad memory with data
        :param data: data to be filled into the scratchpad
        """
        self.data = data

    def read(self, i: int):
        """
        Read data[i] from scratchpad
        :param i: index
        """
        return self.scratchPad[i]
    
    def write(self, i: int, v):
        """
        Write value v to data[i]
        :param i: index
        :param v: value
        """
        self.scratchPad[i] = v