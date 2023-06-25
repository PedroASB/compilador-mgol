class Token:
    def __init__(self, lexeme, class_name, type_name, line, column):
        self.lexeme = lexeme
        self.class_name = class_name
        self.type_name = type_name
        self.line = line
        self.column = column
    
    def get_formatted_line_and_column(self):
        return f"Linha: {self.line}, Coluna: {self.column}"