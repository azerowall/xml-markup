#!/usr/bin/env python3

import sys
import zipfile
import xml.etree.ElementTree as XMLTree

from xmlmarkupparser import literals, parse
from xmlwriter import SimpleXmlWriter

def main():
    word_file_path = sys.argv[1]
    with zipfile.ZipFile(word_file_path, 'r') as zip_file:
        #print('\n'.join(zip_file.namelist()))
        #doc = zip_file.read('word/document.xml')
        zip_file.extract('word/document.xml')

    tree = XMLTree.parse('word/document.xml')
    root = tree.getroot()

    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    style = 'xml-markup'
    #for lit in literals(root, ns, 'xml-markup'):
    #    print(lit)

    tokens = parse(root, ns, style)
    with open('out.xml', 'w') as f:
        writer = SimpleXmlWriter(f)
        for tok in tokens:
            writer.write(tok)



if __name__ == '__main__':
    main()