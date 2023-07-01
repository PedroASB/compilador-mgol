import sys
from analisador.lexico.Lexer import Lexer
from analisador.lexico.SymbolTable import SymbolTable
from analisador.sintatico.ActionTable import ActionTable
from analisador.sintatico.GotoTable import GotoTable
from analisador.sintatico.Parser import Parser
from analisador.sintatico.Production import Production

def get_file():
    try:
        # MUDAR AQUI!!!
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

file_ = get_file()
symbol_table = SymbolTable()
mgol_lexer = Lexer(file_, symbol_table)
mgol_parser = Parser(mgol_lexer)

print('='*40)
print(f"{'PARSER':^40}")
print('='*40)
print(mgol_parser.parse())