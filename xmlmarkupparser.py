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

def parse_markup_tag(tag):
    if tag[:2] == '{{' and tag[-1] == '|':
        return Token.StartTag(tag[2:-1])
    elif tag == '}}':
        return Token.EndTag()
    else:
        return None

def make_token(is_tag, text):
    if is_tag:
        token = parse_markup_tag(text)
        if token is None:
            raise XmlMarkupError
        return token
    else:
        return Token.Data(text)

def literals(root, ns, style):
    paragraphs = root.iterfind('.//w:p', ns)
    for paragraph in paragraphs:
        runs = paragraph.iterfind('w:r', ns)
        for run in runs:
            has_style = is_run_has_style(run, style, ns)
            texts = run.iterfind('w:t', ns)
            for text in texts:
                yield has_style, text.text
        yield False, '\n'

def parse(root, ns, style):
    is_tag_prev = None
    data = []
    for is_tag, text in literals(root, ns, style):
        if is_tag_prev is not None and is_tag_prev != is_tag:
            d = ''.join(data)
            data.clear()
            yield make_token(is_tag_prev, d)
        data.append(text)
        is_tag_prev = is_tag
        
    if data:
        yield make_token(is_tag_prev, ''.join(data))
