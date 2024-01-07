import sys

class DMA:
    def __init__(self, latency_setup: int, 
                 latency_transfer_byte: float) -> None:
        # parameters
        self.latency_setup = latency_setup
        self.latency_transfer_byte = latency_transfer_byte
        # state variable
        self.prefetch_in_progress = False
        self.writeback_in_progress = False
        self.delay_prefetch = 0
        self.delay_writeback = 0
        self.count_prefetch = 0
        self.count_writeback = 0
        # ack
        self.ack_to_compute_device = False

    def prefetch(self, dest:int, src:int, n:int) -> None:
        # TODO: memcpy? reference to dma.hh:25
        self.delay_prefetch = self.calculate_data_transfer_delay(n)
        self.prefetch_in_progress = True

    def write_back(self, dest:int, src:int, n:int) -> None:
        # TODO: memcpy? reference to dma.hh:40
        self.delay_writeback = self.calculate_data_transfer_delay(n)
        self.writeback_in_progress = True

    def execute_tick(self) -> None:
        if self.prefetch_in_progress:
            if self.count_prefetch < self.delay_prefetch:
                self.ack_to_compute_device = False
                self.count_prefetch += 1
            elif self.count_prefetch == self.delay_prefetch:
                self.ack_to_compute_device = True
                self.count_prefetch = 0
                self.prefetch_in_progress = False
            else:
                print('wrong DMA state', file=sys.stderr)
                raise AssertionError
        elif self.writeback_in_progress:
            if self.count_writeback < self.delay_writeback:
                self.ack_to_compute_device = False
                self.count_writeback += 1
            elif self.count_writeback == self.delay_writeback:
                self.ack_to_compute_device = True
                self.count_writeback = 0
                self.writeback_in_progress = False
            else:
                print('wrong DMA state', file=sys.stderr)
                raise AssertionError
        else:
            self.ack_to_compute_device = False

    def interface_host(self, bus_req: bool) -> None:
        self.req_from_compute_device = bus_req

    def get_ack_bus(self) -> bool:
        return self.ack_to_compute_device
    
    def calculate_data_transfer_delay(self, n:int) -> int:
        total_dma_latency = self.latency_setup + (self.latency_transfer_byte * n)
        # TODO: execution_cycles = total_dma_latency * accelerator_freq / DMA_freq
        # return execution_cycles
        