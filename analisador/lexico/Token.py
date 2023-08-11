from analisador.sintatico.consts import friendly_names

class Token:
    def __init__(self, lexeme, class_name, type_name, line, column):
        self.lexeme = lexeme
        self.class_name = class_name
        self.type_name = type_name
        self.line = line
        self.column = column
        self.generic_info = {}
    
    @staticmethod
    def tokenify(lexeme, line = -1, column = -1):
        return Token(lexeme, lexeme, lexeme, line, column)
    
    def get_formatted_line_and_column(self):
        return f"Linha: {self.line}, Coluna: {self.column}"
    
    def get_friendly_name(self):
        try:
            return friendly_names[self.class_name.upper()]
        except KeyError:
            return self.class_name
    
    def __str__(self):
        return f"Token(lexema={self.lexeme}, classe={self.class_name}, tipo={self.type_name})"
    
    def __repr__(self):
        return f"Token(lexema={self.lexeme}, classe={self.class_name}, tipo={self.type_name})"