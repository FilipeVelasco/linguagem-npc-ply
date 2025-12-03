# 📋 Documentação da Gramática - Linguagem NPC

## 1️⃣ ANÁLISE LÉXICA (Lexer)

### Tokens Reconhecidos

| Token | Descrição | Exemplo | Expressão Regular |
|-------|-----------|---------|-------------------|
| `NUMBER` | Números inteiros | `10`, `100`, `55` | `\d+` |
| `STRING` | Texto entre aspas | `"Paladino"`, `"Orc"` | `"[^"]*"` |
| `IDENT` | Identificadores | `vida`, `Goblin`, `ataque` | `[a-zA-Z_][a-zA-Z0-9_]*` |
| `EQUALS` | Atribuição | `=` | `=` |
| `LBRACE` | Abre chave | `{` | `\{` |
| `RBRACE` | Fecha chave | `}` | `\}` |
| `LPAREN` | Abre parêntese | `(` | `\(` |
| `RPAREN` | Fecha parêntese | `)` | `\)` |
| `COMMA` | Vírgula | `,` | `,` |

### Palavras Reservadas

| Palavra | Token | Função |
|---------|-------|--------|
| `npc` | `NPC` | Declara um novo personagem |
| `atacar` | `ATACAR` | Executa ação de ataque |
| `imprimir` | `IMPRIMIR` | Mostra status do NPC |

---

## 2️⃣ ANÁLISE SINTÁTICA (Parser)

### Tabela de Produções e Ações Semânticas

| # | Produção | Ação Semântica | Explicação |
|---|----------|----------------|------------|
| **1** | `programa → instrucoes` | Imprime estado final dos NPCs | Regra inicial - processa todas as instruções |
| **2** | `instrucoes → instrucao instrucoes` | `pass` | Lista de instruções (recursiva) |
| **3** | `instrucoes → instrucao` | `pass` | Uma única instrução (caso base) |
| **4** | `instrucao → definicao_npc` | `pass` | Instrução pode ser criar NPC |
| **5** | `instrucao → acao_atacar` | `pass` | Instrução pode ser atacar |
| **6** | `instrucao → acao_imprimir` | `pass` | Instrução pode ser imprimir |
| **7** | `definicao_npc → NPC IDENT LBRACE lista_atributos RBRACE` | `tabela_simbolos[nome_npc] = atributos` | Cria NPC e armazena na tabela de símbolos |
| **8** | `lista_atributos → atributo lista_atributos` | `p[1].update(p[2]); p[0] = p[1]` | Combina múltiplos atributos |
| **9** | `lista_atributos → atributo` | `p[0] = p[1]` | Um único atributo |
| **10** | `atributo → IDENT EQUALS valor` | `p[0] = {p[1]: p[3]}` | Cria par chave-valor |
| **11** | `valor → NUMBER` | `p[0] = p[1]` | Valor numérico |
| **12** | `valor → STRING` | `p[0] = p[1]` | Valor textual |
| **13** | `acao_atacar → ATACAR LPAREN IDENT COMMA IDENT RPAREN` | Ver detalhes abaixo ⬇️ | Executa lógica de combate |
| **14** | `acao_imprimir → IMPRIMIR LPAREN IDENT RPAREN` | Imprime `tabela_simbolos[nome]` | Mostra status do NPC |

---

### 🎯 Ação Semântica Detalhada: `acao_atacar` (Produção #13)

```python
# Passo 1: Extrair nomes do atacante e alvo
nome_atacante = p[3]  # Primeiro IDENT
nome_alvo = p[5]      # Segundo IDENT

# Passo 2: VALIDAÇÃO SEMÂNTICA - Verificar existência
if nome_atacante not in tabela_simbolos:
    ERRO: "Atacante não existe!"
if nome_alvo not in tabela_simbolos:
    ERRO: "Alvo não existe!"

# Passo 3: Buscar dados dos NPCs
atacante = tabela_simbolos[nome_atacante]
alvo = tabela_simbolos[nome_alvo]

# Passo 4: CÁLCULO DO DANO
dano = atacante['ataque']
defesa = alvo.get('defesa', 0)  # Se não tem defesa, assume 0
dano_real = max(0, dano - defesa)  # Dano nunca é negativo

# Passo 5: APLICAR DANO (modifica estado)
alvo['vida'] -= dano_real

# Passo 6: Verificar derrota
if alvo['vida'] <= 0:
    print("NPC DERROTADO!")
```

