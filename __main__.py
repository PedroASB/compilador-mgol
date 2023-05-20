from analisador.lexico.Lexer import Lexer
from analisador.lexico.DFAReader import DFAReader

if __name__ == '__main__':
    source_code_file = r"./source.mgol"
    dfa = DFAReader(open(r"./analisador/lexico/automaton.dfa", 'r', encoding='utf-8')).read()
    reserved_words = {"inicio", "varinicio", "varfim", "escreva", 
                      "leia", "se", "entao", "fimse", "repita", "fimrepita", "fim", "inteiro", "literal", "real"}
    mgol_lexer = Lexer(open(source_code_file, 'r', encoding="utf-8"), dfa, reserved_words)
    
    while True:
        token = mgol_lexer.scanner()
        if token:
            class_name, lexeme, type_name = token['class'], token['lexeme'], token['type']
            if class_name == "ERRO":
                print("ERRO")
            else:        
                print(f"Classe: {class_name}, Lexema: {lexeme}, Tipo: {type_name}")
        else:
            break
    
    print('Lista de Erros:')
    print(mgol_lexer.errors)