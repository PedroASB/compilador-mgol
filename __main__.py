from analisador.lexico.Lexer import Lexer
from analisador.lexico.DFAReader import DFAReader

if __name__ == '__main__':
    source_code_file = r"./source.mgol"
    dfa = DFAReader(open(r"./analisador/lexico/automaton.dfa", 'r', encoding='utf-8')).read()
    reserved_words = {"inicio", "varinicio", "varfim", "escreva", 
                      "leia", "se", "entao", "fimse", "repita", "fimrepita", "fim", "inteiro", "literal", "real"}
    mgol_lexer = Lexer(open(source_code_file, 'r', encoding="utf-8"), dfa, reserved_words)
    
    print('=' * 40 + '\nSCANNER\n' + '=' * 40)

    while True:
        token = mgol_lexer.scanner()
        if token:
            if token['class'] == "ERRO":
                print("ERRO")
            else:        
                mgol_lexer.print_token(token)
        else:
            break
    
    # print('Lista de Erros:')
    # print(mgol_lexer.errors)

    print('=' * 40 + '\nTABELA DE SÍMBOLOS\n' + '=' * 40)
    for token in mgol_lexer.symbol_table:
        mgol_lexer.print_token(token)