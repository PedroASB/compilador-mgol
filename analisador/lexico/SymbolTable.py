from analisador.lexico.types import Token

class SymbolTable:
    def __init__(self):
        self.table: list[Token] = []

    def get_token(self, lexeme: str) -> Token | None:
        return [l for l in self.table if l['lexeme'] == lexeme][0]
    
    def insert_token(self, token: Token):
        self.table.append(token)

    def has_token(self, token) -> bool:
        return token in self.table

    def update_token(self, lexeme: str):
        pass
    
