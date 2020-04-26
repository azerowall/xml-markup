from dataclasses import dataclass


class Token:
    @dataclass
    class StartTag:
        name: str
        
    @dataclass
    class EndTag:
        pass
        
    @dataclass
    class Data:
        data: str
    
    
class XmlMarkupParser:
    def next(self):
        raise NotImplementedError
        
        
class TextTokenizer(XmlMarkupParser):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        
    def next(self):
        text = self.text
        i = self.pos
        tok = None
        
        
        if text[i] == '{' and text[i + 1] == '{':
            i += 2
            ibar = text.index('|', i)
            value = text[i:ibar]
            i = ibar + 1
            tok = Token.StartTag(value)
        elif text[i] == '}' and text[i + 1] == '}':
            i += 2
            tok = Token.EndTag()
        else:
            inext1, inext2 = None, None
            try:
                inext1 = text.index('{{', i)
            except ValueError:
                pass
            try:
                inext2 = text.index('}}', i)
            except ValueError:
                pass
            
            if inext1 is None and inext2 is None:
                return None
            
            if inext1 is None:
                inext = inext2
            elif inext2 is None:
                inext = inext1
            else:
                inext = min(inext1, inext2)
                
            value = text[i:inext]
            i = inext
            tok = Token.Data(value)
            
        self.pos = i
        return tok
            
        
      

if __name__ == '__main__':      
    with open('test.txt', 'r', encoding='utf8') as f:
        text = f.read()
        
    tokenizer = TextTokenizer(text)

    while True:
        tok = tokenizer.next()
        print(tok)
        if tok is None:
            break