---

## 3️⃣ ANÁLISE SEMÂNTICA

### Estruturas de Dados

```python
# TABELA DE SÍMBOLOS (Dicionário Python)
tabela_simbolos = {
    "Heroi": {
        "vida": 100,
        "ataque": 20,
        "defesa": 5,
        "classe": "Paladino"
    },
    "Goblin": {
        "vida": 50,
        "ataque": 15,
        "defesa": 2,
        "tipo": "Orc"
    }
}
```

### Regras Semânticas Implementadas

| # | Regra | Como é verificada |
|---|-------|-------------------|
| **R1** | NPCs não podem ser redeclarados | Cada NPC só pode ser criado uma vez |
| **R2** | Não pode atacar NPC inexistente | Verifica se `nome in tabela_simbolos` antes de atacar |
| **R3** | Atributos devem ter valores válidos | NUMBER para numéricos, STRING para texto |
| **R4** | Dano nunca é negativo | `max(0, dano - defesa)` |
| **R5** | Vida pode ficar negativa | Permite vida < 0 após derrota |

---

## 4️⃣ EXEMPLO DE CÓDIGO E EXECUÇÃO

### Código na Linguagem NPC:
```
npc Heroi {
    vida = 100
    ataque = 20
    defesa = 5
    classe = "Paladino"
}

npc Goblin {
    vida = 30
    ataque = 10
    defesa = 2
}

imprimir(Heroi)
atacar(Heroi, Goblin)
atacar(Heroi, Goblin)
```

### Saída da Execução:
```
DEBUG: NPC 'Heroi' criado com atributos {...}
DEBUG: NPC 'Goblin' criado com atributos {...}

STATUS Heroi: {'vida': 100, 'ataque': 20, 'defesa': 5, 'classe': 'Paladino'}

[AÇÃO] Heroi atacou Goblin!
       Dano causado: 18 (Ataque: 20 - Defesa: 2)
       Vida de Goblin: 12

[AÇÃO] Heroi atacou Goblin!
       Dano causado: 18 (Ataque: 20 - Defesa: 2)
       Vida de Goblin: -6
       ☠️ Goblin foi DERROTADO!

--- Fim da Execução ---
Estado Final dos NPCs: {'Heroi': {...}, 'Goblin': {'vida': -6, ...}}
```

---

## 5️⃣ GRAMÁTICA FORMAL (BNF)

```bnf
<programa>        ::= <instrucoes>

<instrucoes>      ::= <instrucao> <instrucoes>
                    | <instrucao>

<instrucao>       ::= <definicao_npc>
                    | <acao_atacar>
                    | <acao_imprimir>

<definicao_npc>   ::= "npc" IDENT "{" <lista_atributos> "}"

<lista_atributos> ::= <atributo> <lista_atributos>
                    | <atributo>

<atributo>        ::= IDENT "=" <valor>

<valor>           ::= NUMBER
                    | STRING

<acao_atacar>     ::= "atacar" "(" IDENT "," IDENT ")"

<acao_imprimir>   ::= "imprimir" "(" IDENT ")"
```

---

## 📊 RESUMO ESTATÍSTICO

- **Total de Tokens:** 12 (9 simples + 3 palavras reservadas)
- **Total de Produções:** 14
- **Ações Semânticas Complexas:** 2 (atacar, definir NPC)
- **Estruturas de Dados:** 1 (Tabela de Símbolos)
- **Validações Semânticas:** 5 regras

---

**Criado para o Trabalho de Compiladores**  
*Gerador: PLY (Python Lex-Yacc)*
