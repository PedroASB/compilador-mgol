from io import TextIOWrapper
from collections.abc import Iterator
from analisador.lexico.DFA import DFA
from analisador.lexico.DFAState import DFAState

class Lexer:
    _NEW_LINE_ = '\n'
    _EOF_ = ''
    _INVALID_ = DFAState('invalid')

    def __init__(self, input_reader: TextIOWrapper, dfa: DFA, reserved_words: list[str]):
        self.dfa = dfa
        self.reserved_words = reserved_words
        self.line = 1
        self.column = 1
        self.buffer = ""
        self.current_symbol = None
        self.input_reader = input_reader
        self.is_finished = False

        self.input_reader.seek(0)
        self.load_next_symbol_and_increment_column()
        self.token_iterator = self.get_token_iterator()

    def load_next_symbol_and_increment_column(self):
        self.increment_column()
        self.current_symbol = self.input_reader.read(1)
    
    def get_token_iterator(self) -> Iterator[tuple]:
        while not self.is_finished:
            next_state = self.get_next_state()

            if next_state != Lexer._INVALID_:
                self.go_to_next_state()
                self.append_current_symbol_to_buffer()
                match self.current_symbol:
                    case Lexer._NEW_LINE_:
                        self.increment_line()
                        self.reset_column()
                    case Lexer._EOF_:
                        yield self.get_current_token()
                        self.finish()
                self.load_next_symbol_and_increment_column()
            else:
                if not self.buffer_is_empty():
                    yield self.get_current_token()
                if self.is_in_initial_state():
                    self.handle_error()
                    self.load_next_symbol_and_increment_column()
                self.go_to_initial_state()
                self.reset_buffer()

    def scanner(self) -> tuple:
        return next(self.token_iterator)

    def append_current_symbol_to_buffer(self):
        self.buffer += self.current_symbol

    def get_formatted_line_and_column(self):
        return f"LINE: {self.line} COLUMN: {self.column}"

    def handle_error(self):
        print('ERROR! ', self.get_formatted_line_and_column())

    def get_current_token(self):
        token = self.buffer
        current_state = self.dfa.current_state
        # TODO: Map state to token classification
        return (token, current_state)
    
    def buffer_is_empty(self):
        return self.buffer == ""
    
    def get_next_state(self):
        return self.dfa.get_next_state(self.current_symbol)
    
    def go_to_next_state(self):
        self.dfa.go_to_next_state(self.current_symbol)
    
    def go_to_initial_state(self):
        self.dfa.go_to_initial_state()

    def is_in_initial_state(self):
        return self.dfa.is_in_initial_state()
        
    def increment_line(self):
        self.line += 1

    def increment_column(self):
        self.column += 1

    def reset_column(self):
        self.column = 1

    def reset_buffer(self):
        self.buffer = ""

    def finish(self):
        self.is_finished = True