from collections.abc import Iterator
from io import TextIOWrapper
from analisador.lexico.DFAState import DFAState
from analisador.lexico.consts import state_token_type_map, reserved_words
from analisador.lexico.DFAReader import DFAReader
from analisador.lexico.types import Token
from analisador.lexico.SymbolTable import SymbolTable

class Lexer:
    _NEW_LINE_ = '\n'
    _EOF_ = ''
    _INVALID_ = DFAState('invalid')

    def __init__(self, source_file: TextIOWrapper, symbol_table: SymbolTable):
        self.dfa = DFAReader(open(r"./analisador/lexico/automaton.dfa", 'r', encoding='utf-8')).read()
        self.line = 1
        self.column = 1
        self.buffer = ""
        self.current_symbol = None
        self.input_reader = source_file
        self.is_finished = False
        self.symbol_table = symbol_table
        self.errors: list[str] = []
        self.initialize_symbol_table()
        self.input_reader.seek(0)
        self.load_next_symbol_and_increment_column()
        self.token_iterator = self.get_token_iterator()

    def __del__(self):
        if self.input_reader:
            self.input_reader.close()

    def initialize_symbol_table(self):
        for reserved_word in reserved_words:
            self.symbol_table.insert_token({'class': reserved_word, 
                                            'lexeme': reserved_word, 
                                            'type': reserved_word})

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
                        yield self.get_and_classify_current_token()
                        self.finish()
                self.load_next_symbol_and_increment_column()
            else:
                if self.is_in_initial_state():
                    self.append_current_symbol_to_buffer()

                yield self.get_and_classify_current_token()

                if self.is_in_initial_state() or \
                    self.is_in_incomplete_comment_state() or \
                    self.is_in_incomplete_literal_state():

                    self.handle_error()
                    self.load_next_symbol_and_increment_column()
                
                elif self.is_in_non_accept_state():
                    self.handle_error()

                self.go_to_initial_state()
                self.reset_buffer()

    def scanner(self) -> Token | None:
        try:
            token = next(self.token_iterator)
            while token['class'] in {"Ignorar", "Comentário"}:
                token = next(self.token_iterator)
            if token['class'] == 'id':
                if not self.symbol_table.has_token(token):
                    self.symbol_table.insert_token(token)
                return self.symbol_table.get_token(token['lexeme'])
            else:
                return token
        except StopIteration:
            return None

    def append_current_symbol_to_buffer(self):
        self.buffer += self.current_symbol

    def get_formatted_line_and_column(self):
        return f"Linha: {self.line}, Coluna: {self.column}"

    def handle_error(self):
        if self.current_symbol not in self.dfa.alphabet and self.is_in_initial_state():
            error_message = "Caractere não pertence ao alfabeto da linguagem"
        elif self.is_in_incomplete_comment_state():
            error_message = "Comentário não finalizado"
        elif self.is_in_incomplete_literal_state():
            error_message = "Literal não finalizado"
        elif self.is_in_initial_state() or self.is_in_non_accept_state():
            error_message = "Caractere não esperado"
        
        error = 'ERRO LÉXICO - ' + error_message + ' - ' + self.get_formatted_line_and_column()
        self.errors.append(error)
        print('\033[31m-\033[m' * 80)
        print("{:^85}".format('\033[31mERRO LÉXICO - ' + self.get_formatted_line_and_column()))
        print("{:^90}".format('\033[1;31m' + error_message + '.\033[m'))
        print('\033[31m-\033[m' * 80)


    def get_and_classify_current_token(self) -> Token:
        lexeme = self.buffer
        current_state = self.dfa.current_state
        try:
            class_name, type_name = state_token_type_map[current_state.name]
            if class_name == "id" and lexeme in reserved_words:
                class_name, type_name = lexeme, lexeme
            elif class_name == "EOF":
                lexeme = "EOF"
        except KeyError:
            class_name, type_name = ("ERRO", "Nulo")
        return {'class': class_name, 'lexeme': lexeme, 'type': type_name}
    
    def print_token(self, token: Token):
        print(f"Classe: {token['class']}, Lexema: {token['lexeme']}, Tipo: {token['type']}")
    
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
    
    def is_in_non_accept_state(self):
        return self.dfa.current_state not in self.dfa.accept_states
    
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
