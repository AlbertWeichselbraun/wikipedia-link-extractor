#!/usr/bin/env python

from html import unescape
from xml.sax import make_parser
from xml.sax.saxutils import XMLFilterBase
from collections import defaultdict

import argparse
import bz2
import lzma
import re
import json

RE_WIKI_LINK = re.compile(r'\[\[([^|^\]]+)\|([^|^\]]+)\]\]')
RE_REMOVE_HTML_TAGS = re.compile(r'<[^>^<]+?>')

PREFIX_BLACKLIST = ('user:', 'talk:', 'wikipedia:', 'file:', 'image', 'user talk:', 'user_talk:', 'file talk:', 'talk:', ':template:')
LINK_TEXT_BLACKLIST = ('thumb', )

TEXT_REPLACEMENTS = [("'''", ""), ("''", ""), ('"', ''), ('\xa0', ''), ('„', ''), ('“', ''), ('»', ''), ('»', '')]


class WikiPediaParser(XMLFilterBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mapping = defaultdict(list)
        self.title = ''
        self.redirect = None
        self.in_page = False
        self.in_title = False

    def startElement(self, name, attrs):
        if name == 'page':
            self.in_page = True
            if len(self.mapping) % 1000 == 0:
                print("Detected {} mappings.".format(len(self.mapping)))
        elif name == 'title' and self.in_page:
            self.in_title = True
        elif name == 'redirect' and self.in_page:
            self.redirect = attrs['title']
        

    def endElement(self, name):
        if name == 'page' and self.title and self.redirect:
            self.mapping[self.redirect].append(self.title)

        # new page - we need to clear title, redirect etc.
        if name == 'page':
            self.title = ''
            self.redirect = None
            self.in_page = False
        elif name == 'title':
            self.in_title = False


    def characters(self, content):
        if self.in_title:
            self.title += content


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


def get_parser():
    ''' Parses the arguments if script is run directly via console '''
    parser = argparse.ArgumentParser(description='Extract links and link texts from Wikipedia XML dumps')
    parser.add_argument('input', help='Wikipedia .bz2 dump to parse.')
    parser.add_argument('output', help='LZMA compressed output file name.')
    return parser


def resolve_multiple_redirects(redirect_map):
    # redirects that are in turn redirected
    for target, aliases in redirect_map.copy().items():
        for alias in aliases:
            if alias in redirect_map:
                redirect_map[target].extend(redirect_map[alias])
                del redirect_map[alias]
                print("Deleted alias '{}' which maps to '{}'.".format(alias, target))

    return redirect_map


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    reader = WikiPediaParser(make_parser())
    with bz2.open(args.input) as f:
        reader.parse(f)
    
    with lzma.open(args.output, 'w') as f:
        json_string = json.dumps(reader.mapping, sort_keys=True, indent=4)
        f.write(json_string.encode('utf-8'))

