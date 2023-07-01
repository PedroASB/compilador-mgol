from analisador.lexico.Lexer import Lexer
from analisador.lexico.Token import Token
from analisador.sintatico.GotoTable import GotoTable
from analisador.sintatico.ActionTable import ActionTable
from analisador.sintatico.ParserStack import ParserStack
from analisador.sintatico.consts import productions

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer: Lexer = lexer
        self.productions = productions
        self.tokens_queue = []
        self.action_table = ActionTable(r"./analisador/sintatico/tables/action.csv")
        self.goto_table = GotoTable(r"./analisador/sintatico/tables/goto.csv")

    def get_next_token(self):
        return self.lexer.scanner() if len(self.tokens_queue) == 0 else self.tokens_queue.pop(0)

    def parse(self):
        stack = ParserStack()
        current_token = self.get_next_token()
        current_state = stack.get()
        error_flag = False
        while True:
            action = self.action_table.get_action(current_state, current_token.class_name)
            match action:
                case ('s', next_state):
                    stack.push(next_state)
                    current_token = self.get_next_token()
                    current_state = stack.get()
                case ('r', reduce_production):
                    production = self.productions[reduce_production]
                    stack.pop(production.cardinality)
                    goto_state = self.goto_table.get_goto(stack.get(), production.left)
                    stack.push(goto_state)
                    print(production.left, '->', ' '.join(production.right))
                    current_state = stack.get()
                case ('a', _):
                    return not error_flag
                case ('e', _):
                    error_flag = True
                    print(f"{current_token.get_formatted_line_and_column()} ERRO! | Estado {current_state} | Esperado: {', '.join(self.get_expected_tokens_at_state(current_state))} | Recebido: {current_token.class_name}")
                    if not self.recover_from_wrong_token(current_state, [Token.tokenify(tkn) for tkn in self.get_expected_tokens_at_state(current_state)], stack):
                        print("Não foi possível aplicar REC_WRG_TKN")
                        if not self.recover_from_excessive_token(current_state):
                            print("Não foi possível aplicar REC_EXC_TKN")
                            if not self.recover_from_missing_token(current_state, [Token.tokenify(tkn) for tkn in self.get_expected_tokens_at_state(current_state)], current_token, stack):
                                print("Não foi possível aplicar REC_MSN_TKN")
                                if not self.recover_panic(current_state):
                                    print("Não foi possível aplicar PANIC")
                                    return False
                    current_token = self.get_next_token()
                    current_state = stack.get()
    
    def get_expected_tokens_at_state(self, state: int):
        return [action[0] for action in self.action_table.get_actions_for_state(state) if action[1][0] != 'e']

    def consume_tokens_until(self, token: Token):
        read_token = None
        while (read_token := self.get_next_token()) is not None and read_token.class_name != token.class_name:
            pass
        return read_token is not None
    
    def recover_panic(self, current_state):
        print("APLICANDO PANIC")
        read_token = None
        while read_token := self.get_next_token():
            print(f"CONSUMIDO: {read_token.class_name}")
            if not read_token:
                return False
            if self.token_fits_state(read_token, current_state):
                self.tokens_queue = [read_token, *self.tokens_queue]
                return True

    def token_fits_state(self, token, state):
        action_on_token = self.action_table.get_action(state, token.class_name)
        match action_on_token:
            case ('s', _) | ('r', _):
                return True
            case _:
                return False
            
    def recover_from_wrong_token(self, current_state, possible_tokens, stack):
        print("APLICANDO REC_WRG_TKN")
        next_token = self.get_next_token()
        if next_token is None:
            return False
        if possible_token := self.any_of_possible_tokens_fits_next_token(current_state, possible_tokens, next_token, stack):
            self.tokens_queue = [possible_token, next_token, *self.tokens_queue]
            return True
        self.tokens_queue = [next_token, *self.tokens_queue]
        return False

            
    def recover_from_excessive_token(self, current_state):
        print("APLICANDO EXC_TKN")
        next_token = self.get_next_token()
        if next_token is None:
            return False
        self.tokens_queue = [next_token, *self.tokens_queue]
        return self.token_fits_state(next_token, current_state)

    def recover_from_missing_token(self, current_state, possible_missing_tokens, current_token: Token, stack: ParserStack):
        print("APLICANDO MSN_TKN")
        # Estratégia: se só existe um token possível, insira-o sem qualquer verificação e prossiga com a análise.
        # Se existem múltiplos tokens, teste se a inserção de algum deles faz sentido considerando o token subsequente.
        # Se essa inserção fizer sentido, realize a inserção e prossiga a análise.
        # Se nenhuma inserção fizer sentido, ative o modo pânico.
        if len(possible_missing_tokens) == 1:
            self.tokens_queue = [possible_missing_tokens[0], current_token, *self.tokens_queue]
            return True
        missing_token = self.any_of_possible_tokens_fits_next_token(current_state, possible_missing_tokens, current_token, stack)
        if not missing_token:
            return False
        self.tokens_queue = [missing_token, current_token, *self.tokens_queue]
        return True

    def possible_token_fits_next_token(self, current_state: int, possible_token: Token, next_token: Token, stack: ParserStack):
        new_state_on_possible_token = None
        last_simulated_state = None
        current_simulated_state = current_state
        while True:
            if current_simulated_state == last_simulated_state:
                # Loop detectado
                return False
            action_given_possible_token = self.action_table.get_action(current_simulated_state, possible_token.class_name)
            match action_given_possible_token:
                case ('s', next_state):
                    new_state_on_possible_token = next_state
                    break
                case ('r', reduce_production):
                    production = self.productions[reduce_production]
                    last_simulated_state = current_simulated_state
                    current_simulated_state = self.goto_table.get_goto(stack.stack[-production.cardinality-1], production.left) # Simula a exclusão de |production| estados da pilha e pega o que ficar no topo 
                case ('a', _):
                    return True
                case ('e', _):
                    return False
        action_on_next_token = self.action_table.get_action(new_state_on_possible_token, next_token.class_name)
        match action_on_next_token:
            case ('s', _) | ('r', _):
                return True
            case ('e', _):
                return False

    def any_of_possible_tokens_fits_next_token(self, current_state: int, possible_tokens, next_token, stack: ParserStack):
        for possible_token in possible_tokens:
            if self.possible_token_fits_next_token(current_state, possible_token, next_token, stack):
                return possible_token
        return None
