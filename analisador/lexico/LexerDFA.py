from analisador.lexico import DFAState
from analisador.lexico.DFA import DFA

class LexerDFA(DFA):
    line = 1
    column = 1
    buffer = ""

    def go_to_next_state(self, symbol: str):
        self.update_line_and_column(symbol)
        super().go_to_next_state(symbol)
        self.buffer += symbol

    def reinit(self):
        super().reinit()
        self.buffer = ""

    def get_buffer(self):
        return self.buffer
    
    def update_line_and_column(self, symbol):
        if symbol == '\n':
            self.increment_line()
            self.reset_column()
        else:
            self.increment_column()
    
    def increment_line(self):
        self.line += 1

    def increment_column(self):
        self.column += 1

    def reset_column(self):
        self.column = 1

    def get_formatted_line_and_column(self):
        return f"LINE: {self.line} COLUMN: {self.column}"
