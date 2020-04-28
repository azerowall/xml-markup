from xmlmarkupparser import Token


class SimpleXmlWriter:
    def __init__(self, writer):
        self._writer = writer
        self._stack = []
        self._data = None
        
    def write(self, tok):
        ttok = type(tok)
        if ttok is Token.StartTag:
            self._data = None
            self._writer.write(f'<{tok.name}>')
            self._stack.append(tok.name)
        elif ttok is Token.EndTag:
            if self._data is not None:
                self._writer.write(self._data)
                self._data = None
            name = self._stack.pop()
            self._writer.write(f'</{name}>')
        elif ttok is Token.Data:
            self._data = tok.data
        
    def close(self):
        self._writer.close()
        
        
        
        
if __name__ == '__main__':
    toks = [
        Token.Data('blablabla'),
        Token.StartTag('title'),
        Token.Data('something interesting'),
        Token.EndTag(),
        Token.Data('another blabla'),
    ]

    with open('out.xml', 'w') as f:
        writer = SimpleXmlWriter(f)
        for tok in toks:
            writer.write(tok)