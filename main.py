import sys
import zipfile
import xml.etree.ElementTree as XMLTree

from xmlmarkupparser import microsoft_word_xml_document_parse
from xmlwriter import SimpleXmlWriter

def main():
    word_file_path = sys.argv[1]
    with zipfile.ZipFile(word_file_path, 'r') as zip_file:
        zip_file.extract('word/document.xml')

    tree = XMLTree.parse('word/document.xml')
    root = tree.getroot()

    tokens = microsoft_word_xml_document_parse(root)
    with open('out.xml', 'w') as f:
        writer = SimpleXmlWriter(f)
        for tok in tokens:
            writer.write(tok)



if __name__ == '__main__':
    main()