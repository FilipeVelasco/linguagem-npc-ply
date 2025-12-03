# 🎤 Guia de Apresentação - Trabalho de Compiladores
## Linguagem NPC com PLY (Python Lex-Yacc)

*Tempo máximo: 7 minutos*

---

## 📌 SLIDE 1: Introdução (30 seg)

### Gerador Escolhido: PLY (Python Lex-Yacc)
- **Linguagem:** Python
- **Baseado em:** Lex e Yacc (ferramentas clássicas do Unix)
- **Vantagens:** 
  - Simples de usar
  - Integração nativa com Python
  - Ótima documentação

### Projeto: Linguagem para definir NPCs de Jogos
- ✅ **NÃO é calculadora!**
- ✅ Permite criar personagens
- ✅ Executar ações (atacar, imprimir status)
- ✅ Sistema de combate com dano/defesa

---

## 📌 SLIDE 2: Análise Léxica (1 min)

### Onde está no código: `lexer.py`

**Tokens Criados:**

```python
# Expressões Regulares que criei:
t_EQUALS = r'='          # símbolo de atribuição
t_LBRACE = r'\{'         # abre chave
t_RBRACE = r'\}'         # fecha chave
t_LPAREN = r'\('         # abre parêntese (para funções)
t_RPAREN = r'\)'         # fecha parêntese
t_COMMA  = r','          # vírgula (separador de argumentos)

def t_STRING(t):
    r'"[^"]*"'           # texto entre aspas
    t.value = t.value.strip('"')
    return t

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'  # identificadores
    t.type = reserved.get(t.value, 'IDENT')
    return t

def t_NUMBER(t):
    r'\d+'               # números inteiros
    t.value = int(t.value)
    return t
```

**Palavras Reservadas Adicionadas:**
```python
reserved = {
    'npc': 'NPC',           # declarar personagem
    'atacar': 'ATACAR',     # ação de combate
    'imprimir': 'IMPRIMIR'  # debug/status
}
```

**Total:** 12 tokens (9 simples + 3 palavras reservadas)

---

## 📌 SLIDE 3: Análise Sintática - Regras Gramaticais (1.5 min)

### Onde está no código: `parser.py`

**Produções Principais:**

```python
# 1. Criar NPC
def p_definicao_npc(p):
    '''definicao_npc : NPC IDENT LBRACE lista_atributos RBRACE'''
    # Formato: npc Nome { atributos }

# 2. Lista de atributos (recursiva)
def p_lista_atributos(p):
    '''lista_atributos : atributo lista_atributos
                       | atributo'''
    # Permite múltiplos atributos

# 3. Atributo individual
def p_atributo(p):
    '''atributo : IDENT EQUALS valor'''
    # Formato: vida = 100

# 4. Ação de ataque
def p_acao_atacar(p):
    '''acao_atacar : ATACAR LPAREN IDENT COMMA IDENT RPAREN'''
    # Formato: atacar(Heroi, Monstro)

# 5. Ação de impressão
def p_acao_imprimir(p):
    '''acao_imprimir : IMPRIMIR LPAREN IDENT RPAREN'''
    # Formato: imprimir(Heroi)
```

**Gramática BNF:**
```
programa      → instrucoes
instrucoes    → instrucao instrucoes | instrucao
instrucao     → definicao_npc | acao_atacar | acao_imprimir
definicao_npc → npc IDENT { lista_atributos }
acao_atacar   → atacar(IDENT, IDENT)
```

---

## 📌 SLIDE 4: Ações Semânticas (1.5 min)

### Tabela de Produções e Ações

| Produção | Ação Semântica | O que faz |
|----------|----------------|-----------|
| `definicao_npc` | `tabela_simbolos[nome] = atributos` | Armazena NPC na memória |
| `acao_atacar` | `alvo['vida'] -= (ataque - defesa)` | Calcula e aplica dano |
| `acao_imprimir` | `print(tabela_simbolos[nome])` | Mostra status |

### Código da Ação Semântica mais complexa:

```python
def p_acao_atacar(p):
    '''acao_atacar : ATACAR LPAREN IDENT COMMA IDENT RPAREN'''
    nome_atacante = p[3]
    nome_alvo = p[5]
    
    # VALIDAÇÃO SEMÂNTICA
    if nome_atacante not in tabela_simbolos:
        print(f"ERRO: Atacante '{nome_atacante}' não existe!")
        return
    
    # BUSCA NA TABELA DE SÍMBOLOS
    atacante = tabela_simbolos[nome_atacante]
    alvo = tabela_simbolos[nome_alvo]
    
    # CÁLCULO
    dano = atacante.get('ataque', 0)
    defesa = alvo.get('defesa', 0)
    dano_real = max(0, dano - defesa)
    
    # MODIFICAÇÃO DE ESTADO
    alvo['vida'] -= dano_real
    
    # VERIFICAÇÃO DE DERROTA
    if alvo['vida'] <= 0:
        print(f"☠️ {nome_alvo} foi DERROTADO!")
```

