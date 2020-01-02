from utils.log import warning

reserved = {
    'bind'   : 'BIND',
    'lambda' : 'LAMBDA'
}

tokens = list(reserved.values()) + [
    'EQUALS',
    'RARROW',
    'COMMA',
    'SEMICOLON',

    'LPAREN',
    'RPAREN',

    'IDENTIFIER',
    'STRING_LITERAL'
]

t_EQUALS         = r'='
t_RARROW         = r'->'
t_COMMA          = r','
t_SEMICOLON      = r';'
t_LPAREN         = r'\('
t_RPAREN         = r'\)'
t_STRING_LITERAL = r'\"[^\n]*?\"'

# Ignored characters
t_ignore = " \t"

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_comment(t):
    r'\#[^\n]*'
    pass

def t_error(t):
    warning('Lexer error: {}'.format(t))
    t.lexer.skip(1)

# Build the lexer
# TODO disable debug
import ply.lex
ply.lex.lex(debug=True)
