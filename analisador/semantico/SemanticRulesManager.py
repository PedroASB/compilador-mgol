from analisador.lexico.SymbolTable import SymbolTable
from analisador.semantico.ObjectFileManager import ObjectFileManager
from analisador.semantico.SemanticStack import SemanticStack

class SemanticRulesInvoker:
    functions = {}

    def __init__(self, symbol_table: SymbolTable, obj_file_manager: ObjectFileManager):
        self.symbol_table = symbol_table
        self.obj_file_manager = obj_file_manager
        self.stack = SemanticStack()

    def invoke_rule(production_index):
        match production_index:
            case 1:
                pass