import ply.lex as lex

# Palavras Reservadas
reserved = {
    'npc': 'NPC',
    'atacar': 'ATACAR',
    'imprimir': 'IMPRIMIR'
}

# Lista de tokens que nossa linguagem reconhece.
# Pense neles como "palavras importantes" da linguagem.
tokens = [
    'NUMBER',  # números (ex: 10, 20, 55)
    'IDENT',   # identificadores (ex: vida, ataque, Goblin)
    'STRING',  # textos entre aspas
    'EQUALS',  # símbolo '='
    'LBRACE',  # '{'
    'RBRACE',  # '}'
    'LPAREN',  # '('
    'RPAREN',  # ')'
    'COMMA',   # ','
] + list(reserved.values())

# Regras simples: tokens que são só um caractere
t_EQUALS = r'='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA  = r','

# Ignora espaços, tabs e quebras de linha
t_ignore = ' \t'

# Regra para Strings (ex: "Orc")
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value.strip('"') # Remove as aspas
    return t

# Regra para Identificadores E Palavras Reservadas
# O lexer verifica se a palavra está na lista 'reserved'.
# Se estiver, retorna o token específico (ex: NPC), senão retorna IDENT.
def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENT') 
    return t

# Regra para números inteiros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Tratamento de erro: se o caractere não for reconhecido
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Cria o lexer
lexer = lex.lex()
