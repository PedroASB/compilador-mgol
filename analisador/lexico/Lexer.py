from io import TextIOWrapper
from typing import TypeAlias
from collections.abc import Iterator
from analisador.lexico.DFA import DFA
from analisador.lexico.DFAState import DFAState

Token: TypeAlias = tuple[str, str, str]

class Lexer:
    _NEW_LINE_ = '\n'
    _EOF_ = ''
    _INVALID_ = DFAState('invalid')

    # TODO: place this out of the class
    tokens_classes_and_types = {
        "ART_OP": ("OPM", "Nulo"),
        "ASSIGN": ("RCB", "Nulo"),
        "CL_PAR": ("FC_P", "Nulo"),
        "COMMA": ("VIR", "Nulo"),
        "COMMENT_2": ("Comentário", "Nulo"),
        "EOF": ("EOF", "Nulo"),
        "ID": ("id", "Nulo"),
        "INT": ("Num", "inteiro"),
        "LIT_2": ("LIT", "literal"),
        "NL": ("Ignorar", "Nulo"),
        "OP_PAR": ("AB_P", "Nulo"),
        "REAL_3": ("Num", "real"),
        "REAL_5": ("Num", "real"),
        "REL_OP_1": ("OPR", "Nulo"),
        "REL_OP_2": ("OPR", "Nulo"),
        "REL_OP_3": ("OPR", "Nulo"),
        "S_COL": ("PT_V", "Nulo"),
        "SPACE": ("Ignorar", "Nulo"),
        "TAB": ("Ignorar", "Nulo"),
    }

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
                if self.is_in_initial_state() or self.dfa.current_state == DFAState('COMMENT_1') or self.dfa.current_state == DFAState('LIT_1'):
                    self.handle_error()
                    self.load_next_symbol_and_increment_column()
                self.go_to_initial_state()
                self.reset_buffer()

    def scanner(self) -> Token | None:
        token = next(self.token_iterator)
        return token if token[0] != "Ignorar" else None

    def append_current_symbol_to_buffer(self):
        self.buffer += self.current_symbol

    def get_formatted_line_and_column(self):
        return f"Linha: {self.line}, Coluna: {self.column}"

    def handle_error(self):
        error_message = None
        if self.current_symbol not in self.dfa.alphabet:
            error_message = "Caractere não pertence ao alfabeto da linguagem"
        if self.dfa.current_state == self.dfa.initial_state:
            error_message = "Caractere não esperado"
        if self.dfa.current_state == DFAState('COMMENT_1'):
            error_message = "Comentário não finalizado"
        if self.dfa.current_state == DFAState('LIT_1'):
            error_message = "Literal não finalizado"
            
        print('ERRO LÉXICO -', self.get_formatted_line_and_column())
        print(error_message)

    def get_current_token(self) -> Token:
        lexeme = self.buffer
        current_state = self.dfa.current_state
        try:
            class_name, type_name = Lexer.tokens_classes_and_types[current_state.name]
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