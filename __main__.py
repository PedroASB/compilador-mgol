from analisador.lexico.Lexer import Lexer
from analisador.lexico.DFAReader import DFAReader

if __name__ == '__main__':
    arquivo_codigo_fonte = r"./test.mgol"

    mgol_lexer = Lexer(
        open(arquivo_codigo_fonte, 'r', encoding="utf-8"),
        DFAReader(open(r"./analisador/lexico/automaton.dfa", 'r', encoding='utf-8')).read(),
        ["inicio", "varinicio", "varfim", "escreva", "leia", "entao", "fimse", "repita", "fimrepita", "fim", "inteiro", "literal", "real"]
    )

    print('\n==================================')
    print('==================================')

    try:
        while True:
            token = mgol_lexer.scanner()
            if token:
                print(f"Classe: {token[0]}, Lexema: {token[1]}, Tipo: {token[2]}")
    except StopIteration:
        print('=== END ===')
