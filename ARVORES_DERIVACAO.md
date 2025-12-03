# 🌳 Árvores de Derivação - Linguagem NPC

Este documento mostra como o parser processa o código através de árvores de derivação.

---

## EXEMPLO 1: Definição Simples de NPC

### 📝 Código de Entrada:
```
npc Goblin {
    vida = 50
}
```

---

### 🌳 ÁRVORE DE DERIVAÇÃO (Sintática)

Esta árvore mostra **como o parser quebra a sentença** seguindo as regras gramaticais:

```
                          programa
                             |
                        instrucoes
                             |
                         instrucao
                             |
                      definicao_npc
                   /       |        \
                 NPC     IDENT    LBRACE lista_atributos RBRACE
                  |        |        |          |            |
                "npc"  "Goblin"    "{"     atributo        "}"
                                              |
                                    IDENT EQUALS valor
                                      |     |      |
                                   "vida"  "="  NUMBER
                                                   |
                                                  50
```

**Explicação passo a passo:**
1. `programa` → começa aqui
2. `instrucoes` → lista de comandos
3. `instrucao` → um comando específico
4. `definicao_npc` → é uma definição de NPC
5. Divide em: palavra `npc` + nome `Goblin` + bloco `{ ... }`
6. Dentro do bloco: `vida = 50`

---

### 🎯 ÁRVORE ANOTADA (Semântica)

Esta árvore mostra **os valores calculados em cada nó** (ações semânticas):

```
                          programa
                             |
                       [Estado Final: tabela_simbolos = {"Goblin": {...}}]
                             |
                        instrucoes
                             |
                         instrucao
                             |
                      definicao_npc
                   /       |        \
                 NPC     IDENT    LBRACE lista_atributos RBRACE
                  |        |        |          |            |
                "npc"  "Goblin"    "{"    [{"vida": 50}]   "}"
                                              |
                                    atributo
                                      |
                              [{"vida": 50}]
                                      |
                                IDENT EQUALS valor
                                  |     |      |
                               "vida"  "="   [50]
                                              |
                                           NUMBER
                                              |
                                             50

📌 AÇÃO SEMÂNTICA EXECUTADA:
   tabela_simbolos["Goblin"] = {"vida": 50}
```

**O que acontece:**
- ✅ Token `50` é reconhecido como `NUMBER`
- ✅ `atributo` cria dicionário `{"vida": 50}`
- ✅ `definicao_npc` armazena na tabela de símbolos
- ✅ Resultado: NPC "Goblin" criado com vida=50

---

## EXEMPLO 2: Comando de Ataque

### 📝 Código de Entrada:
```
atacar(Heroi, Goblin)
```

---

### 🌳 ÁRVORE DE DERIVAÇÃO (Sintática)

```
                    programa
                       |
                  instrucoes
                       |
                   instrucao
                       |
                  acao_atacar
            /       |      |      |      |      \
        ATACAR  LPAREN  IDENT  COMMA  IDENT  RPAREN
           |       |       |      |      |       |
       "atacar"   "("   "Heroi"  ","  "Goblin"  ")"
```

---

### 🎯 ÁRVORE ANOTADA (Semântica)

```
                    programa
                       |
              [Executa ação de ataque]
                       |
                  instrucoes
                       |
                   instrucao
                       |
                  acao_atacar
            /       |      |      |      |      \
        ATACAR  LPAREN  IDENT  COMMA  IDENT  RPAREN
           |       |       |      |      |       |
       "atacar"   "("   "Heroi"  ","  "Goblin"  ")"
                          |             |
                    [atacante]       [alvo]
                          |             |
                      BUSCA NA     BUSCA NA
                   TABELA SÍMBOLOS  TABELA
                          |             |
                    {"ataque":20}  {"vida":50,
                    {"defesa":5}    "defesa":2}

📌 AÇÕES SEMÂNTICAS EXECUTADAS:

1️⃣ Validação:
   ✅ "Heroi" existe? → SIM
   ✅ "Goblin" existe? → SIM

2️⃣ Cálculo:
   dano = atacante["ataque"] = 20
   defesa = alvo["defesa"] = 2
   dano_real = max(0, 20 - 2) = 18

3️⃣ Modificação do Estado:
   tabela_simbolos["Goblin"]["vida"] = 50 - 18 = 32

4️⃣ Saída:
   "[AÇÃO] Heroi atacou Goblin!"
   "Dano causado: 18"
   "Vida de Goblin: 32"
```

---

## EXEMPLO 3: Programa Completo

