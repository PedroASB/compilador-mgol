# Compilador Mgol
![Static Badge](https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&logoColor=white&color=4B8BBE)
![Static Badge](https://img.shields.io/badge/stable-gray?style=for-the-badge&label=status&color=66c100)
![Static Badge](https://img.shields.io/badge/compiler_--_lexer_--_parser-gray?style=for-the-badge&label=topics&color=ef8b23)


## Descrição
- Trabalho desenvolvido como estudo de caso durante a disciplina de Compiladores do curso de Ciência da Computação (🏫 [Universidade Federal de Goiás](<https://ufg.br/>)).
- O programa consiste em um compilador da linguagem fictícia Mgol. Recebe-se como entrada um arquivo contendo o código-fonte escrito em Mgol e é produzido um código em C como saída.
- Linguagem utilizada para a implementação: **Python** (versão 3.11.3).


---
## Desenvolvedores
- Nickolas Carlos Carvalho Silva ([nickolascarlos](<https://github.com/nickolascarlos>))
- Pedro Augusto Serafim Belo ([PedroASB](<https://github.com/PedroASB>))


---
## Como Executar
Após clonar o repositório, entre no diretório principal e utilize o comando `python . <file>`, onde _\<file\>_ é um arquivo de texto contendo o código-fonte em Mgol.

Códigos-fonte de exemplo e testes unitários em Mgol estão disponíveis no diretório `unit_tests/`.

Exemplo de uso:
```bash
python . unit_tests/source.mgol
```

---
## Sobre a Linguagem Mgol
**Mgol** é uma linguagem de programação fictícia previamente desenvolvida para o estudo de caso em questão.

Essa linguagem possui os elementos básicos de uma linguagem de programação, incluindo declaração e atribuição de variáveis, leitura e escrita na saída padrão, operações matemáticas e relacionais, estruturas condicionais e estruturas de repetição.

Palavras reservadas presentes na linguagem:
- `inicio`: delimita o início do programa.
- `fim`: delimita o fim do programa.
- `varinicio`: delimita o início da declaração de variáveis.
- `varfim`: delimita o fim da declaração de variáveis.
- `leia`: lê da entrada padrão.
- `escreva`: imprime na saída padrão.
- `se`: delimita o início de uma estrutura condicional.
- `entao`: elemento de uma estrutura condicional.
- `fimse`: delimita o fim de uma estrutura condicional.
- `repita`: delimita o início de uma estrutura de repetição.
- `fimrepita`: delimita o fim de uma estrutura de repetição.
- `inteiro`: define o tipo de dado inteiro.
- `real`: define o tipo de dado real.
- `literal`: define o tipo de dado literal.

### Produções da Gramática Livre de Contexto

ID | Regra Gramatical
:--- | :---
1 | P'  → P
2 | P → inicio V A
3 | V → varincio LV
4 | LV → D LV
5 | LV → varfim pt_v
6 | D → TIPO L pt_v
7 | L → id vir L
8 | L → id
9 | TIPO → inteiro
10 | TIPO → real
11 | TIPO → literal
12 | A → ES A
13 | ES → leia id pt_v
14 | ES → escreva ARG pt_v
15 | ARG → lit
16 | ARG → num
17 | ARG → id
18 | A → CMD A
19 | CMD → id atr LD pt_v
20 | LD → OPRD opm OPRD
21 | LD → OPRD
22 | OPRD → id
23 | OPRD → num
24 | A → COND A
25 | COND → CAB CP
26 | CAB → se ab_p EXP_R fc_p entao
27 | EXP_R → OPRD opr OPRD
28 | CP → ES CP
29 | CP → CMD CP
30 | CP → COND CP
31 | CP → fimse
32 | A → R A
33 | R → CABR CPR
34 | CABR  → repita ab_p EXP_R fc_p
35 | CPR → ES CPR
36 | CPR → CMD CPR
37 | CPR → COND CPR
38 | CPR → fimrepita
39 | A → fim


---
## Sobre a Implementação
O módulo `__main__.py` representa a função principal do programa, onde são instanciadas as principais classes e realiza-se a chamada do método que inicia o processo de compilação do código-fonte.

Os demais módulos estão presentes em três pacotes contidos no diretório `analisador/`. Cada um desses pacotes representa uma etapa da arquitetura de um compilador:

1. **`analisador/lexico/`: Análise Léxica**
2. **`analisador/sintatico/`: Análise Sintática**
3. **`analisador/semantico/`: Análise Semântica e Geração de Código Final**

As três etapas foram desenvolvidas sequencialmente. Segue uma descrição de cada uma delas:

### 1 - Análise Léxica
Implementação do analisador léxico (_lexer_) e da tabela de símbolos, com a finalidade de reconhecer tokens.

**Módulos do pacote `analisador/lexico/`:**
- `consts.py`: contém as constantes utilizadas pelo analisador léxico.
- `DFA.py`: contém a classe que representa um autômato finito determinístico (DFA).
- `DFAReader.py`: contém a classe responsável pela leitura de um arquivo .dfa e retorno de uma instância de um DFA. O arquivo `automaton.dfa` contém a descrição do autômato que reconhece os tokens da linguagem Mgol.
- `DFAState.py`: contém a classe que representa um estado de um DFA.
- `Lexer.py`: contém a classe do analisador léxico.
- `SymbolTable.py`: contém a classe que representa uma tabela de símbolos.
- `Token.py`: contém a classe que representa um token.
- `types.py`: contém tipos de dados definidos para o projeto.


### 2 - Análise Sintática
Implementação do analisador sintático (_parser_) ascendente SLR(1), com o algoritmo de análise shift-reduce, para realizar a verificação de sintaxe.

Inclui recuperação de erros a nível de frase (_phrase-level recovery_) e pelo método pânico (_panic mode_).

**Módulos do pacote `analisador/sintatico/`:**
- `ActionTable.py`: contém a classe que gerencia a tabela _ACTION_ do modelo shift-reduce. Essa tabela está armazenada em `tables/action.csv`.
- `consts.py`: contém as constantes utilizadas pelo analisador sintático.
- `GotoTable.py`: contém a classe que gerencia a tabela _GOTO_ do modelo shift-reduce. Essa tabela está armazenada em `tables/goto.csv`.
- `Parser.py`: contém a classe do analisador sintático.
- `ParserStack.py`: contém a classe da pilha do analisador sintático.
- `Production.py`: contém a classe que representa uma produção gramatical.


### 3 - Análise Semântica e Geração de Código Final
Implementação do analisador semântico e gerador de código final a partir do método tradução dirigida pela sintaxe.

**Módulos do pacote `analisador/semantico/`:**
- `ObjectFileManager.py`: contém a classe responsável por gerenciar a criação e formatação do arquivo objeto `PROGRAMA.c`.
- `SemanticRulesManager.py`: contém a classe do analisador semântico.
- `SemanticStack.py`: contém a classe da pilha do analisador semântico.
