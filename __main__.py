from analisador.lexico.Lexer import Lexer
from analisador.lexico.DFAReader import DFAReader

if __name__ == '__main__':
    arquivo_codigo_fonte = r"./test.mgol"

    mgol_lexer = Lexer(
        open(arquivo_codigo_fonte, 'r', encoding="utf-8"),
        DFAReader(open(r"./analisador/lexico/automata.dfa", 'r', encoding='utf-8')).read(),
        ["inicio", "varinicio", "varfim", "escreva", "leia", "entao", "fimse", "repita", "fimrepita", "fim", "inteiro", "literal", "real"]
    )

    print('\n==================================')
    print('==================================')
    for token in mgol_lexer.get_token_stream():
        print(token[0] if token[0] != '\n' else '%NL%', ':::', token[1].name)


