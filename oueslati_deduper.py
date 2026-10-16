#!/usr/bin/env python

import argparse

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






