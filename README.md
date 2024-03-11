# ToyCGRA
Usage: `python3 simulator/sim.py --exedir test/dummy`

```
usage: sim.py [-h] [--pe_row_size PE_ROW_SIZE] [--pe_col_size PE_COL_SIZE] [--scratchpad_mem_size SCRATCHPAD_MEM_SIZE]
              [--search_args SEARCH_ARGS] [--exedir EXEDIR] [--log_fname LOG_FNAME] [--log_level LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --pe_row_size PE_ROW_SIZE
                        *PE row size.
  --pe_col_size PE_COL_SIZE
                        *PE column size.
  --scratchpad_mem_size SCRATCHPAD_MEM_SIZE
                        *scratchpad memory size.
  --search_args SEARCH_ARGS
                        searchable design arguments, can be "pe_row_size,pe_col_size,cfg_mem_size"
  --exedir EXEDIR
  --log_fname LOG_FNAME
  --log_level LOG_LEVEL
                        debug true: print every cycle's PE state to log file
```