**Estrutura de Dados:**
```python
# TABELA DE SÍMBOLOS
tabela_simbolos = {
    "Heroi": {"vida": 100, "ataque": 20, "defesa": 5},
    "Goblin": {"vida": 50, "ataque": 15, "defesa": 2}
}
```

---

## 📌 SLIDE 5: Árvore de Derivação (1 min)

### Sentença: `npc Goblin { vida = 50 }`

**Árvore Sintática:**
```
                programa
                   |
              instrucoes
                   |
               instrucao
                   |
            definicao_npc
         /      |       \
      NPC    IDENT    {...}
       |       |
     "npc"  "Goblin"
```

**Árvore Anotada (com valores):**
```
         definicao_npc
              |
    [AÇÃO: tabela_simbolos["Goblin"] = {"vida": 50}]
              |
         atributo
              |
        {"vida": 50}
         /     \
    "vida"  =  50
```

---

## 📌 SLIDE 6: Demonstração ao Vivo (2 min)

### Código de Exemplo:
```python
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
atacar(Heroi, Monstro)
atacar(Heroi, Monstro)
atacar(Heroi, Monstro)
```

**Execute:** `python parser.py`

### Saída Esperada:
```
DEBUG: NPC 'Heroi' criado com atributos {...}
DEBUG: NPC 'Monstro' criado com atributos {...}

STATUS Heroi: {'vida': 100, 'ataque': 20, 'defesa': 5, 'classe': 'Paladino'}

[AÇÃO] Heroi atacou Monstro!
       Dano causado: 18 (Ataque: 20 - Defesa: 2)
       Vida de Monstro: 32

[AÇÃO] Heroi atacou Monstro!
       Dano causado: 18
       Vida de Monstro: 14

[AÇÃO] Heroi atacou Monstro!
       Dano causado: 18
       Vida de Monstro: -4
       ☠️ Monstro foi DERROTADO!
```

---

## 📌 SLIDE 7: Resumo Técnico (30 seg)

### Estatísticas do Projeto

| Componente | Quantidade |
|------------|------------|
| **Tokens criados** | 12 |
| **Produções gramaticais** | 14 |
| **Palavras reservadas** | 3 |
| **Ações semânticas complexas** | 2 |
| **Validações semânticas** | 5 |
| **Estruturas de dados** | 1 (Tabela de Símbolos) |

### Conceitos Aplicados:
✅ Análise Léxica (Expressões Regulares)  
✅ Análise Sintática (Gramática Livre de Contexto)  
✅ Análise Semântica (Tabela de Símbolos, Validação de Tipos)  
✅ Tradução Dirigida pela Sintaxe  
✅ Tratamento de Erros (Léxico e Semântico)  

---

## 🎯 DICAS PARA A APRESENTAÇÃO

### O que MOSTRAR no código:

1. **lexer.py:** 
   - Aponte as expressões regulares
   - Mostre a função `t_IDENT` que trata palavras reservadas

2. **parser.py:**
   - Mostre a tabela de símbolos (linha ~8)
   - Aponte a função `p_definicao_npc` (criação de NPC)
   - Destaque a função `p_acao_atacar` (lógica complexa)

3. **Árvores:**
   - Use o arquivo `ARVORES_DERIVACAO.md`
   - Mostre a diferença entre árvore sintática e anotada

### Possíveis Perguntas:

**P: Por que escolheu PLY?**
R: Porque uso Python, tem boa documentação e é didático para aprender compiladores.

**P: Como trata erros?**
R: Tenho `t_error` no lexer para caracteres inválidos e `p_error` no parser para sintaxe. Na semântica, verifico se NPCs existem antes de atacar.

**P: Qual a maior dificuldade?**
R: Implementar a lógica de combate mantendo o estado consistente na tabela de símbolos.

**P: Pode estender o projeto?**
R: Sim! Posso adicionar estruturas de controle (if/while), funções customizadas, tipos de dados, etc.

---

## 📚 Arquivos de Referência

- `DOCUMENTACAO_GRAMATICA.md` - Tabelas completas
- `ARVORES_DERIVACAO.md` - Árvores detalhadas
- `lexer.py` - Código do analisador léxico
- `parser.py` - Código do analisador sintático

---

**Boa apresentação! 🚀**
