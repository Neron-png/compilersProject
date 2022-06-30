import logging

import ply.yacc as yacc
import SimplePascalLexer
from SimplePascalLexer import tokens
from SimplePascalLexer import lex


error_f = False

start = 'program'

precedence = (
    ('nonassoc', 'EQU', 'RELOP', 'INOP'),
    ('left', 'ADDOP', 'OROP'),
    ('left', 'MULDIVANDOP'),
    ('right', 'NOTOP'),
    ('right', 'ELSE'),
    ('left', 'DOT', 'LBRACK', 'RBRACK', 'LPAREN', 'RPAREN'),

)



def p_empty(p):
    'empty :'

    p[0] = None

def p_program(p):
    """
    program : header declarations subprograms comp_statement DOT
    """

    p[0] = ("Program", p[1], p[2], p[3], p[4])


def p_header(p):
    """
    header : PROGRAM ID SEMI
    """
    p[0] = ("Header", p[1], p[2])


def p_declarations (p):
    """
    declarations : constdefs typedefs vardefs
    """
    p[0] = ("Declarations", p[1], p[2], p[3])


def p_constdefs(p):
    """
    constdefs : CONST constant_defs SEMI
              | empty
    """
    if len(p) == 2:
        return
    p[0] = ("Constdefs", p[1], p[2])


def p_constant_defs(p):
    """
    constant_defs : constant_defs SEMI ID EQU expression
                  |  ID EQU expression
    """
    if len(p) == 4:
        p[0] = ("Constant_defs", p[1], p[2], p[3])
        return
    p[0] = ("Constdefs", p[1], p[3], p[4], p[5])


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
    if len(p) == 4:
        if p[1] != "(":
            # Binop
            p[0] = (p[2], p[1], p[3])
        else:
            # ( EXPRESSION )
            p[0] = p[2]
    elif len(p) == 3:
        if p[1] == "-":
            p[0] == ("UMINUS", p[2])
        elif p[1] == "+":
            p[0] = p[2]
        else:
            # NOT
            p[0] = (p[1], p[2])
    elif len(p) == 5:
        # Function def | ['_try_me', '(', None, ')']
        p[0] = ("fundef", p[1], p[3])
    else:
        p[0] = p[1]


def p_variable (p):
    """
    variable    : ID
                | variable DOT ID
                | variable LBRACK expressions RBRACK
    """
    if len(p) == 2:
        p[0] = ("Variable", p[1])
    elif len(p) == 4:
        p[0] = ("Variable", p[1], p[2], p[3])
    else:
        p[0] = ("Variable", p[1], p[2], p[3], p[4])


def p_expressions (p):
    """
    expressions : expressions COMMA expression
                | expression
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    p[0] = (p[1], p[3])


def p_constant (p):
    """
    constant    : ICONST
                | RCONST
                | BCONST
                | CCONST
    """
    p[0] = p[1]


def p_setexpression (p):
    """
    setexpression    : LBRACK elexpressions RBRACK
                    | LBRACK RBRACK
    """
    if len(p) == 3:
        p[0] = (p[1], p[2])
        return
    p[0] = (p[1], p[2], p[3])


def p_elexpressions (p):
    """
    elexpressions   : elexpressions COMMA elexpression
                    | elexpression
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    p[0] = (p[1], p[2], p[3])


def p_elexpression (p):
    """
    elexpression    : expression DOTDOT expression
                    | expression
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    p[0] = (p[1], p[2], p[3])


def p_typedefs (p):
    """
    typedefs    : TYPE type_defs SEMI
                    | empty
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    p[0] = (p[1], p[2])


def p_type_defs (p):
    """
    type_defs    : type_defs SEMI ID EQU type_def
                | ID EQU type_def
    """
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
        return
    p[0] = (p[1], p[3], p[4], p[5])


def p_type_def (p):
    """
    type_def    : ARRAY LBRACK dims RBRACK OF typename
                | SET OF typename
                | RECORD fields END
                | LPAREN identifiers RPAREN
                | limit DOTDOT limit
    """
    if len(p) == 7:
        p[0] = (p[1], p[2], p[3], p[4], p[5], p[6])
        return
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])


def p_dims (p):
    """
    dims        : dims COMMA limits
                | limits
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])


def p_limits (p):
    """
    limits      : limit DOTDOT limit
                | ID
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])


def p_limit (p):
    """
    limit       : ADDOP ICONST
                | ADDOP ID
                | ICONST
                | CCONST
                | BCONST
                | ID
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 3:
        p[0] = (p[1], p[2])


def p_typename (p):
    """
    typename        : standard_type
                    | ID
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 3:
        p[0] = (p[1], p[2])


def p_standard_type (p):
    """
    standard_type   : INTEGER
                    | REAL
                    | BOOLEAN
                    | CHAR
    """
    if len(p) == 2:
        p[0] = p[1]


