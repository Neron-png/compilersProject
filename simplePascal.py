import SimplePascalParser
import SimplePascalLexer
import sys


def printTree(ast, depth=0):
    if depth == 0:
        print("root")
    for node in ast:
        if not isinstance(node, tuple):
            print("│"*(depth-1) + "└" + str(node))
        else:
            printTree(node, depth+1)

def makeSymbolTable(ast, parent=None, depth = 0, path=None):
    if path is None:
        path = []
    for i, node in enumerate(ast):

        if ast[i] in ("Constant_defs", "type", "var"):
            path += (parent, (ast[i:]))
        elif ast[i] in ("procdef", "funcdef"):
            path = (parent, (ast[i+1], (ast[i:])))
        elif isinstance(node, tuple):
            makeSymbolTable(node, parent, depth + 1, path)
        else :
            continue

    return path

a = (None, (
    ('procdef', 'all', ('(', (None, ';', 'var', 'x', ':', 'real'), ')')),
    ';',
    ('Declarations', None, None, None),
    (None,
     (
         ('funcdef', '_try_me', ('(', None, ')')
          )
     )
     )
)
 )

def run(filename):

    try:
        f = open(filename, 'r+')
        result = SimplePascalParser.parser.parse(f.read(), lexer=SimplePascalLexer.lexer)

        if result:
            printTree(result)
            print("↑ Formatted AST ↑")
            print("↓    Raw AST    ↓")
            print(result)
            print("↓  SymbolTable  ↓")
            print(makeSymbolTable(result))

        else:
            print("Failed!")
    except Exception as e:
        print("Invalid filename!")
        print(e)

if __name__ == '__main__':

    run(sys.argv[1] if len(sys.argv) > 1 else "SimplePascaltest1.p")

