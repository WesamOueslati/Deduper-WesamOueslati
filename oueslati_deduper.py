#!/usr/bin/env python

import argparse
import re
# import hashlib
import gzip

EPILOG = """Usage: ./oueslati_deduper.py -u STL96.txt -f <in.sam> -o <out.sam> """

def get_args():
    parser = argparse.ArgumentParser(
        prog = 'Deduper',
        description = 'Reference Based PCR Duplicate Removal tool',
        epilog=EPILOG)
    parser.add_argument('-f', '--file', help='Absolute file path to sorted sam file', required=True)
    parser.add_argument('-o', '--outfile', help='Absolute file path to deduplicated sam file',  required=True)
    parser.add_argument('-u', '--umi', help='Absolute file path to deduplicated sam file',  required=True)
    return parser.parse_args()


def calc_adj_start(pos: int, cigar: str, rev_comp: bool) -> int:
    """ Find the 5' position of an alignment
    
    Parameters
    ----------
        pos: int 
            The leftmost alignment position
        cigar: str
            The cigar string associated with the alignment
        rev_comp: bool
            True is the read aligns to the reverse strand
        
    Returns
    -------
        int
            The 5' position
    """
    MODS = ['N', 'D', 'M'] ## <- removed the I since insertions consume query not the reference
    start = int(pos)
    
    comps = parse_cigar(cigar)
    # soft clipping
    r_sc = int(comps[-1].strip('S')) if comps[-1][-1] == 'S' else 0
    l_sc = int(comps[0].strip('S')) if comps[0][-1] == 'S' else 0
    
    if not rev_comp:
        start = start - l_sc
    else:
        offset = 0
        for comp in comps:
            if comp[-1] in MODS:
                # print(int(comp[:-1]))
                offset += int(comp[:-1])
        start = start + offset + r_sc
    return start

def parse_cigar(cigar: str) -> list:
    """
    Parameters
    ----------
        cigar: str
            The cigar string associated with the alignment
            
    Returns
    -------
            A list of modifications applied based on the cigar string (modifications = 'S', 'N', 'M', 'I', 'D') 
    """
    mod = re.sub(r'(\D+)(\d+)', r'\1\t\2', cigar)    
    comps = mod.split('\t')
    return comps

def extract_cols(line) -> list:
    """
    Parameters
    ---------- 
        line: str
            A line from a sam file
            
    Returns
    -------
        umi: str
            The umi associated with the aligned read
        pos: str
            The 1-based left-most starting position of the alignment
        cigar: str
            The cigar string associated withe the alignment
        flag: str
            The flag associated with the alignment
        rname: str
            The reference name: Chromosome/Contig read aligned to.
    """
    cols = line.split('\t')
    umi, pos, flag, cigar, rname = cols[0].split(':')[-1], cols[3], cols[1], cols[5], cols[2]
    return  umi, pos, cigar, flag, rname

# def hash(umi, start, rev_comp) -> str:
#     """ Returns a hash for an alignment based on the 5' start, umi, and rev_comp
#     Parameters
#     ----------
#         umi: str
#             The umi associated with the aligned read
#         start: int
#             The 5' starting position of the alignment
#         rev_comp: bool
#             The strand the read aligned to (True for reverse/ False for forward)
            
#     Returns
#     -------
#         hashed: Hash Object (don't know the exact name yet)
#             A hash for the alignement
#     """
#     concat = umi + str(start) + str(rev_comp)
#     # hashed = hashlib.sha256(concat)    
#     return concat

def is_rev(flag) -> bool:
    """ Checks whether the read maps to the reverse strand
    
    Parameters
    ----------
        flag: str
            The flag associated with the alignment
    Returns
    -------
        True if the read mapped to the reverse strand, else False
    """
    return (flag & 16) == 16

def is_unmapped(flag) -> bool:
    """ Checks whether the read is unmapped
    
    Parameters
    ----------
        flag: str
            The flag associated with the alignment
    Returns
    -------
        True if the read is unmapped, else False
    """
    return (flag & 4) == 4

def extract_umis(umi_file) -> list[str]:
    """ Extracts a list of umis from a file
    
    Parameters
    ----------
        umi_file: str
            File path to text file containing the umis, each on a separate line
    Returns
    -------
        umi_list: list[str]
            List containing all the umis from the input file
    """
    umi_list = []
    with open(umi_file, 'rt') as fh:
        for umi in fh:
            umi = umi.strip()
            umi_list.append(umi)    
    return umi_list

def dedupe(input, output, umis) -> dict:
    """ Removes PCR duplicates from a sam file given a list of umis 
        and writes non duplicates to a specified output
    Parameters
    ----------
        input: str
            Path to the input sam file
        output: str
            Path to the output sam file
        umis: list[str]
            Path to the file containing the umis
    Returns
    -------
        stats: dict{str:int}
    """
    
    stats = {
        "header_lines": 0,
        "invalid_umis" : 0,
        "duplicates": 0,
        "unique_reads": 0,
        "unmapped_reads" : 0
    }
    # n_reads = 0
    hashes = {}
    umi_list = extract_umis(umis)
    prev_chr = ""
    
    # with open(input, 'rt') as fh, open(output, 'wt') as out, open('per_chrom.tsv', 'wt') as per_chrom:
    with open(input, 'rt') as fh, open(output, 'wt') as out:
        for line in fh:
            # Header lines are skipped
            if line.startswith('@'):
                out.write(line)
                stats["header_lines"] += 1
                continue
            
            line = line.strip('\n')
            umi, pos, cigar, flag, chr = extract_cols(line)
            
            # Empty records when moving on to next chr
            if chr != prev_chr:
                # per_chrom.write(f"{prev_chr}\t{n_reads}\n")
                # n_reads = 0
                hashes.clear()
                prev_chr = chr
            if umi not in umi_list: 
                stats["invalid_umis"] += 1
                continue
            if is_unmapped(int(flag)):
                stats["unmapped"] += 1
                continue
            
            rev_comp = is_rev(int(flag))
            start = calc_adj_start(pos, cigar, rev_comp)
            concat = umi + str(rev_comp)
            
            
            if start not in hashes: # <- first time we encounter a specific 5' starting position
                hashes[start] = []
                hashes[start].append(concat)
                out.write(f"{line}\n")
                stats['unique_reads'] += 1
                # n_reads += 1
            else: # <- 5' was encountered before
                if concat in hashes[start]: # <- # they also have the same umi and are on the same strand
                    stats["duplicates"] += 1
                else : # <- either have a different umi or are on a different strand
                    out.write(f"{line}\n")
                    hashes[start].append(concat)
                    stats['unique_reads'] += 1
                    # n_reads += 1
                    
        # per_chrom.write(f"{chr}\t{n_reads}")
    return stats

if __name__ == "__main__":
    assert parse_cigar('20M5N4T') == ['20M', '5N', '4T']
    # assert calc_adj_start('120', '2S2M15N1I5M5S', True) == 147
    
    args = get_args()
    input = args.file
    output = args.outfile
    umis = args.umi
    
    stats = dedupe(input, output, umis)
    print(stats)