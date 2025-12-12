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

## 📌 SLIDE 3b: Simulação de Derivação Complexa (1 min)

### Código de Entrada:
```
npc Heroi { vida=100 ataque=20 defesa=5 }
npc Goblin { vida=50 ataque=15 defesa=2 }
atacar(Heroi, Goblin)
imprimir(Goblin)
```

### Derivação Passo a Passo:

**Passo 1: Derivação da primeira instrução (Criar Herói)**

```
programa
  ⇒ instrucoes
  ⇒ instrucao instrucoes
  ⇒ definicao_npc instrucoes
  ⇒ NPC IDENT LBRACE lista_atributos RBRACE instrucoes
  ⇒ npc Heroi { lista_atributos } instrucoes
  ⇒ npc Heroi { atributo lista_atributos } instrucoes
  ⇒ npc Heroi { IDENT EQUALS valor lista_atributos } instrucoes
  ⇒ npc Heroi { vida = 100 lista_atributos } instrucoes
  ...
  [AÇÃO SEMÂNTICA: tabela_simbolos["Heroi"] = {"vida": 100, "ataque": 20, "defesa": 5}]
```

**Passo 2: Derivação da segunda instrução (Criar Goblin)**

```
instrucoes
  ⇒ instrucao instrucoes
  ⇒ definicao_npc instrucoes
  ⇒ npc Goblin { vida=50 ataque=15 defesa=2 } instrucoes
  [AÇÃO SEMÂNTICA: tabela_simbolos["Goblin"] = {"vida": 50, "ataque": 15, "defesa": 2}]
```

**Passo 3: Derivação da ação de ataque**

```
instrucoes
  ⇒ instrucao instrucoes
  ⇒ acao_atacar instrucoes
  ⇒ ATACAR LPAREN IDENT COMMA IDENT RPAREN instrucoes
  ⇒ atacar ( Heroi , Goblin ) instrucoes
  
  [AÇÃO SEMÂNTICA COMPLEXA]
  ├─ Validação: Verifica se Heroi e Goblin existem ✓
  ├─ Busca: atacante = tabela_simbolos["Heroi"]
  ├─ Busca: alvo = tabela_simbolos["Goblin"]
  ├─ Cálculo: dano = 20 (ataque do Heroi)
  ├─ Cálculo: defesa = 2 (defesa do Goblin)
  ├─ Cálculo: dano_real = max(0, 20 - 2) = 18
  ├─ Modificação: alvo['vida'] = 50 - 18 = 32
  └─ Output: "[AÇÃO] Heroi atacou Goblin! Dano: 18"
```

**Passo 4: Derivação da ação de impressão**

```
instrucoes
  ⇒ instrucao
  ⇒ acao_imprimir
  ⇒ IMPRIMIR LPAREN IDENT RPAREN
  ⇒ imprimir ( Goblin )
  
  [AÇÃO SEMÂNTICA]
  ├─ Busca: tabela_simbolos["Goblin"]
  └─ Output: "STATUS Goblin: {'vida': 32, 'ataque': 15, 'defesa': 2}"
```

### Estado Final da Tabela de Símbolos:
```python
{
    "Heroi": {"vida": 100, "ataque": 20, "defesa": 5},
    "Goblin": {"vida": 32, "ataque": 15, "defesa": 2}  # Vida reduzida!
}
```

---

## 📌 SLIDE 4: Análise Semântica Formal (2 min)

### Tabela Semântica Completa

| Produção | Domínio | Predicados (Condições) | Ações Semânticas | Efeitos |
|----------|---------|----------------------|-------------------|---------|
| `definicao_npc → NPC IDENT { lista_atributos }` | `IDENT: string`, `atributos: dict` | ¬∃(nome ∈ TS) | `TS[nome] ← atributos`; `tipos[nome] ← "NPC"` | Inserção em TS; Verificação de redeclaração |
| `atributo → IDENT = valor` | `IDENT: string`, `NUMBER: int`, `STRING: string` | `valor ∈ {int, string}` | `tipo[IDENT] ← typeof(valor)` | Atribuição de tipo a propriedade |
| `acao_atacar → ATACAR(IDENT₁, IDENT₂)` | `IDENT₁, IDENT₂: string` | `∃IDENT₁ ∈ TS ∧ ∃IDENT₂ ∈ TS ∧ vida > 0 ∧ ataque ∈ Z⁺ ∧ defesa ∈ Z⁺` | `dano ← ataque₁ - defesa₂`; `vida₂ ← vida₂ - max(0, dano)`; `emit("[AÇÃO]...")` | Modificação de estado em TS; Validação de tipo |
| `acao_imprimir → IMPRIMIR(IDENT)` | `IDENT: string` | `∃IDENT ∈ TS ∧ tipo[IDENT] = "NPC"` | `emit(TS[IDENT])` | Sem efeito colateral em TS |

### Domínios e Tipos:

```
Domínio de Valores:
  V = Int ∪ String
  
Domínio de Identificadores:
  ID = {strings: [a-zA-Z_][a-zA-Z0-9_]*}
  
Domínio de NPCs:
  NPC = {
    nome: ID,
    vida: Int (vida > 0),
    ataque: Int (ataque ≥ 0),
    defesa: Int (defesa ≥ 0)
  }

Tabela de Símbolos (TS):
  TS: ID → NPC
  Invariante: chaves únicas, sem redeclaração
```

