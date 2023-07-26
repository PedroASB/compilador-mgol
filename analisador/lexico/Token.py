class Token:
    def __init__(self, lexeme, class_name, type_name, line, column):
        self.lexeme = lexeme
        self.class_name = class_name
        self.type_name = type_name
        self.line = line
        self.column = column
    
    @staticmethod
    def tokenify(lexeme):
        return Token(lexeme, lexeme, lexeme, -1, -1)
    
    def get_formatted_line_and_column(self):
        return f"Linha: {self.line}, Coluna: {self.column}"
    
    def __str__(self):
        return f"Token(lexema={self.lexeme}, classe={self.class_name}, tipo={self.type_name})"
    
    def __repr__(self):
        return f"Token(lexema={self.lexeme}, classe={self.class_name}, tipo={self.type_name})"