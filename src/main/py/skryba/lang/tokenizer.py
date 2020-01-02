from utils.log import warning

tokens = (
    'BIND',
    'LAMBDA',

    'EQUALS',
    'RARROW',
    'COMMA',
    'SEMICOLON',

    'LPAREN',
    'RPAREN',

    'IDENTIFIER',
    'STRING_LITERAL'
)

t_BIND           = r'bind'
t_LAMBDA         = r'lambda'
t_EQUALS         = r'='
t_RARROW         = r'->'
t_COMMA          = r','
t_SEMICOLON      = r';'
t_LPAREN         = r'\('
t_RPAREN         = r'\)'
t_IDENTIFIER     = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_STRING_LITERAL = r'\"[^\n]*?\"'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_comment(t):
    r'\#[^\n]*'
    pass

def t_error(t):
    warning('Illegal character {}'.format(None if ((t is None) or (t.value is None)) else (t.value[0])))
    t.lexer.skip(1)

# Build the lexer
# TODO disable debug
import ply.lex
ply.lex.lex(debug=True)
