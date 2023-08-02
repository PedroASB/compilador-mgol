# compilador-mgol
Compilador Mgol escrito em Python

## TODO

- [x] Implementação da classe DFA
- [x] Implementação da classe Lexer
  - [x] Funções bases: implementar as funcionalidades básicas do Lexer
  - [x] Classificação do Token: implementar uma lógica de mapeamento de estado para classificação de token mais significativa
  - [x] Tratamento de erros: adicionar mecanismos de relatório de erros
  - [x] Palavras reservadas: implementar lookup de palavras reservadas
  - [X] Definir o DFA da linguagem: implementar as transições
  - **Semântico**:
    - [x] Corrigir a ordem das variáveis na impressão das declarações
    - [x] Ajustar linha e coluna do print_error_message do semântico
    - [x] Ver sobre a tabulação (if dentro de if, etc.)
    - [] Item (J): Verificar a necessidade de atualizar o que será utilizado em EXP_R para teste no repita
    - [] Realizar vários testes
