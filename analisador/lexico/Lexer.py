from io import TextIOWrapper
from typing import TypeAlias
from collections.abc import Iterator
from analisador.lexico.DFA import DFA
from analisador.lexico.DFAState import DFAState
from analisador.lexico.consts import state_token_type_map

Token: TypeAlias = tuple[str, str, str]

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
        self.symbol_table: list[Token] = []
        self.errors: list[str] = []

        self.input_reader.seek(0)
        self.load_next_symbol_and_increment_column()
        self.token_iterator = self.get_token_iterator()

    def load_next_symbol_and_increment_column(self):
        self.increment_column()
        self.current_symbol = self.input_reader.read(1)
    
    def get_token_iterator(self) -> Iterator[Token]:
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
                
                if self.is_in_initial_state() or \
                    self.is_in_incomplete_comment_state() or \
                    self.is_in_incomplete_literal_state():

                    self.handle_error()
                    self.load_next_symbol_and_increment_column()

                self.go_to_initial_state()
                self.reset_buffer()

    def scanner(self) -> Token | None:
        try:
            token = next(self.token_iterator)
            while token[0] == "Ignorar":
                token = next(self.token_iterator)
            return token
        except StopIteration:
            return None

    def append_current_symbol_to_buffer(self):
        self.buffer += self.current_symbol

    def get_formatted_line_and_column(self):
        return f"Linha: {self.line}, Coluna: {self.column}"

    def handle_error(self):
        if self.current_symbol not in self.dfa.alphabet:
            error_message = "Caractere não pertence ao alfabeto da linguagem"
        if self.is_in_initial_state():
            error_message = "Caractere não esperado"
        if self.is_in_incomplete_comment_state():
            error_message = "Comentário não finalizado"
        if self.is_in_incomplete_literal_state():
            error_message = "Literal não finalizado"
            
        self.errors.append('ERRO LÉXICO - ' + error_message + ' - ' + self.get_formatted_line_and_column())

    def get_current_token(self) -> Token:
        lexeme = self.buffer
        current_state = self.dfa.current_state
        try:
            class_name, type_name = state_token_type_map[current_state.name]
        except KeyError:
            class_name, type_name = ("ERRO", "Nulo")
        # TODO: Map state to token classification
        return (class_name, lexeme, type_name)
    
    def buffer_is_empty(self):
        return self.buffer == ""
    
    def get_next_state(self):
        return self.dfa.get_next_state(self.current_symbol)

    def get_current_state(self):
        return self.dfa.current_state
    
    def go_to_next_state(self):
        self.dfa.go_to_next_state(self.current_symbol)
    
    def go_to_initial_state(self):
        self.dfa.go_to_initial_state()

    def is_in_initial_state(self):
        return self.dfa.is_in_initial_state()
    
    def is_in_incomplete_comment_state(self):
        return self.dfa.current_state == DFAState('COMMENT_1')
    
    def is_in_incomplete_literal_state(self):
        return self.dfa.current_state == DFAState('LIT_1')
        
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