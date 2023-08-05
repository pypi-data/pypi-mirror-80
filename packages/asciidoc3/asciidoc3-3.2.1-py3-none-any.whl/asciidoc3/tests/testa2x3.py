#!/usr/bin/env python3

"""
Runs a bunch of a2x3.py testcases analogue to 'testasciidoc3.py'
(which tests asciidoc3.py). First some files are copied to
./tests/data/a2x3testdata
In a second step a2x3.py is executed in diverse approaches. See the
'command lines' presented as 'TEST_TUPEL'.
Be sure to have all needed programs installed: lynx, w3m, epubcheck,
dblatex, fop ...

Before you can use testa2x3.py you have to run
'python3 testasciidoc3.py --force update'
to produce the testfiles. Output is written to
'./tests/data/a2x3testdata/'

Usage: [python3 testasciidoc3.py --force update &&] python3 testa2x3.py [-v]

Known bugs:
If producing dvi/ps, the source must not contain images - this seems to
be a dblatex issue ... (?)

Copyright (C) 2020 by Berthold Gehrke <berthold.gehrke@gmail.com>
Free use of this software is granted under the terms of the
GNU General Public License Version 2 or higher (GNU GPLv2+).
"""

from argparse import ArgumentParser
from concurrent import futures
import os
import shutil
import subprocess


TEST_TUPEL = (
    # txt to pdf
    ['-f', 'pdf', './data/a2x3testdata/pdf_test.txt'],
    # txt to pdf using fop
    ['-f', 'pdf', '--fop', './data/a2x3testdata/fop_test.txt'],
    # txt to epub
    ['-f', 'epub', './data/a2x3testdata/epub_test.txt'],
    # txt to epub leave artifacts
    ['-f', 'epub', '-k', './data/a2x3testdata/epub_artifacts_test.txt'],
    # txt to epub epubcheck
#    ['-f', 'epub', '-k', '--epubcheck', \
#     './data/a2x3testdata/epubcheck_test.txt'],
    # txt to text (lynx)
    ['-f', 'text', '--lynx', './data/a2x3testdata/lynx_test.txt'],
    # txt to text (w3m)
    ['-f', 'text', './data/a2x3testdata/w3m_test.txt'],
    # txt to xhtml
    ['-f', 'xhtml', './data/a2x3testdata/test.txt'],
    # txt to manpage
    ['-f', 'manpage', '-d', 'manpage', './data/a2x3testdata/a2x3.1.txt'],
    # txt to docbook xml
    ['-f', 'docbook', './data/a2x3testdata/docbook_test.txt'],
    # xml (docbook) to pdf
    ['-f', 'pdf', './data/a2x3testdata/test-docbook45.xml'],
    # txt to chunked
    ['-f', 'chunked', './data/a2x3testdata/chunked_test.txt'],
    # xml (docbook) to dvi
    ['-f', 'dvi', './data/a2x3testdata/faq_dvi_test_45.xml'],
    # xml (docbook) to ps
    ['-f', 'ps', './data/a2x3testdata/faq_ps_test_51.xml'],
    # xml (docbook) to tex
    ['-f', 'tex', './data/a2x3testdata/tex_test_51.xml'],
    )


DESCRIPTION = '''Runs tests for AsciiDoc3 / a2x3.py.
                 Use option '-v' to see a2x3 working.'''
ARG_PARSER = ArgumentParser(usage='usage: python3 a2x3test.py [-v]',
                            description=DESCRIPTION)
ARG_PARSER.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='see more output')
ARGS = ARG_PARSER.parse_args()


def remove_testitems():
    """remove files from previous tests"""
    if os.path.exists('./data/a2x3testdata/'):
        shutil.rmtree('./data/a2x3testdata/')
        if ARGS.verbose:
            print("remove ./data/a2x3testdata/")


def copy_testfiles():
    """Copy files to ./data/a2x3testdata/"""
    os.mkdir('./data/a2x3testdata/')
    for file_item in ('test.txt',
                      'a2x3.1.txt',
                      ):
        if os.path.exists('../doc/'+file_item):
            shutil.copy2('../doc/'+file_item, './data/a2x3testdata/'+file_item)
            if ARGS.verbose:
                print("copy "+file_item)
    # We use copies of 'test.txt' to test text, pdf, fop, epub, epubcheck ...'
    if os.path.exists('./data/a2x3testdata/test.txt'):
        shutil.copy2('./data/a2x3testdata/test.txt',
                     './data/a2x3testdata/pdf_test.txt')
        shutil.copy2('./data/a2x3testdata/test.txt',
                     './data/a2x3testdata/fop_test.txt')
        shutil.copy2('./data/a2x3testdata/test.txt',
                     './data/a2x3testdata/lynx_test.txt')
        shutil.copy2('./data/a2x3testdata/test.txt',
                     './data/a2x3testdata/w3m_test.txt')
        shutil.copy2('./data/a2x3testdata/test.txt',
                     './data/a2x3testdata/fop_test.txt')
        shutil.copy2('./data/a2x3testdata/test.txt',
                     './data/a2x3testdata/epub_test.txt')
        shutil.copy2('./data/a2x3testdata/test.txt',
                     './data/a2x3testdata/epub_artifacts_test.txt')
#        shutil.copy2('./data/a2x3testdata/test.txt',
#                     './data/a2x3testdata/epubcheck_test.txt')
        shutil.copy2('./data/a2x3testdata/test.txt',
                     './data/a2x3testdata/docbook_test.txt')
        shutil.copy2('./data/a2x3testdata/test.txt',
                     './data/a2x3testdata/chunked_test.txt')
        shutil.copy2('./data/test-docbook45.xml',
                     './data/a2x3testdata/test-docbook45.xml')
        shutil.copy2('./data/faq-docbook45.xml',
                     './data/a2x3testdata/faq_dvi_test_45.xml')
        shutil.copy2('./data/faq-docbook51.xml',
                     './data/a2x3testdata/faq_ps_test_51.xml')
        shutil.copy2('./data/test-docbook51.xml',
                     './data/a2x3testdata/tex_test_51.xml')
        if ARGS.verbose:
            print("copy testfiles to ./data/a2x3testdata/")


def run_tests_a2x3(list_data):
    """Runs tests parallel"""
    arg_list = ['python3', '../a2x3.py']
    if ARGS.verbose:
        arg_list += ['-v']
    arg_list += list_data
    if ARGS.verbose:
        print(arg_list)
    subprocess_a2x3test = subprocess.run(arg_list)
    if subprocess_a2x3test.returncode:
        print("[WARN] Returncode != zero running", arg_list)


if __name__ == '__main__':
    remove_testitems()
    copy_testfiles()
    with futures.ProcessPoolExecutor(max_workers=4) as e:
        for test_item in TEST_TUPEL:
            e.submit(run_tests_a2x3, test_item)
