from analisador.lexico.Lexer import Lexer
from analisador.lexico.SymbolTable import SymbolTable

if __name__ == '__main__':
    source_code_name = r"./source.mgol"
    symbol_table = SymbolTable()
    mgol_lexer = Lexer(source_code_name, symbol_table)

    print('=' * 40 + '\nSCANNER\n' + '=' * 40)

    while True:
        token = mgol_lexer.scanner()
        if token:
            mgol_lexer.print_token(token)
        else:
            break
    
    # print('=' * 40 + '\nTABELA DE SÍMBOLOS\n' + '=' * 40)
    # for token in mgol_lexer.symbol_table.table:
    #     mgol_lexer.print_token(token)