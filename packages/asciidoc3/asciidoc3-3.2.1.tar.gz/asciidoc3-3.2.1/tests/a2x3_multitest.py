#!/usr/bin/env python3

"""
Runs a bunch of a2x3.py testcases over alle txt-files in directory
./tests/data/
to produce PDFs via, first, dblatex and, secons, via Apache FOP. 

Usage: python3 a2x3_multitest.py

You'll see some errors because of not all documents are
valid DocBook. That's not a bug (nonvalid_docbook51.xml, newtables_docbook51
at al.), it's the expected behavior.

Copyright (C) 2020 by Berthold Gehrke <berthold.gehrke@gmail.com>
Free use of this software is granted under the terms of the
GNU General Public License Version 2 or higher (GNU GPLv2+).
"""

from concurrent import futures
import os
import subprocess
from shutil import copy


def a2x3_multi(testfile):
    '''
    TODO
    '''
    if testfile.endswith('_fop.txt'):
        subprocess.run(["python3", "../a2x3.py", "-f", "pdf", "--fop", path_to_data + testfile])
    else:
        subprocess.run(["python3", "../a2x3.py", "-f", "pdf", path_to_data + testfile])


def data_files():
    '''
    TODO
    '''
    testfiles = list()
    with os.scandir(path_to_data) as testpath:
        for entry in testpath:
            if entry.name.endswith('.txt'):
                testfiles.append(entry.name)
                filename_short = entry.name[:-4]
                copy('data/' + entry.name,
                     'data/' + filename_short + '_fop.txt')
                testfiles.append(filename_short + '_fop.txt')
    return tuple(testfiles)


def del_files():
    '''
    Remove files to have an "empty workspace"
    '''
    artifacts_to_remove = (
        'latex1.md5',
        'latex1.png',
        'latex-filter__1.md5',
        'latex-filter__1.png',
        'latex-filter__2.md5',
        'latex-filter__2.png',
        'latex-filter__3.md5',
        'latex-filter__3.png',
        'music1.md5',
        'music1.png',
        'music2.md5',
        'music2.png',
        'open-block-test__1.md5',
        'open-block-test_fop__1.md5',
        'open-block-test__1.png',
        'open-block-test__3.md5',
        'open-block-test_fop__3.md5',
        'open-block-test__3.png',
        'open-block-test_fop__1.png',
        'open-block-test_fop__2.png',
        'open-block-test_fop__3.png',
        'slidy-example__1.md5',
        'slidy-example__1.png',
        'graphviz1.png',
        'graphviz2.png',
        'open-block-test__1.png',
        'open-block-test__2.png',
        'open-block-test__3.png',
        'slidy-example__1.png',)
    for item in artifacts_to_remove:
        if os.path.exists("../images/" + item):
            os.remove("../images/" + item)
    with os.scandir(path_to_data) as testpath:
        for entry in testpath:
            if entry.name.endswith('_fop.txt'):
                os.remove(path_to_data + '/' + entry.name)
            elif entry.name.endswith('.pdf'):
                os.remove(path_to_data + '/' + entry.name)
            elif entry.name.endswith('.xml') and \
                 not entry.name.endswith('test-docbook45.xml') and \
                 not entry.name.endswith('test-docbook51.xml'):
                os.remove(path_to_data + '/' + entry.name)
            else:
                pass

def main(item):
    '''
    TODO
    '''
    print(item)
    a2x3_multi(item)


if __name__ == "__main__":
    '''do not run as an imported module or using an IDE like IDLE'''
    full_path = os.path.abspath(os.path.dirname(__file__))
    path_to_data = full_path + "/data/"
    del_files()
    # to remove only the 'test artifacts',
    # comment out the next three lines
    TUPLE_TEST = data_files()
    with futures.ProcessPoolExecutor(max_workers=4) as e:
        for item in TUPLE_TEST:
            e.submit(main, item)
