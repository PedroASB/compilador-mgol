import sys
from analisador.lexico.Lexer import Lexer
from analisador.lexico.SymbolTable import SymbolTable

def main():
    file_ = get_file()
    symbol_table = SymbolTable()
    mgol_lexer = Lexer(file_, symbol_table)

    print_header()
    while token := mgol_lexer.scanner():
        print_token(token)
    print('\033[1;30m=\033[m'*80)

def get_file():
    try:
        source_code_name = sys.argv[1]
        file_ = open(source_code_name, 'r', encoding="utf-8")
    except IndexError:
        print("Erro em __main__: Quantidade de argumentos incorreta.")
        print("Uso: python . <nome_do_arquivo>")
        exit(0)
    except FileNotFoundError:
        print("Erro em __main__: Arquivo não encontrado.")
        print("Uso: python . <nome_do_arquivo>")
        exit(0)
    return file_

def print_header():
    print('\033[1;30m=\033[m'*80)
    print("{:^92}".format('\033[1;34mSCANNER\033[m'))
    print('\033[1;30m=\033[m'*80)
    print("| {:^30} | {:^40} | {:^30} |".format("\033[1;30mCLASSE\033[m", "\033[1;30mLEXEMA\033[m", "\033[1;30mTIPO\033[m"))
    print("| {} | {} | {} |".format('\033[1;30m=\033[m'*20, '\033[1;30m=\033[m'*30, '\033[1;30m=\033[m'*20))

def print_token(token):
    s = token['lexeme'].split('\n')
    for i, l in enumerate(s):
        if i == 0:
            print("| {:^20} | {:^30} | {:^20} |".format(token['class'], l, token['type']))
        else:
            print("| {:^20} | \033[3m{:^30}\033[m | {:^20} |".format('', l, ''))

if __name__ == '__main__':
    main()