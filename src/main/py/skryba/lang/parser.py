import lang.tokenizer as tokenizer

tokens = tokenizer.tokens

precedence = (
    ('left', 'LAMBDA','RARROW'),
    ('left', 'COMMA'),   
)

def p_program_1(p):
    'program : statement'
    pass
def p_program_2(p):
    'program : statement program'
    pass

def p_statement_bind(p):
    'statement : BIND IDENTIFIER EQUALS expression'
    pass

def p_statement_expr(p):
    'statement : expression'
    pass

def p_expression_lambda(p):
    'expression : LAMBDA IDENTIFIER RARROW expression'
    pass

def p_expression_list_1(p):
    'expression_list : expression'
    pass
def p_expression_list_2(p):
    'expression_list : expression expression_list'
    pass
def p_expression_application(p):
    'expression : expression expression_list'
    pass

def p_tuple_list_1(p):
    'tuple_list : expression'
    pass
def p_tuple_list_2(p):
    'tuple_list : expression COMMA tuple_list'
    pass
def p_expression_tuple(p):
    'expression : LPAREN expression COMMA tuple_list RPAREN'
    pass

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    pass

def p_expression_string_literal(p):
    'expression : STRING_LITERAL'
    pass

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    pass

def p_error(p):
    print("Syntax error at '%s'" % p.value)

# Build the parser
# TODO disable debug
import ply.yacc
ply.yacc.yacc(debug=True)

def parse(s):
    return ply.yacc.parse(s)
