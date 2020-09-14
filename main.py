#!/usr/bin/env python3

import sys
import argparse
#import tempfile
import zipfile
import xml.etree.ElementTree as XMLTree

from xmlmarkupparser import literals, parse
from xmlwriter import SimpleXmlWriter

def make_argparser():
    parser = argparse.ArgumentParser(description="Extract xml-markup from docx into xml")
    parser.add_argument('input', help='input path for docx file')
    parser.add_argument('--output', help='output path for xml file', default='out.xml')
    parser.add_argument('--style', help='style name of xml-markup in docx', default='xml-markup')
    return parser


def main():
    parser = make_argparser()
    args = parser.parse_args(sys.argv[1:])

    #tmpfile = tempfile.mkstemp()
    with zipfile.ZipFile(args.input, 'r') as zip_file:
        document_str = zip_file.read('word/document.xml')
        #zip_file.extract('word/document.xml')

    #tree = XMLTree.parse('word/document.xml')
    #root = tree.getroot()
    root = XMLTree.fromstring(document_str)

    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    tokens = parse(root, ns, args.style)
    with open(args.output, 'w') as f:
        writer = SimpleXmlWriter(f)
        for tok in tokens:
            writer.write(tok)



if __name__ == '__main__':
    main()