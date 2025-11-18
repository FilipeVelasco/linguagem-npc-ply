import ply.yacc as yacc
from lexer import tokens  # importa a lista de tokens do lexer

# Regra principal da linguagem:
# Um NPC segue o formato:
# npc Nome {
#     atributos...
# }
def p_npc(p):
    '''npc : IDENT IDENT LBRACE atributos RBRACE'''
    
    # p[1] = IDENT (ex: npc)
    # p[2] = IDENT (ex: Goblin)
    # p[4] = dicionário de atributos
    
    # Montamos um dicionário Python com tudo organizado
    p[0] = {
        "tipo": p[1],
        "nome": p[2],
        "atributos": p[4]
    }

# Constrói a lista de atributos
# Pode ser:
#  - só 1 atributo
#  - vários atributos um atrás do outro
def p_atributos_lista(p):
    '''atributos : atributo
                 | atributos atributo'''
    
    # Caso só tenha UM atributo
    if len(p) == 2:
        # p[1] é uma tupla ("vida", 20)
        p[0] = {p[1][0]: p[1][1]}
    
    # Caso tenha mais de um
    else:
        # p[1] é o dicionário já criado
        # p[2] é a nova tupla a ser adicionada
        p[1][p[2][0]] = p[2][1]
        p[0] = p[1]

# Define o formato de um atributo:
# exemplo: vida = 20
def p_atributo(p):
    '''atributo : IDENT EQUALS valor'''
    
    # Retorna uma tupla:
    # ("vida", 20)
    p[0] = (p[1], p[3])

# Um valor pode ser:
# - número
# - string
# - identificador (ex: uma palavra)
def p_valor(p):
    '''valor : NUMBER
             | STRING
             | IDENT'''
    p[0] = p[1]

# Se ocorrer erro na gramática
def p_error(p):
    print("Erro de sintaxe!", p)

# Constrói o parser
parser = yacc.yacc()

# Teste quando você roda o arquivo direto
if __name__ == "__main__":
    texto = '''
    npc Goblin {
        vida = 20
        ataque = 5
        classe = "guerreiro"
    }
    '''
    result = parser.parse(texto)
    print(result)