### 📝 Código de Entrada:
```
npc Heroi {
    vida = 100
    ataque = 20
}

npc Goblin {
    vida = 50
    defesa = 2
}

atacar(Heroi, Goblin)
imprimir(Goblin)
```

---

### 🌳 ÁRVORE DE DERIVAÇÃO (Simplificada)

```
                          programa
                             |
                        instrucoes
                    /        |        \
               instrucao  instrucoes  (recursão)
                  |           |
            definicao_npc  instrucao
                  |           |
            [npc Heroi]  definicao_npc
                             |
                       [npc Goblin]
                             |
                        instrucoes
                       /         \
                  instrucao    instrucoes
                     |             |
                acao_atacar    instrucao
                     |             |
            [atacar(...)]    acao_imprimir
                                  |
                            [imprimir(...)]
```

---

### 🎯 ÁRVORE ANOTADA COM EXECUÇÃO SEQUENCIAL

```
PASSO 1: Criar Heroi
   definicao_npc → tabela_simbolos["Heroi"] = {"vida": 100, "ataque": 20}
   ✅ Estado: {"Heroi": {...}}

PASSO 2: Criar Goblin
   definicao_npc → tabela_simbolos["Goblin"] = {"vida": 50, "defesa": 2}
   ✅ Estado: {"Heroi": {...}, "Goblin": {...}}

PASSO 3: Executar Ataque
   acao_atacar → 
      - Busca "Heroi" → ataque = 20
      - Busca "Goblin" → vida = 50, defesa = 2
      - Calcula: dano = 20 - 2 = 18
      - Modifica: Goblin.vida = 50 - 18 = 32
   ✅ Estado: {"Heroi": {...}, "Goblin": {"vida": 32, "defesa": 2}}

PASSO 4: Imprimir Status
   acao_imprimir →
      - Busca "Goblin" na tabela
      - Imprime: {"vida": 32, "defesa": 2}
   ✅ Saída: "STATUS Goblin: {'vida': 32, 'defesa': 2}"

RESULTADO FINAL:
   tabela_simbolos = {
       "Heroi": {"vida": 100, "ataque": 20},
       "Goblin": {"vida": 32, "defesa": 2}
   }
```

---

## 📊 COMPARAÇÃO: Árvore Sintática vs Árvore Semântica

| Aspecto | Árvore Sintática | Árvore Anotada (Semântica) |
|---------|------------------|----------------------------|
| **Objetivo** | Mostrar estrutura gramatical | Mostrar valores calculados |
| **Nós** | Tokens e não-terminais | Valores e ações executadas |
| **Quando** | Durante parsing (análise) | Durante execução |
| **Informação** | O que é cada parte | Qual valor cada parte tem |
| **Exemplo** | `IDENT` | `"Goblin"` ou `{"vida": 50}` |

---

## 🎓 CONCEITOS IMPORTANTES

### 1. Derivação à Esquerda
O parser processa da esquerda para direita:
```
npc Goblin { vida = 50 }
 ↓    ↓       ↓
[1]  [2]    [3,4,5]
```

### 2. Recursão nas Produções
```
instrucoes → instrucao instrucoes  (recursão à direita)
```
Permite processar múltiplos comandos em sequência.

### 3. Atributos Sintetizados
Valores "sobem" na árvore:
```
NUMBER(50) → valor[50] → atributo[{"vida": 50}] → lista_atributos[{...}]
```

### 4. Efeitos Colaterais (Side Effects)
Algumas ações modificam estado global:
```
definicao_npc → MODIFICA tabela_simbolos
acao_atacar   → MODIFICA vida do alvo
```

---

## ✅ VERIFICAÇÃO DE CORRETUDE

### Exemplo: Atacar NPC Inexistente

**Código:**
```
atacar(Dragao, Heroi)
```

**Árvore (com ERRO):**
```
                  acao_atacar
            /       |      |      |      |      \
        ATACAR  LPAREN  IDENT  COMMA  IDENT  RPAREN
                          |             |
                      "Dragao"       "Heroi"
                          |             |
                    BUSCA NA       BUSCA NA
                   TABELA (❌)     TABELA (✅)
                          |
                   NÃO ENCONTRADO!

📌 ERRO SEMÂNTICO:
   "Atacante 'Dragao' não existe!"
   ❌ Ação NÃO é executada
```

---

**Criado para o Trabalho de Compiladores**  
*Estas árvores demonstram a Tradução Dirigida pela Sintaxe (Syntax-Directed Translation)*