def p_fields (p):
    """
    fields   : fields SEMI field
             | field
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[3])


def p_field (p):
    """
    field   : identifiers COLON typename
    """
    p[0] = (p[1], p[2], p[3])


def p_identifiers (p):
    """
    identifiers     : identifiers COMMA ID
                    | ID
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])


def p_vardefs (p):
    """
    vardefs     : VAR variable_defs SEMI
                    | empty
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[2])


def p_variable_defs (p):
    """
    variable_defs     : variable_defs SEMI identifiers COLON typename
                    | identifiers COLON typename
    """
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
        return
    else:
        p[0] = (p[1], p[3], p[4], p[5])


def p_subprograms (p):
    """
    subprograms     : subprograms subprogram SEMI
                    | empty
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[2])


def p_subprogram (p):
    """
    subprogram     : sub_header SEMI FORWARD
                | sub_header SEMI declarations subprograms comp_statement
    """
    if len(p) == 4:
        p[0] = (p[1], p[3])
        return
    elif len(p) == 6:
        p[0] = (p[1], p[3], p[4], p[5])


def p_sub_header (p):
    """
    sub_header  : FUNCTION ID formal_parameters COLON standard_type
                | PROCEDURE ID formal_parameters
                | FUNCTION ID
    """
    if len(p) == 4:
        p[0] = ("procdef" , p[2], p[3])
        return
    elif len(p) == 6:
        p[0] = ("funcdef" , p[2], p[3], p[4], p[5])
    else:
        p[0] = ("funcdef", p[2])


def p_formal_parameters (p):
    """
    formal_parameters  : LPAREN parameter_list RPAREN
                | empty
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])


def p_parameter_list (p):
    """
    parameter_list  : parameter_list SEMI pass_p identifiers COLON typename
                | pass_p identifiers COLON typename
    """
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
        return
    elif len(p) == 7:
        p[0] = (p[1], p[3], p[4], p[6])


def p_pass_p (p):
    """
    pass_p      : VAR
                | empty
    """
    if len(p) == 2:
        p[0] = p[1]
        return


def p_comp_statement (p):
    """
    comp_statement      : BEGIN statements END
    """
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
        return


def p_statements (p):
    """
    statements      : statements SEMI statement
                    | statement
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[3])


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
    if len(p) == 1:
        return
    p[0] = p[1]


def p_assignment (p):
    """
    assignment      : variable ASSIGN expression
                    | variable ASSIGN STRING
    """
    p[0] = ("ASSIGN", p[1], p[3])


def p_if_statement (p):
    """
    if_statement      : IF expression THEN statement if_tail
    """
    p[0] = ("IF", p[2], p[4], p[5])


def p_if_tail (p):
    """
    if_tail         : ELSE statement
                    | %prec ELSE
    """
    if len(p) == 3:
        p[0] = (p[2])


def p_while_statement (p):
    """
    while_statement         : WHILE expression DO statement
    """
    p[0] = ("WHILE", p[2], p[4])


def p_for_statement (p):
    """
    for_statement         : FOR ID ASSIGN iter_space DO statement
    """
    p[0] = ("FOR", p[2], p[4], p[6])


def p_iter_space (p):
    """
    iter_space          : expression TO expression
                        | expression DOWNTO expression
    """
    p[0] = (p[2], p[1], p[3])


def p_with_statement (p):
    """
    with_statement      : WITH variable DO statement
    """
    p[0] = (p[1], p[2], p[3], p[4])


def p_subprogram_call (p):
    """
    subprogram_call     : ID
                        | ID LPAREN expressions RPAREN
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 5:
        p[0] = (p[1], p[2], p[3], p[4])


def p_io_statement (p):
    """
    io_statement        : READ LPAREN read_list RPAREN
                        | WRITE LPAREN write_list RPAREN
    """
    p[0] = (p[1], p[2], p[3], p[4])


def p_read_list (p):
    """
    read_list           : read_list COMMA read_item
                        | read_item
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])


def p_read_item (p):
    """
    read_item           : variable
    """
    p[0] = ("READ", p[1])


def p_write_list (p):
    """
    write_list          : write_list COMMA write_item
                        | write_item
    """
    if len(p) == 2:
        p[0] = p[1]
        return
    elif len(p) == 4:
        p[0] = (p[1], p[2], p[3])


def p_write_item (p):
    """
    write_item          : expression
                        | string
    """
    p[0] = ("WRITE", p[1])

def p_string (p):
    """
    string :     STRING
    """
    p[0] = ("STRING", p[1])

#########################################################################

def p_error(p):
    if p is None:
        print("Unexpected end-of-file")
    else:
        print("Unexpected token '{}' at line {}".format(p.value, p.lineno))
        print(f"lexpos: {p.lexpos}, type: {p.type}")
    error_f = True

parser = yacc.yacc()




if __name__ == "__main__" :
    f = open("SimplePascaltest1.p", "r")

    result = parser.parse(f.read(), lexer=SimplePascalLexer.lexer)

    print(result)

    if parser.errorok :
        print("Parsing succeeded")
    else:
        print("Parsing failed")
