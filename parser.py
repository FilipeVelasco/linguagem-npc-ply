import ply.yacc as yacc
from lexer import tokens

# --- TABELA DE SÍMBOLOS ---
# Aqui armazenamos o estado global do nosso "jogo".
# Em um compilador real, isso armazenaria tipos e endereços de memória.
# Aqui, armazena os atributos dos nossos monstros.
tabela_simbolos = {}

# --- REGRAS DA GRAMÁTICA ---

# Regra Inicial: Um programa é uma lista de instruções
def p_programa(p):
    '''programa : instrucoes'''
    print("\n--- Fim da Execução ---")
    print("Estado Final dos NPCs:", tabela_simbolos)

def p_instrucoes(p):
    '''instrucoes : instrucao instrucoes
                  | instrucao'''
    pass

# Uma instrução pode ser criar um NPC ou executar uma ação
def p_instrucao(p):
    '''instrucao : definicao_npc
                 | acao_atacar
                 | acao_imprimir'''
    pass

# --- DEFINIÇÃO DE NPC ---
# Ex: npc Goblin { vida=10 ... }
def p_definicao_npc(p):
    '''definicao_npc : NPC IDENT LBRACE lista_atributos RBRACE'''
    nome_npc = p[2]
    atributos = p[4]
    
    # AÇÃO SEMÂNTICA: Salvar na tabela de símbolos
    tabela_simbolos[nome_npc] = atributos
    print(f"DEBUG: NPC '{nome_npc}' criado com atributos {atributos}")

# --- LISTA DE ATRIBUTOS ---
def p_lista_atributos(p):
    '''lista_atributos : atributo lista_atributos
                       | atributo'''
    if len(p) == 3:
        p[1].update(p[2]) # Junta os dicionários
        p[0] = p[1]
    else:
        p[0] = p[1]

def p_atributo(p):
    '''atributo : IDENT EQUALS valor'''
    # Retorna um dicionário simples { "vida": 20 }
    p[0] = {p[1]: p[3]}

def p_valor(p):
    '''valor : NUMBER
             | STRING'''
    p[0] = p[1]

# --- AÇÃO: ATACAR ---
# Ex: atacar(Goblin, Heroi)
def p_acao_atacar(p):
    '''acao_atacar : ATACAR LPAREN IDENT COMMA IDENT RPAREN'''
    nome_atacante = p[3]
    nome_alvo = p[5]

    # AÇÃO SEMÂNTICA: Lógica do combate
    # 1. Verificar se os NPCs existem
    if nome_atacante not in tabela_simbolos:
        print(f"ERRO SEMÂNTICO: Atacante '{nome_atacante}' não existe!")
        return
    if nome_alvo not in tabela_simbolos:
        print(f"ERRO SEMÂNTICO: Alvo '{nome_alvo}' não existe!")
        return

    atacante = tabela_simbolos[nome_atacante]
    alvo = tabela_simbolos[nome_alvo]

    # 2. Calcular dano
    dano = atacante.get('ataque', 0)
    defesa = alvo.get('defesa', 0) # Se não tiver defesa, assume 0
    dano_real = max(0, dano - defesa)

    # 3. Aplicar dano
    alvo['vida'] -= dano_real
    
    print(f"\n[AÇÃO] {nome_atacante} atacou {nome_alvo}!")
    print(f"       Dano causado: {dano_real} (Ataque: {dano} - Defesa: {defesa})")
    print(f"       Vida de {nome_alvo}: {alvo['vida']}")

    if alvo['vida'] <= 0:
        print(f"       ☠️ {nome_alvo} foi DERROTADO!")

# --- AÇÃO: IMPRIMIR ---
# Ex: imprimir(Goblin) - Para ver o status atual
def p_acao_imprimir(p):
    '''acao_imprimir : IMPRIMIR LPAREN IDENT RPAREN'''
    nome = p[3]
    if nome in tabela_simbolos:
        print(f"STATUS {nome}: {tabela_simbolos[nome]}")
    else:
        print(f"Erro: {nome} não encontrado.")

def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}' (linha {p.lineno})")
    else:
        print("Erro de sintaxe no final do arquivo (EOF)")

# Constroi o parser
parser = yacc.yacc()

# --- EXECUÇÃO ---
if __name__ == "__main__":
    # Exemplo de código na nossa linguagem
    codigo_fonte = '''
    npc Heroi {
        vida = 100
        ataque = 20
        defesa = 5
        classe = "Paladino"
    }

    npc Monstro {
        vida = 50
        ataque = 15
        defesa = 2
        tipo = "Orc"
    }

    imprimir(Heroi)
    imprimir(Monstro)

    atacar(Heroi, Monstro)
    atacar(Monstro, Heroi)
    atacar(Heroi, Monstro)
    atacar(Heroi, Monstro)
    '''

    print("--- Iniciando Análise e Execução ---")
    parser.parse(codigo_fonte)