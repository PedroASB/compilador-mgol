from io import TextIOWrapper
from analisador.lexico.DFA import DFA
from analisador.lexico.DFAState import DFAState

class Lexer:
    _NEW_LINE_ = '\n'
    _EOF_ = ''
    _ERROR_STATE_ = DFAState('ERROR')

    def __init__(self, input_reader: TextIOWrapper, dfa: DFA, reserved_words: list[str]):
        self.dfa = dfa
        self.reserved_words = reserved_words
        self.line = 1
        self.column = 1
        self.buffer = ""
        self.current_symbol = None
        self.input_reader = input_reader
        self.is_finished = False

    def load_next_symbol(self):
        self.increment_column()
        self.current_symbol = self.input_reader.read(1)

    def print_current_state(self):
        print(f"""
            current_symbol: {self.current_symbol}
            state: {self.dfa.current_state.name}
            initial_state? {self.dfa.is_in_initial_state()}
            next_state: {self.get_next_state().name}
        """)
    
    def get_token_stream(self):
        self.is_finished = False
        self.input_reader.seek(0)
        self.load_next_symbol()

        while not self.is_finished:
            next_state = self.get_next_state()

            if next_state == Lexer._ERROR_STATE_:
                yield self.get_current_token()
                if self.is_in_initial_state():
                    self.handle_error()
                    self.load_next_symbol()
                self.go_to_initial_state()
                self.reset_buffer()
            else:
                self.dfa.go_to_next_state(self.current_symbol)
                self.append_current_symbol_to_buffer()

                match self.current_symbol:
                    case Lexer._NEW_LINE_:
                        self.increment_line()
                        self.reset_column()
                    case Lexer._EOF_:
                        self.finish() # ou seria melhor um simples break?
                
                self.load_next_symbol()

        yield self.get_current_token()

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