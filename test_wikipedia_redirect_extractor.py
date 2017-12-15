#!/usr/bin/env python

import io
from xml.sax import make_parser

from wikipedia_redirect_extractor import resolve_multiple_redirects
from wikipedia_redirect_extractor import WikiPediaParser

redirect_map = {'Arno': ['Asc', 'wl'],
                'Scharl': ['Arno', 'ARN'],
               }

def test_resolve_multiple_redirects():
    result = {'Scharl': ['Arno', 'ARN', 'Asc', 'wl']}
    print(resolve_multiple_redirects(redirect_map))
    assert result == resolve_multiple_redirects(redirect_map)

def test_parser():
    XML = io.StringIO("""<page>
    <title>AT&amp;T Bell Laboratories</title>
    <ns>0</ns>
    <id>2681082</id>
    <redirect title="Bell Labs" />
    <revision>
      <id>730868459</id>
      <parentid>721130357</parentid>
      <timestamp>2016-07-21T14:14:34Z</timestamp>
      <contributor>
        <username>Xqbot</username>
        <id>8066546</id>
      </contributor>
      <minor />
      <comment>Bot: Fixing double redirect to [[Bell Labs]]</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">#REDIRECT [[Bell Labs]]</text>
      <sha1>6s0q2pbnwvsrnejkcfqayc5zt4ln348</sha1>
    </revision>
    </page>""")

    reader = WikiPediaParser(make_parser())
    reader.parse(XML)

    assert 'AT&T Bell Laboratories' in reader.mapping['Bell Labs']
