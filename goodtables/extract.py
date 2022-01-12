#import ijson.backends.python as ijson
import ijson

class _Numberer(object):
    def __init__(self, f):
        self.lineno = 0
        self.f = f

    def read(self, n):
        # ijson does a read(0) to get the data type
        if not n:
            return self.f.read(0)
        # return one line regardless of the size requested
        # so we can generate line numbers for the pot file
        self.lineno += 1
        rval = next(self.f)
        return rval


def extract_errors(fileobj, *args, **kwargs):
    n = _Numberer(fileobj)
    parser = ijson.parse(n)
    for prefix, event, value in parser:
        if event != 'string' or not prefix.startswith('errors.'):
            continue
        if prefix.endswith('.message') or prefix.endswith('.description') or prefix.endswith('.name'):
            yield (n.lineno, '', value, [prefix])
