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
    parser.add_argument('format', default='csv', help='Serialization format (csv*|turtle)')
    return parser


def parse_file(src):
    ''' parses the given input file '''
    
    # create mapping
    mapping = defaultdict(lambda: defaultdict(int))
    with lzma.open(src) as f:
        for no, line in enumerate(f):
            try:
                link_text, link_target = [cell.strip() for cell in line.decode('utf-8', errors='ignore').split('\t')]
                mapping[link_text][link_target] += 1
                if no % CNT_INTERVALL == 0 and no != 0:
                    print("Parsed {} lines yielding {} linkings.".format(no, len(mapping)))
            except ValueError:
                print("Error parsing line '{}'.".format(line))

    return mapping

def serialize_csv(dst, mapping):
    ''' serialize the mapping to a csv file '''
    with lzma.open(dst, 'w') as f:
        for link_text, link_targets in mapping.items():
            # skip ambiguous links
            if len(link_targets) > 1:
                continue

            # skip links text that is a prefix of the target (e.g. Pope for Pope Benedikt)
            link_target = list(link_targets.keys()).pop()
            if link_target.startswith(link_text):
                continue

            f.write("{}\t{}\t{}\n".format(link_text, link_target, list(link_targets.values()).pop()).encode('utf-8'))

def serialize_turtle(dst, mapping):
    ''' serialize the mapping to a turtle file '''
    with lzma.open(dst, 'w') as f:
        f.write("@prefix skos:<http://www.w3.org/2004/02/skos/core#>\n".encode('utf-8'))
        f.write("@prefix dbr:<http://dbpedia.org/resource/>\n".encode('utf-8'))
        for link_text, link_targets in mapping.items():
            # skip ambiguous links
            if len(link_targets) > 1:
                continue

            # skip links text that is a prefix of the target (e.g. Pope for Pope Benedikt)
            link_target = list(link_targets.keys()).pop()
            if link_target.startswith(link_text) or link_target.startswith('#'):
                continue

            link_target = link_target.replace(' ', '_')
            f.write("dbr:{}   skos:altLabel   \"{}\"\n".format(link_target, link_text).encode('utf-8'))


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    mapping = parse_file(src=args.input)

    if args.format == 'turtle':
        serialize_turtle(args.output, mapping)
    else:
        serialize_csv(args.output, mapping)
