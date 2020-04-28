import re

class Token:
    class StartTag:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f'StartTag({self.name})'
        
        
    class EndTag:
        def __repr__(self):
            return 'EndTag'
        

    class Data:
        def __init__(self, data):
            self.data = data

        def __repr__(self):
            return f'Data({self.data})'
    

class XmlMarkupError(Exception):
    pass

    
def is_run_has_style(run, style, ns):
    props = run.find('w:rPr', ns)
    if props is None:
        return False

    style_prop = props.find('w:rStyle', ns)
    if style_prop is None:
        return False

    value = style_prop.attrib[f'{{{ns["w"]}}}val']
    if value and value == style:
        return True
    return False

def parse_markup_tags(tags_str):
    for tag in re.findall(r'{{[^|]+\||}}', tags_str):
        if tag[:2] == '{{' and tag[-1] == '|':
            yield Token.StartTag(tag[2:-1])
        elif tag == '}}':
            yield Token.EndTag()
        else:
            raise XmlMarkupError

def microsoft_word_xml_document_parse(root):
    ns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    xml_markup_tag = str()
    data = []
    for paragraph in root.iterfind('.//w:p', ns):
        for run in paragraph.iterfind('w:r', ns):
            text = run.find('w:t', ns)
            if text is None:
                continue
            if is_run_has_style(run, 'xml-markup', ns): # hack
                if len(data) > 0:
                    yield Token.Data(''.join(data))
                    data.clear()
                #print(f'markup text: "{text.text}"')
                xml_markup_tag += text.text
            else:
                if xml_markup_tag:
                    tokens = parse_markup_tags(xml_markup_tag)
                    for tok in tokens:
                        yield tok
                    xml_markup_tag = str()
                data.append(text.text)
        #data.append('\n')
    
    #if xml_markup_tag:
    #    yield Token.Data(''.join(data))
    if len(data) > 0:
        yield Token.Data(''.join(data))

    #print(''.join(data))