import logging

import ply.yacc as yacc
import SimplePascalLexer
from SimplePascalLexer import tokens
from SimplePascalLexer import lex

error_f = False

start = 'program'

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OROP'),
    ('nonassoc', 'EQU', 'RELOP'),
    # ('nonassoc', 'RELOP'),
    ('left', 'ADDOP'),
    ('left', 'MULDIVANDOP'),
    ('right', 'NOTOP'),
    ('right', 'ELSE'),
    ('right', 'RPAREN'),
)



def p_empty(p):
    'empty :'
    pass

def p_program(p):
    """
    program : header declarations subprograms comp_statement DOT
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
    type_defs    : type_defs SEMI ID EQU type_def
                | ID EQU type_def
    """
    pass


def p_type_def (p):
    """
    type_def    : ARRAY LBRACK dims RBRACK OF typename
                | SET OF typename
                | RECORD fields END
                | LPAREN identifiers RPAREN
                | limit DOTDOT limit
    """
    pass


def p_dims (p):
    """
    dims        : dims COMMA limits
                | limits
    """
    pass


def p_limits (p):
    """
    limits      : limit DOTDOT limit
                | ID
    """
    pass


def p_limit (p):
    """
    limit       : ADDOP ICONST
                | ADDOP ID
                | ICONST
                | CCONST
                | BCONST
                | ID
    """
    pass


def p_typename (p):
    """
    typename        : standard_type
                    | ID
    """
    pass


def p_standard_type (p):
    """
    standard_type   : INTEGER
                    | REAL
                    | BOOLEAN
                    | CHAR
    """
    pass


def p_fields (p):
    """
    fields   : fields SEMI field
             | field
    """
    pass


def p_field (p):
    """
    field   : identifiers COLON typename
    """
    pass


def p_identifiers (p):
    """
    identifiers     : identifiers COMMA ID
                    | ID
    """
    pass


def p_vardefs (p):
    """
    vardefs     : VAR variable_defs SEMI
                    | empty
    """
    pass


def p_variable_defs (p):
    """
    variable_defs     : variable_defs SEMI identifiers COLON typename
                    | identifiers COLON typename
    """
    pass


def p_subprograms (p):
    """
    subprograms     : subprograms subprogram SEMI
                    | empty
    """
    pass


def p_subprogram (p):
    """
    subprogram     : sub_header SEMI FORWARD
                | sub_header SEMI declarations subprograms comp_statement
    """
    pass


def p_sub_header (p):
    """
    sub_header  : FUNCTION ID formal_parameters COLON standard_type
                | PROCEDURE ID formal_parameters
                | FUNCTION ID
    """
    pass


def p_formal_parameters (p):
    """
    formal_parameters  : LPAREN parameter_list RPAREN
                | empty
    """
    pass


def p_parameter_list (p):
    """
    parameter_list  : parameter_list SEMI pass_p identifiers COLON typename
                | pass_p identifiers COLON typename
    """
    pass


def p_pass_p (p):
    """
    pass_p      : VAR
                | empty
    """
    pass


def p_comp_statement (p):
    """
    comp_statement      : BEGIN statements END
    """
    pass


def p_statements (p):
    """
    statements      : statements SEMI statement
                    | statement
    """
    pass


def p_statement (p):
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


def p_assignment (p):
    """
    assignment      : variable ASSIGN expression
                    | variable ASSIGN STRING
    """
    pass


def p_if_statement (p):
    """
    if_statement      : IF expression THEN statement if_tail
    """
    pass


def p_if_tail (p):
    """
    if_tail         : ELSE statement
                    | empty
    """
    pass


def p_while_statement (p):
    """
    while_statement         : WHILE expression DO statement
    """
    pass


def p_for_statement (p):
    """
    for_statement         : FOR ID ASSIGN iter_space DO statement
    """
    pass


def p_iter_space (p):
    """
    iter_space          : expression TO expression
                        | expression DOWNTO expression
    """
    pass


def p_with_statement (p):
    """
    with_statement      : WITH variable DO statement
    """
    pass


def p_subprogram_call (p):
    """
    subprogram_call     : ID
                        | ID LPAREN expressions RPAREN
    """
    pass


def p_io_statement (p):
    """
    io_statement        : READ LPAREN read_list RPAREN
                        | WRITE LPAREN write_list RPAREN
    """
    pass


def p_read_list (p):
    """
    read_list           : read_list COMMA read_item
                        | read_item
    """
    pass


def p_read_item (p):
    """
    read_item           : variable
    """
    pass


def p_write_list (p):
    """
    write_list          : write_list COMMA write_item
                        | write_item
    """
    pass


def p_write_item (p):
    """
    write_item          : expression
                        | STRING
    """
    pass

#########################################################################

def p_error(p):
    if p is None:
        signal_error("Unexpected end-of-file", 'end')
    else:
        signal_error("Unexpected token '{0}'".format(p.value), p.lineno)

parser = yacc.yacc()

def signal_error(string, lineno):
    print("{1}: {0}".format(string, lineno))
    error_f = True


def from_file(filename):
    try:
        with open(filename, "rU") as f:
            parser.parse(f.read(), lexer=lex.lex(module=SimplePascalLexer), debug=None)
        return not error_f
    except IOError as e:
        print("I/O error: %s: %s" % (filename, e.strerror))


if __name__ == "__main__" :
    f = open("SimplePascaltest1.p", "r")
    logging.basicConfig(
            level=logging.CRITICAL,
    )
    log = logging.getLogger()
    res = parser.parse(f.read(), lexer=SimplePascalLexer.lexer, debug=log)

    if parser.errorok :
        print("Parsing succeeded")
    else:
        print("Parsing failed")
