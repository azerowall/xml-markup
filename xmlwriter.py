from xmlmarkupparser import Token


class SimpleXmlWriter:
    def __init__(self, writer):
        self._writer = writer
        self._stack = []
        self._data = None
        self._is_first_write = True
        
    def write(self, tok):
        if self._is_first_write:
            self._writer.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            self._is_first_write = False

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
