from lang.ast import Bind, FunCallExpr, FunCallStmt, Identifier, Lambda, Program, StringLiteral, Tuple
import lang.tokenizer as tokenizer
from utils.log import warning, debug

tokens = tokenizer.tokens

def p_program_1(p):
    'program : statement'
    p[0] = Program(p[1])

def p_program_2(p):
    'program : statement program'
    p[0] = Program(p[1],p[2])

def p_statement_1(p):
    'statement : BIND IDENTIFIER EQUALS expression SEMICOLON'
    p[0] = Bind(p[2],p[4])

def p_statement_2(p):
    'statement : function_call SEMICOLON'
    p[0] = FunCallStmt(p[1])

def p_expression_1(p):
    'expression : LAMBDA IDENTIFIER RARROW expression'
    p[0] = Lambda(p[2],p[4])

def p_expression_2(p):
    '''expression : function_call
                  | expression_atomic
    '''
    p[0] = p[1]

def p_function_call(p):
    'function_call : IDENTIFIER expression_atomic_list'
    p[0] = FunCallExpr(p[1], p[2])

def p_expression_atomic_1(p):
    'expression_atomic : STRING_LITERAL'
    p[0] = StringLiteral(p[1])

def p_expression_atomic_2(p):
    'expression_atomic : LPAREN expression COMMA tuple_list RPAREN'
    p[0] = Tuple([p[2]] + p[4])

def p_expression_atomic_3(p):
    'expression_atomic : IDENTIFIER'
    p[0] = Identifier(p[1])

def p_expression_atomic_4(p):
    'expression_atomic : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_atomic_list_1(p):
    'expression_atomic_list : expression_atomic'
    p[0] = [p[1]]

def p_expression_atomic_list_2(p):
    'expression_atomic_list : expression_atomic expression_atomic_list'
    p[0] = [p[1]] + p[2]

def p_tuple_list_1(p):
    'tuple_list : expression'
    p[0] = [p[1]]

def p_tuple_list_2(p):
    'tuple_list : expression COMMA tuple_list'
    p[0] = [p[1]] + p[3]

def p_error(p):
    warning('Parse error: {}'.format(p))

# Build the parser
# TODO disable debug
import ply.yacc
ply.yacc.yacc(debug=True)

import logging

def parse(input):
    for t in tokens:
        debug('token: {}'.format(t))
    return ply.yacc.parse(input, debug=logging.getLogger())
