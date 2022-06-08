import simplePascalParser
import SimplePascalLexer as lexer
import ast
# import absmc

def run(filename):

    infile = filename + ".p"

    # ast.initialize_ast()
    # if simplePascalParser.from_file(infile):
    #     if (ast.typecheck()):
    #         # ast.print_ast()
    #         outfile = filename + ".ami"
    #         absmc.print_code(outfile, ast.classtable)

    # else:
    #     print
    #     "Failure: there were errors."

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run("SimplePascaltest1")

