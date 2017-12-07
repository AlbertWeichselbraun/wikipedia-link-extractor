#!/usr/bin/env python

from html import unescape
from collections import defaultdict

import argparse
import lzma

CNT_INTERVALL = 100000

def get_parser():
    ''' Parses the arguments if script is run directly via console '''
    parser = argparse.ArgumentParser(description='Return the unique mappings from the CSV file.')
    parser.add_argument('input', help='CSV output to parse.')
    parser.add_argument('output', help='Output file')
    return parser


def parse_file(src, dst):
    ''' parses the given input file '''
    
    # create mapping
    mapping = defaultdict(lambda: defaultdict(int))
    with lzma.open(src) as f:
        for no, line in enumerate(f):
            try:
                link_text, link_target = [cell.strip() for cell in line.decode('utf-8', errors='ignore').split('\t')]
                mapping[link_text][link_target] += 1
                if no % CNT_INTERVALL == 0:
                    print("Parsed {} lines yielding {} linkings.".format(no, len(mapping)))
            except ValueError:
                print("Error parsing line '{}'.".format(line))
    
    # serialize mapping
    with lzma.open(dst, 'w') as f:
        for link_text, link_targets in mapping.items():
            if len(link_target) > 1:
                continue

            f.write("{}\t{}\t{}\n".format(link_text, link_target.keys()[0], link_target.values()[0]))

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    parse_file(src=args.input, dst=args.output)
