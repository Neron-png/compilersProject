from ply.lex import lex

# All tokens must be named in advance.
tokens = ('PROGRAM', 'CONST', 'TYPE', 'ARRAY', 'SET', 'OF', 'RECORD', 'VAR', 'FORWARD', 'FUNCTION', 'PROCEDURE',
          'INTEGER', 'REAL', 'BOOLEAN', 'CHAR', 'BEGIN', 'END', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'FOR',
          'DOWNTO', 'TO', 'WITH', 'READ', 'WRITE', 'OROP', 'NOTOP', 'INOP', 'ICONST', 'RCONST', 'BCONST', 'CCONST',
          'RELOP', 'ADDOP', 'MULDIVANDOP', 'LPAREN', 'RPAREN', 'SEMI', 'DOT', 'COMMA', 'COLON', 'ASSIGN', 'EQU',
          'LBRACK',
          'RBRACK', 'EOF', 'COMMENT', 'NAME', 'STRING',)

# Ignored characters
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_STRING(t):
    r'"(.(\\\n)?)*"'
    t.value = t.value[1:-1]
    t.lexer.lineno += t.value.count("\n")
    return t


def t_COMMENT(t):
    r'{([^}]|\n)*}'
    t.lexer.lineno += t.value.count("\n")
    return t


# Words
t_PROGRAM = r'program'
t_CONST = r'const'
t_TYPE = r'type'
t_ARRAY = r'array'
t_SET = r'set'
t_OF = r'of'
t_RECORD = r'record'
t_VAR = r'var'
t_FORWARD = r'forward'
t_FUNCTION = r'function'
t_PROCEDURE = r'procedure'
t_INTEGER = r'integer'
t_REAL = r'real'
t_BOOLEAN = r'boolean'
t_CHAR = r'char'
t_BEGIN = r'begin'
t_END = r'end'
t_IF = r'if'
t_THEN = r'then'
t_ELSE = r'else'
t_DO = r'do'
t_WHILE = r'while'
t_FOR = r'for'
t_DOWNTO = r'downto'
t_TO = r'to'
t_WITH = r'with'
t_READ = r'read'
t_WRITE = r'write'
t_OROP = r'or'
t_NOTOP = r'not'
t_INOP = r'in'


t_NAME = r'_?[a-zA-Z]([a-zA-Z0-9_]*[a-zA-Z0-9])?'

# OPERATOS
t_MULDIVANDOP = r'(\*)|/|(DIV)|(MOD)|(AND)'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_DOT = r'\.'
t_COMMA = r','
t_ASSIGN = r':='
t_COLON = r':'
t_EQU = r'='
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_EOF = r'<EOF>'


def t_ADDOP(t):
    r'\+|-'


def t_RELOP(t):
    r'<|>|(<=)|(>=)|(<>)'
    return t


def t_BCONST(t):
    r'(TRUE)|(FALSE)'
    t.value = t.value == "TRUE"
    return t





def t_ICONST_bin(t):
    r'0B(1(0|1)*)'
    t.value = int(t.value[2:], 2)
    t.type = "ICONST"
    return t


def t_ICONST_hex(t):
    r'0H([A-F1-9][A-F0-9]*)'
    t.value = int(t.value[2:], 16)
    t.type = "ICONST"
    return t


def t_ICONST_decim(t):
    r'[1-9][0-9]*'
    t.value = int(t.value)
    t.type = "ICONST"
    return t


def t_ICONST_zero(t):
    r'0'
    t.value = 0
    t.type = "ICONST"
    return t


def t_RCONST_bin(t):
    r'0B(0|(1(1|0)*))?\.(0|((0|1)*1))'
    a = int(t.value.split(".")[0][2:], 2)
    b = int(t.value.split(".")[1], 2)
    t.value = a + b / 10 ** len(str(b))
    t.type = "RCONST"
    return t


def t_RCONST_hex(t):
    r'0H(([A-F1-9][A-F0-9]*)|0)?\.(0|([A-F0-9]*[A-F1-9]))'
    a = int(t.value.split(".")[0][2:], 16)
    b = int(t.value.split(".")[1], 16)
    t.value = a + b / 10 ** len(str(b))
    t.type = "RCONST"
    return t


def t_RCONST_exp(t):
    r'([1-9][0-9]*)E-?([1-9][0-9]*)'
    a = int(t.value.split("E")[0])
    b = int(t.value.split("E")[1])
    t.value = a * 10 ** b
    t.type = "RCONST"
    return t


def t_RCONST_reg(t):
    r'(([1-9][0-9]*)|0)?\.(([0-9]*[1-9])|0)'
    t.value = float(t.value)
    t.type = "RCONST"
    return t


def t_CCONST(t):
    r"'.|(\\[bvrntf])'"
    t.value = t.value[1:-1]
    return t


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    print(lexer.lineno)
    # t.lexer.skip(1)


lexer = lex()
with open("SimplePascaltest1.p", "r+") as f:
    lexer.input(f.read())
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(tok)
