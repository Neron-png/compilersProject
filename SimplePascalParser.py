import ply.yacc as yacc
import SimplePascalLexer
from SimplePascalLexer import tokens
from SimplePascalLexer import lex


def p_empty(p):
    'empty :'
    pass

def p_program(p):
    """
    program : header declarations subprograms comp statement DOT
    """
    pass


def p_header(p):
    """
    header : PROGRAM ID SEMI
    """
    pass


def p_declarations (p):
    """
    declarations : constdefs typedefs vardefs
    """
    pass


def p_constdefs(p):
    """
    constdefs : CONST constant_defs SEMI
              | empty
    """
    pass


def p_constant_defs(p):
    """
    constant_defs : constant_defs SEMI ID EQU expression
                  |  ID EQU expression
    """
    pass


def p_expression(p):
    """
    expression  : expression RELOP expression
                | expression EQU expression
                | expression INOP expression
                | expression OROP expression
                | expression ADDOP expression
                | expression MULDIVANDOP expression
                | ADDOP expression
                | NOTOP expression
                | variable
                | ID LPAREN expressions RPAREN
                | constant
                | LPAREN expression RPAREN
                | setexpression
    """
    pass


def p_variable (p):
    """
    variable    : ID
                | variable DOT ID
                | variable LBRACK expressions RBRACK
    """
    pass


def p_expressions (p):
    """
    expressions : expressions COMMA expression
                | expression
    """
    pass


def p_constant (p):
    """
    constant    : ICONST
                | RCONST
                | BCONST
                | CCONST
    """
    pass


def p_setexpression (p):
    """
    setexpression    : LBRACK elexpressions RBRACK
                    | LBRACK RBRACK
    """
    pass


def p_elexpressions (p):
    """
    elexpressions   : elexpressions COMMA elexpression
                    | elexpression
    """
    pass


def p_elexpression (p):
    """
    elexpression    : expression DOTDOT expression
                    | expression
    """
    pass


def p_typedefs (p):
    """
    typedefs    : TYPE type_defs SEMI
                    | empty
    """
    pass


def p_type_defs (p):
    """
    type_defs    : type_defs SEMI ID EQU type def
                | ID EQU type_def
    """
    pass


def type_def (p):
    """
    type_def    : ARRAY LBRACK dims RBRACK OF typename
                | SET OF typename
                | RECORD fields END
                | LPAREN identifiers RPAREN
                | limit DOTDOT limit
    """
    pass


def dims (p):
    """
    dims        : dims COMMA limits
                | limits
    """
    pass


def limits (p):
    """
    limits      : limit DOTDOT limit
                | ID
    """
    pass


def limit (p):
    """
    limit       : ADDOP ICONST
                | ADDOP ID
                | ICONST
                | CCONST
                | BCONST
                | ID
    """
    pass


def typename (p):
    """
    typename        : standard_type
                    | ID
    """
    pass


def standard_type (p):
    """
    standard_type   : INTEGER
                    | REAL
                    | BOOLEAN
                    | CHAR
    """
    pass


def fields (p):
    """
    fields   : fields SEMI field
             | field
    """
    pass


def field (p):
    """
    field   : identifiers COLON typename
    """
    pass


def identifiers (p):
    """
    identifiers     : identifiers COMMA ID
                    | ID
    """
    pass


def vardefs (p):
    """
    vardefs     : VAR variable_defs SEMI
                    | empty
    """
    pass


def variable_defs (p):
    """
    variable_defs     : variable_defsSEMI identifiers COLON typename
                    | identifiers COLON typename
    """
    pass


def subprograms (p):
    """
    subprograms     : subprograms subprogram SEMI
                    | empty
    """
    pass


def subprogram (p):
    """
    subprogram     : sub_header SEMI FORWARD
                | sub_header SEMI declarations subprograms comp_statement
    """
    pass


def sub_header (p):
    """
    sub_header  : FUNCTION ID formal_parameters COLON standard_type
                | PROCEDURE ID formal_parameters
                | FUNCTION ID
    """
    pass


def formal_parameters (p):
    """
    formal_parameters  : LPAREN parameter list RPAREN
                | empty
    """
    pass


def parameter_list (p):
    """
    parameter_list  : parameter_list SEMI pass_p identifiers COLON typename
                | pass_p identifiers COLON typename
    """
    pass


def pass_p (p):
    """
    pass_p      : VAR
                | empty
    """
    pass


def comp_statement (p):
    """
    comp_statement      : BEGIN statements END
    """
    pass


def statements (p):
    """
    statements      : statements SEMI statement
                    | statement
    """
    pass


def statement (p):
    """
    statement       : assignment
                    | if_statement
                    | while_statement
                    | for_statement
                    | with_statement
                    | subprogram_call
                    | io_statement
                    | comp_statement
                    | empty
    """
    pass


def assignment (p):
    """
    assignment      : variable ASSIGN expression
                    | variable ASSIGN STRING
    """
    pass


def if_statement (p):
    """
    if_statement      : IF expression THEN statement if_tail
    """
    pass


def if_tail (p):
    """
    if_tail         : ELSE statement
                    | empty
    """
    pass


def while_statement (p):
    """
    while_statement         : WHILE expression DO statement
    """
    pass


def for_statement (p):
    """
    for_statement         : FOR ID ASSIGN iter_space DO statement
    """
    pass


def iter_space (p):
    """
    iter_space          : expression TO expression
                        | expression DOWNTO expression
    """
    pass


def with_statement (p):
    """
    with_statement      : WITH variable DO statement
    """
    pass


def subprogram_call (p):
    """
    subprogram_call     : ID
                        | ID LPAREN expressions RPAREN
    """
    pass


def io_statement (p):
    """
    io_statement        : READ LPAREN read list RPAREN
                        | WRITE LPAREN write_list RPAREN
    """
    pass


def read_list (p):
    """
    read_list           : read_list COMMA read_item
                        | read_item
    """
    pass


def read_item (p):
    """
    read_item           : variable
    """
    pass


def write_list (p):
    """
    write_list          : write_list COMMA write_item
                        | write_item
    """
    pass


def write_item (p):
    """
    write_item          : expression
                        | STRING
    """
    pass


