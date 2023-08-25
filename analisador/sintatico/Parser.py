from analisador.lexico.Lexer import Lexer
from analisador.lexico.Token import Token
from analisador.sintatico.GotoTable import GotoTable
from analisador.sintatico.ActionTable import ActionTable
from analisador.sintatico.ParserStack import ParserStack
from analisador.semantico.ObjectFileManager import ObjectFileManager
from analisador.semantico.SemanticRulesManager import SemanticRulesManager
from analisador.sintatico.consts import productions

class Parser:
    def __init__(self, lexer: Lexer, object_file_manager: ObjectFileManager):
        self.lexer = lexer
        self.semantic_rules_manager = SemanticRulesManager(lexer, object_file_manager)
        self.object_file_manager = object_file_manager
        self.productions = productions
        self.tokens_queue = []
        self.action_table = ActionTable(r"./analisador/sintatico/tables/action.csv")
        self.goto_table = GotoTable(r"./analisador/sintatico/tables/goto.csv")
        self.error_flag = False

    def get_next_token(self):
        return self.lexer.scanner() if len(self.tokens_queue) == 0 else self.tokens_queue.pop(0)

    def parse(self):
        stack = ParserStack()
        current_token = self.get_next_token()
        current_state = stack.get()
        while True:
            action = self.action_table.get_action(current_state, current_token.class_name)
            match action:
                case ('s', next_state):
                    stack.push(next_state)
                    self.semantic_rules_manager.push_token(current_token)
                    current_token = self.get_next_token()
                    current_state = stack.get()
                case ('r', reduce_production):
                    production = self.productions[reduce_production]
                    stack.pop(production.cardinality)
                    goto_state = self.goto_table.get_goto(stack.get(), production.left)
                    stack.push(goto_state)
                    print(reduce_production, production)
                    self.semantic_rules_manager.invoke_rule(reduce_production)
                    current_state = stack.get()
                case ('a', _):
                    some_error = self.lexer.error_flag or self.semantic_rules_manager.error_flag or self.error_flag
                    if not some_error:
                        self.object_file_manager.generate_final()
                        return True
                    return False
                case ('e', _):
                    self.error_flag = True
                    error_line_and_column: str = self.lexer.get_formatted_line_and_column()
                    possible_tokens = [Token.tokenify(token, self.lexer.line, self.lexer.column) for token in self.get_expected_tokens_at_state(current_state)]
                    
                    recovery_method, recovery_token = None, None
                    if recovery_token := self.recover_from_wrong_token(current_state, possible_tokens, stack):
                        recovery_method = "wrong_token"
                    elif self.recover_from_excessive_token(current_state):
                        recovery_method = "excessive_token"
                    elif recovery_token := self.recover_from_missing_token(current_state, possible_tokens, current_token, stack):
                        recovery_method = "missing_token"
                    elif self.recover_panic(current_state):
                        recovery_method = "panic"

                    self.print_error_message(current_token, possible_tokens, recovery_method, recovery_token, error_line_and_column)
                    if recovery_method is None:
                        return False
                    
                    current_token = self.get_next_token()
                    current_state = stack.get()
    
    def get_expected_tokens_at_state(self, state: int):
        return [action[0] for action in self.action_table.get_actions_for_state(state) if action[1][0] != 'e']

    def recover_panic(self, current_state):
        read_token = None
        while read_token := self.get_next_token():
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
        next_token = self.get_next_token()
        if next_token is None:
            return False
        if possible_token := self.any_of_possible_tokens_fits_next_token(current_state, possible_tokens, next_token, stack):
            self.tokens_queue = [possible_token, next_token, *self.tokens_queue]
            return possible_token
        self.tokens_queue = [next_token, *self.tokens_queue]
        return False

    def recover_from_excessive_token(self, current_state):
        next_token = self.get_next_token()
        if next_token is None:
            return False
        self.tokens_queue = [next_token, *self.tokens_queue]
        return self.token_fits_state(next_token, current_state)

    def recover_from_missing_token(self, current_state, possible_missing_tokens, current_token: Token, stack: ParserStack):
        missing_token = self.any_of_possible_tokens_fits_next_token(current_state, possible_missing_tokens, current_token, stack)
        if not missing_token:
            return False
        self.tokens_queue = [missing_token, current_token, *self.tokens_queue]
        return missing_token

    def possible_token_fits_next_token(self, current_state: int, possible_token: Token, next_token: Token, stack: ParserStack):
        new_state_on_possible_token = None
        last_simulated_state = None
        current_simulated_state = current_state
        while True:
            if current_simulated_state == last_simulated_state:
                return False
            action_given_possible_token = self.action_table.get_action(current_simulated_state, possible_token.class_name)
            match action_given_possible_token:
                case ('s', next_state):
                    new_state_on_possible_token = next_state
                    break
                case ('r', reduce_production):
                    production = self.productions[reduce_production]
                    last_simulated_state = current_simulated_state
                    current_simulated_state = self.goto_table.get_goto(stack.stack[-production.cardinality-1], production.left)
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
    
    def print_error_message(self, current_token: Token, possible_tokens: list[Token], 
                            recovery_method: str, recovery_token: Token, formatted_line_and_column: str):
        self.error_flag = True
        print('\033[0;31m▦\033[m' * 90)
        print("{:^100}".format('\033[31;1mERRO SINTÁTICO\033[0;31m - ' + formatted_line_and_column + '\033[m\n'))
        if len(possible_tokens) <= 1:
            print("{:^100}".format('\033[1;31m' + 'Esperado: \033[0m\033[3;31m' + possible_tokens[0].get_friendly_name() + '\033[m'))
        else:
            print("{:^140}".format('\033[1;31m' + 'Esperado: \033[0m\033[3;31m' + ', '.join([token.get_friendly_name() for token in possible_tokens][:-1]) + ' \033[m\033[1;31m\033[4;31mou\033[3;31m\033[0;31m\033[3;31m ' + possible_tokens[-1].get_friendly_name() + '\033[m'))
            
        print("{:^100}".format('\033[1;31m' + 'Recebido: \033[0m\033[3;31m' + current_token.get_friendly_name() + '\033[m\n'))
        match recovery_method:
            case 'wrong_token':
                print("{:^110}".format(f"\033[1;32mErro recuperado a nível de frase\033[0;32m - Substituição de '{current_token.get_friendly_name()}' por '{recovery_token.get_friendly_name()}'\033[m"))
            case 'excessive_token':
                print("{:^110}".format(f"\033[1;32mErro recuperado a nível de frase\033[0;32m - Deleção de '{current_token.get_friendly_name()}'\033[m"))
            case 'missing_token':
                print("{:^110}".format(f"\033[1;32mErro recuperado a nível de frase\033[0;32m - Inserção de '{recovery_token.get_friendly_name()}'\033[m"))
            case 'panic':
                print("{:^110}".format("\033[1;32mErro recuperado pelo modo pânico\033[m"))
            case None:
                print("{:^110}".format("\033[1;31mNão foi possível recuperar o erro\033[m"))
        print('\033[0;31m▦\033[m' * 90)
        