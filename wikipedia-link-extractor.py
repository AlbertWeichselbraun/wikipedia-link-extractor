#!/usr/bin/env python

from html import unescape

import argparse
import bz2
import lzma
import re

RE_WIKI_LINK = re.compile(r'\[\[([^|^\]]+)\|([^|^\]]+)\]\]')
RE_REMOVE_HTML_TAGS = re.compile(r'<[^>^<]+?>')

PREFIX_BLACKLIST = ('user:', 'talk:', 'wikipedia:', 'file:', 'image', 'user talk:', 'user_talk:', 'file talk:', 'talk:', ':template:')
LINK_TEXT_BLACKLIST = ('thumb', )

TEXT_REPLACEMENTS = [("'''", ""), ("''", ""), ('"', ''), ('\xa0', ''), ('„', ''), ('“', ''), ('»', ''), ('»', '')]

def clean_text(text):
    # handle (multiple) encoded text
    count = 0
    while '&' in text and ';' in text and count < 3:
        count += 1
        text = unescape(text)

    # handle html text
    count =0
    while '<' in text and '>' in text and count < 3:
        count += 1
        text = RE_REMOVE_HTML_TAGS.sub('', text)

    # cleanup text
    for src, dst in TEXT_REPLACEMENTS:
        text = text.replace(src, dst)

    return text


def get_parser():
    ''' Parses the arguments if script is run directly via console '''
    parser = argparse.ArgumentParser(description='Extract links and link texts from Wikipedia XML dumps')
    parser.add_argument('input', help='Wikipedia .bz2 dump to parse.')
    parser.add_argument('output', help='LZMA compressed output file name.')
    return parser


def is_blacklisted_target(link_target):
    ''' blacklist special wikipedia namespaces such as 'User:', 'File:', ...
        without blocking legitimate pages that contain a ': '.
    '''
    if not ':' in link_target:
        return False
    elif ': ' not in link_target:
        return True

    for blacklist_prefix in PREFIX_BLACKLIST:
        if link_target.lower().startswith(blacklist_prefix):
            return True

    return False

def parse_file(src, dst):
    ''' parses the given input file '''
    with bz2.open(src) as f, lzma.open(dst, 'w') as g:
        for line in f:
            for link_target, link_text in RE_WIKI_LINK.findall(line.decode('utf-8', errors='ignore')):
                link_text = clean_text(link_text)
                if is_blacklisted_target(link_target) or link_text in LINK_TEXT_BLACKLIST or link_text.isdigit():
                    continue
                g.write("{}\t{}\n".format(link_text, link_target).encode('utf-8'))


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    parse_file(src=args.input, dst=args.output)
