# Deduper

## Problem Definition:
<p>
PCR duplicates originate when a DNA molecule is copied multiple times during amplification. This can skew results or produce biased results during analysis. So, we want to remove these duplicated before proceeding with analysis.
Given a sam file, we only want to keep a single copy of each sequence. That is, if multiple entries in the sam file originate from the same molecule, we want to remove all but one.
</p>

### Features associated with PCR duplicates:
- PCR duplicates have the same chr #
- PCR duplicates have the same adjusted position:
    - Need to account for soft clipped sequences by checking the 5' position as well
- PCR duplicates originate from the same strand
- PCR duplicates have the same UMI


## Pseudocode:
```
sam = sorted(sam) ## Primary sort via RNAME and subsort via POS using samtools

store first entry in memory (dict)
while True:
    while curr_read overlaps(stored_read):
        entry = read_line()
        if UMI(entry) not in UMI list: continue
        add(entry) to dict

    for entry in dict():
        calc_adjusted_start(CIGAR): finds the 5' start 
        split into two sets (forward reads and reverse reads)
        for each set:
            if start_positions_match() and are_aligned(CIGAR) and UMIs_match(): <- this marks a duplicate
            # are_aligned() checks if gaps, insertions and deletions are aligned in both sequences
                write only one entry to output
            else:
                write both entries to output
    if not EOF:
        clear_dict()
        read_line()
    else:
        exit_loop()

```

## Helper Functions:
``` python
def extract_UMI():
    """
    Extracts the unique molecular identified for each read from the header.
    input: QNAME
    output: UMI
    
    Example: 
        in: NS500451:154:HWKTMBGXX:1:11101:15364:1139:GAACAGGT
        out: GAACAGGT
    """


def extract_cols(): 
    """
    Extracts the starting position (POS) of the read.
    input: SAM entry
    output: list of items
    
    Example:
        in: NS500451:154:HWKTMBGXX:1:11101:16635:1076-GAGAANAG^GAAGACCA;0^0 83 11 67245662 36 71M = 67245443 -293 AGGTGTACAACTCCGTGGGTGCCCTGGCCAAGTCCATGTATGAGAAGATGTTCCTATGGATGGTCACCCGC
        out: [NS500451:154:HWKTMBGXX:1:11101:16635:1076-GAGAANAG^GAAGACCA;0^0, 83, 11, 67245662, 36, 71M, =, 67245443, -293]
    """

def calc_adj_start():
    """
    Finds the 5' start based on POS and soft clipping
    input: POS, CIGAR, rev_comp
    output: 5' position
    
    Example:
        in: 113, 2S5M, False
        out: 111
    """

def is_clipped():
    """
    Determines whether or not the read was soft clipped.
    input: CIGAR
    output: bool
    
    Example:
        in: 2S5M
        out: True
    """

def is_rev():
    """
    Determines whether or not the read was mapped to the reverse strand
    input: FLAG
    output: bool
    
    Example:
        in: 0000000010000
        out: True
    """

def process_cigar() → 
    """
    Finds all modifications that a CIGAR string contains
    input: CIGAR
    output: List of modifications
    
    Example:
        in: 2S5M3N5M
        out: ['S', 'M', 'N']
    """
```


