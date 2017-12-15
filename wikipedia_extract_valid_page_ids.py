#!/usr/bin/env python

'''
generates a list of valid page ids for the given dbpedia version
'''

from urllib.request import urlopen

import lzma
import bz2

VERSIONS = {'2016-10-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/2016-10/core-i18n/en/page_ids_en.ttl.bz2',
            '2016-04-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/2016-04/core-i18n/en/page_ids_en.ttl.bz2',
            '2015-10-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/2015-10/core-i18n/en/page_ids_en.ttl.bz2',
            '2015-04-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/2015-04/core-i18n/en/page-ids_en.ttl.bz2',
            '3.9-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.9/en/page_ids_en.ttl.bz2',
            '3.8-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.8/en/page_ids_en.ttl.bz2',
            '3.7-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.7/en/page_ids_en.nt.bz2',
            '3.6-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.6/en/page_ids_en.nt.bz2',
            '3.5-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.5/en/page_ids_en.nt.bz2',
            '3.4-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.4/en/articles_label_en.nt.bz2',
            '3.3-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.3/en/articles_label_en.nt.bz2',
            '3.2-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.2/en/articles_label_en.nt.bz2',
            '3.1-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.1/en/articles_label_en.nt.bz2',
            '3.0-entity_list_en.txt.xz': 'http://downloads.dbpedia.org/3.0/en/articles_label_en.nt.bz2',
            }

TMP_FILE = '.dbpedia.bz2'

def download_and_parse_dbpedia_file(url, fname):
    '''
    This downloads, decompresses and parses the dbpedia file and records all
    resources (?s) in these files
    '''
    with urlopen(url) as response:
        content = response.read()

    with open(TMP_FILE, 'wb') as f:
        f.write(content)

    with bz2.open(TMP_FILE) as src, lzma.open(fname, 'w') as dst:
        for line in src:
            resource = line.decode('utf-8').split('> <')[0][1:]
            dst.write(resource.encode('utf-8')+b'\n')


if __name__ == '__main__':
    for fname, url in VERSIONS.items():
        print("Creating entity list '{}' from '{}'.".format(fname, url))
        download_and_parse_dbpedia_file(url, fname)
