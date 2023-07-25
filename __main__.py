import sys
from analisador.lexico.Lexer import Lexer
from analisador.lexico.SymbolTable import SymbolTable
from analisador.semantico.ObjectFileManager import ObjectFileManager
from analisador.sintatico.ActionTable import ActionTable
from analisador.sintatico.GotoTable import GotoTable
from analisador.sintatico.Parser import Parser
from analisador.sintatico.Production import Production

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

file_ = get_file()
symbol_table = SymbolTable()
obj_file_manager = ObjectFileManager()
mgol_lexer = Lexer(file_, symbol_table)
mgol_parser = Parser(mgol_lexer, obj_file_manager)

print('\033[1m='*90)
print(f"{'PARSER':^90}")
print('\033[1m=\033[m'*90)
if mgol_parser.parse():
    obj_file_manager.generate_final()
