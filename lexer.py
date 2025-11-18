import ply.lex as lex

# Lista de tokens que nossa linguagem reconhece.
# Pense neles como "palavras importantes" da linguagem.
tokens = [
    'NUMBER',  # números (ex: 10, 20, 55)
    'IDENT',   # identificadores (ex: vida, ataque, Goblin)
    'STRING',  # textos entre aspas
    'EQUALS',  # símbolo '='
    'LBRACE',  # '{'
    'RBRACE'   # '}'
]

# Regras simples: tokens que são só um caractere
t_EQUALS = r'='     # símbolo =
t_LBRACE = r'\{'    # abre chave {
t_RBRACE = r'\}'    # fecha chave }

# Reconhece strings entre aspas, ex: "guerreiro"
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value.strip('"')  # remove as aspas
    return t

# Reconhece identificadores: palavras com letras e números
# Ex: nome, Goblin, vida, ataque
def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Reconhece números inteiros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # converte para inteiro
    return t

# Ignora espaços, tabs e quebras de linha
t_ignore = ' \t\n'

# Tratamento de erro: se o caractere não for reconhecido
def t_error(t):
    print("Caractere ilegal:", t.value[0])
    t.lexer.skip(1)

# Cria o lexer
lexer = lex.lex()
