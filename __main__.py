from analisador.lexico.Lexer import Lexer
from analisador.lexico.DFAReader import DFAReader

if __name__ == '__main__':
    arquivo_codigo_fonte = r"./test.mgol"

    mgol_lexer = Lexer(
        open(arquivo_codigo_fonte, 'r', encoding="utf-8"),
        DFAReader(open(r"./analisador/lexico/automaton.dfa", 'r', encoding='utf-8')).read(),
        ["inicio", "varinicio", "varfim", "escreva", "leia", "se", "entao", "fimse", "repita", "fimrepita", "fim", "inteiro", "literal", "real"]
    )

    print('\n==================================')
    print('==================================')

    while True:
        token = mgol_lexer.scanner()
        if token:
            class_name, lexeme, type_name = token[0], token[1], token[2]
            if class_name == "ERRO":
                print("ERRO")
            else:        
                print(f"Classe: {class_name}, Lexema: {lexeme}, Tipo: {type_name}")
        else:
            break
    
    print('Lista de Erros:')
    print(mgol_lexer.errors)
