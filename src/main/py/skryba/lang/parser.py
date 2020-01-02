import lang.tokenizer as tokenizer

tokens = tokenizer.tokens

precedence = (
    ('left', 'LAMBDA','RARROW'),
    ('left', 'COMMA'),   
)

def p_program(p):
    '''program : statement
               | statement program
    '''
    pass

def p_statement(p):
    '''statement : BIND IDENTIFIER EQUALS expression SEMICOLON
                 | function_call SEMICOLON
    '''
    pass

def p_expression(p):
    '''expression : LAMBDA IDENTIFIER RARROW expression
                  | function_call
                  | expression_atomic
    '''
    pass

def p_function_call(p):
    '''function_call : maybe_func expression_atomic_list
    '''
    pass

def p_maybe_func(p):
    '''maybe_func : IDENTIFIER
                  | LPAREN expression RPAREN
    '''
    pass

def p_expression_atomic(p):
    '''expression_atomic : STRING_LITERAL
                         | LPAREN expression COMMA tuple_list RPAREN
                         | maybe_func
    '''
    pass

def p_expression_atomic_list(p):
    '''expression_atomic_list : expression_atomic
                              | expression_atomic expression_atomic_list
    '''
    pass

def p_tuple_list(p):
    '''tuple_list : expression
                  | expression COMMA tuple_list
    '''
    pass

def p_error(p):
    print("Syntax error at '%s'" % p.value)

# Build the parser
# TODO disable debug
import ply.yacc
ply.yacc.yacc(debug=True)

def parse(s):
    return ply.yacc.parse(s)