### Verificação de Tipos:

```
typeof(X):
  if X ∈ Int then typeof(X) = integer
  if X ∈ String then typeof(X) = string
  if X ∈ TS then typeof(X) = npc

Regras de Tipagem:
  [IDENT = NUMBER]  ⇒ tipo(IDENT) = integer
  [IDENT = STRING]  ⇒ tipo(IDENT) = string
  [ATACAR(I₁, I₂)]  ⇒ tipo(I₁) = npc ∧ tipo(I₂) = npc
  [IMPRIMIR(I)]     ⇒ tipo(I) = npc
```

### Tabela de Atributos (com propagação):

```
Atributo      | Tipo    | Domínio      | Requerido | Padrão
--------------|---------|--------------|-----------|--------
nome          | string  | ID           | Sim       | —
vida          | integer | Z⁺ ∪ {0}    | Sim       | —
ataque        | integer | Z⁺ ∪ {0}    | Não       | 0
defesa        | integer | Z⁺ ∪ {0}    | Não       | 0
classe        | string  | {Herói, Monstro, Boss} | Não | "Monstro"
```

### Exemplo de Análise Semântica Detalhada - Ação ATACAR:

**Entrada:** `atacar(Heroi, Goblin)`

**Processamento Semântico:**

```
Fase 1: VERIFICAÇÃO DE TIPOS
────────────────────────────
  1. Verificar: tipo(Heroi) = npc ✓  [Heroi ∈ TS]
  2. Verificar: tipo(Goblin) = npc ✓ [Goblin ∈ TS]
  3. Predicado: ∃Heroi ∈ TS ∧ ∃Goblin ∈ TS  [VÁLIDO]

Fase 2: VALIDAÇÃO SEMÂNTICA
────────────────────────────
  4. Validar: TS["Heroi"]["ataque"] ∈ Z⁺ = 20  [VÁLIDO]
  5. Validar: TS["Goblin"]["defesa"] ∈ Z⁺ = 2  [VÁLIDO]
  6. Validar: TS["Goblin"]["vida"] > 0 = 50    [VÁLIDO]

Fase 3: CÁLCULO SEMÂNTICO
──────────────────────────
  7. atacante = TS["Heroi"]
  8. alvo = TS["Goblin"]
  9. dano = atacante.ataque = 20
  10. defesa = alvo.defesa = 2
  11. dano_real = max(0, 20 - 2) = 18

Fase 4: MODIFICAÇÃO DE ESTADO (Side Effect)
────────────────────────────────────────────
  12. TS["Goblin"]["vida"] := 50 - 18 = 32
  13. Verificar: vida > 0 ? 32 > 0 [SIM]

Fase 5: EMISSÃO DE CÓDIGO (Output)
──────────────────────────────────
  14. emit: "[AÇÃO] Heroi atacou Goblin! Dano: 18"
```

**Código da Implementação:**

```python
def p_acao_atacar(p):
    '''acao_atacar : ATACAR LPAREN IDENT COMMA IDENT RPAREN'''
    nome_atacante = p[3]
    nome_alvo = p[5]
    
    # ====== FASE 1: VERIFICAÇÃO DE TIPOS ======
    if nome_atacante not in tabela_simbolos:
        print(f"[ERRO SEMÂNTICO] Tipo indefinido: {nome_atacante}")
        return
    if nome_alvo not in tabela_simbolos:
        print(f"[ERRO SEMÂNTICO] Tipo indefinido: {nome_alvo}")
        return
    
    # ====== FASE 2: VALIDAÇÃO SEMÂNTICA ======
    atacante = tabela_simbolos[nome_atacante]
    alvo = tabela_simbolos[nome_alvo]
    
    # Verificar atributos obrigatórios
    if 'ataque' not in atacante:
        print(f"[ERRO SEMÂNTICO] Atributo 'ataque' não definido em {nome_atacante}")
        return
    if 'defesa' not in alvo:
        print(f"[ERRO SEMÂNTICO] Atributo 'defesa' não definido em {nome_alvo}")
        return
    
    # Verificar predicados
    if alvo['vida'] <= 0:
        print(f"[ERRO SEMÂNTICO] {nome_alvo} já está derrotado (vida ≤ 0)")
        return
    
    # ====== FASE 3: CÁLCULO SEMÂNTICO ======
    dano = atacante.get('ataque', 0)
    defesa = alvo.get('defesa', 0)
    dano_real = max(0, dano - defesa)
    
    # ====== FASE 4: MODIFICAÇÃO DE ESTADO ======
    alvo['vida'] -= dano_real
    
    # ====== FASE 5: EMISSÃO ======
    print(f"[AÇÃO] {nome_atacante} atacou {nome_alvo}!")
    print(f"       Dano calculado: {dano} - {defesa} = {dano_real}")
    print(f"       Vida de {nome_alvo}: {alvo['vida'] + dano_real} → {alvo['vida']}")
    
    if alvo['vida'] <= 0:
        print(f"       ☠️ {nome_alvo} foi DERROTADO!")
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
