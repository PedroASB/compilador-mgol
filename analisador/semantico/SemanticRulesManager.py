from analisador.lexico.Token import Token
from analisador.lexico.Lexer import Lexer
from analisador.semantico.ObjectFileManager import ObjectFileManager
from analisador.semantico.SemanticStack import SemanticStack
from analisador.sintatico.consts import productions

class SemanticRulesManager:

    def __init__(self, lexer: Lexer, obj_file_manager: ObjectFileManager):
        self.lexer = lexer
        self.obj_file_manager = obj_file_manager
        self.semantic_stack = SemanticStack()
        self.temporary_variable_counter = 0
        self.variable_list: list[Token] = []

    def print_stack(self):
        for item in self.semantic_stack.stack:
            print(f'Classe: {item.class_name}, Lexema: {item.lexeme}, Tipo: {item.type_name}')

    def push_token(self, token):
        self.semantic_stack.push(token)
  
    def get_type_token(self) -> Token | None:
        try:
            return [l for l in self.semantic_stack.stack if l.lexeme == 'TIPO'][-1]
        except IndexError:
            return None
    
    def set_id_type(self, lexeme: str, type_name: str):
        symbol_table = self.lexer.symbol_table
        token = symbol_table.get_token(lexeme)
        if token.type_name == 'Nulo':
            symbol_table.update_token_type(lexeme, type_name)
        else:
            self.print_error_message('Redeclaração de variável', token)

    def add_temporary_variable_to_object(self, name: str, type_name: str):
        self.obj_file_manager.add_temporary_variable(name, type_name)
    
    def new_temporary_variable(self) -> str:
        temporary_variable = 'T' + str(self.temporary_variable_counter)
        self.temporary_variable_counter += 1
        return temporary_variable

    def print_to_object(self, line):
        self.obj_file_manager.print(line)

    def invoke_rule(self, production_index):
        production = productions[production_index]
        named_tokens, tokens_list = self.semantic_stack.get_named_tokens(production.right)
        left_token = Token.tokenify(production.left, tokens_list[-1].line, tokens_list[-1].column)
        self.run_rule(production_index, named_tokens, left_token)
        self.semantic_stack.push(left_token)
    
    def print_error_message(self, error_message: str, last_production_token: Token):
        print('\033[1;31m◼\033[m' * 90)
        print("{:^100}".format('\033[31mERRO SEMÂNTICO - ' + last_production_token.get_formatted_line_and_column() + '\033[m'))
        print("{:^100}".format('\033[31;1m' + error_message + '\033[m'))
        print('\033[1;31m◼\033[m' * 90)

    def run_rule(self, production_index, tokens: dict[str, Token], left_token: Token):
        match production_index + 1:
            case 5:
                self.print_to_object('\n')

            case 6:
                for index, variable in enumerate(self.variable_list[::-1]):
                    self.print_to_object(' ' + variable.lexeme + (',' if index != len(self.variable_list) - 1 else ''))
                self.print_to_object(';\n')
                self.variable_list = []

            case 7:
                id_, L = tokens['id'], tokens['L']
                left_token.type_name = L.type_name
                self.set_id_type(id_.lexeme, left_token.type_name)
                self.variable_list.append(id_)

            case 8:
                left_token.type_name = self.get_type_token().type_name
                id_ = tokens['id']
                self.set_id_type(id_.lexeme, left_token.type_name)
                self.variable_list.append(id_)

            case 9:
                inteiro = tokens['inteiro']
                left_token.type_name = inteiro.type_name
                self.print_to_object('int')

            case 10:
                real = tokens['real']
                left_token.type_name = real.type_name
                self.print_to_object('double')

            case 11:
                literal = tokens['literal']
                left_token.type_name = literal.type_name
                self.print_to_object('string')

            case 13:
                id_ = tokens['id']
                match id_.type_name:
                    case 'literal':
                        self.print_to_object(f'scanf("%s", &{id_.lexeme});\n')
                    case 'inteiro':
                        self.print_to_object(f'scanf("%d", &{id_.lexeme});\n')
                    case 'real':
                        self.print_to_object(f'scanf("%lf", &{id_.lexeme});\n')
                    case _:
                        self.print_error_message('Variável não declarada', id_)

            case 14:
                ARG = tokens["ARG"]
                match ARG.type_name:
                    case 'literal':
                        self.print_to_object(f'printf("%s", {ARG.lexeme});\n')
                    case 'inteiro':
                        self.print_to_object(f'printf("%d", {ARG.lexeme});\n')
                    case 'real':
                        self.print_to_object(f'printf("%lf", {ARG.lexeme});\n')

            case 15:
                literal = tokens['lit']
                left_token.lexeme = literal.lexeme
                left_token.class_name = literal.class_name
                left_token.type_name = literal.type_name

            case 16:
                num = tokens['num']
                left_token.lexeme = num.lexeme
                left_token.class_name = num.class_name
                left_token.type_name = num.type_name

            case 17:
                id_ = tokens['id']
                if id_.type_name != 'Nulo':
                    left_token.lexeme = id_.lexeme
                    left_token.class_name = id_.class_name
                    left_token.type_name = id_.type_name
                else:
                    self.print_error_message('Variável não declarada', id_)

            case 19:
                id_, LD, pt_v = tokens['id'], tokens['LD'], tokens['pt_v']
                if id_.type_name != 'Nulo':
                    if id_.type_name == LD.type_name:
                        self.print_to_object(f'{id_.lexeme} = {LD.lexeme};\n')
                    else:
                        self.print_error_message('Atribuição com tipos diferentes', pt_v)
                else:
                    self.print_error_message('Variável não declarada', pt_v)

            case 20:
                OPRD, opm, OPRD_1 = tokens["OPRD"], tokens['opm'], tokens["OPRD_1"]
                if OPRD.type_name == OPRD_1.type_name != 'literal':
                    temporary_variable = self.new_temporary_variable()
                    self.add_temporary_variable_to_object(temporary_variable, OPRD.type_name)
                    left_token.lexeme = temporary_variable
                    left_token.type_name = OPRD.type_name
                    self.print_to_object(f'{temporary_variable} = {OPRD.lexeme} {opm.lexeme} {OPRD_1.lexeme};\n')
                else:
                    self.print_error_message('Operandos com tipos incompatíveis', OPRD_1)

            case 21:
                left_token.lexeme = tokens['OPRD'].lexeme
                left_token.class_name = tokens['OPRD'].class_name
                left_token.type_name = tokens['OPRD'].type_name

            case 22:
                id_ = tokens['id']
                if id_.type_name != 'Nulo':
                    left_token.lexeme = id_.lexeme
                    left_token.class_name = id_.class_name
                    left_token.type_name = id_.type_name
                else:
                    self.print_error_message('Variável não declarada', id_)

            case 23:
                num = tokens['num']
                left_token.lexeme = num.lexeme
                left_token.class_name = num.class_name
                left_token.type_name = num.type_name

            case 25:
                self.print_to_object("}\n")
            
            case 26:
                EXP_R = tokens['EXP_R']
                self.print_to_object(f"if ({EXP_R.lexeme}) " + "{\n")

            case 27:
                OPRD = tokens['OPRD']
                opr = tokens['opr']
                OPRD_1 = tokens['OPRD_1']

                if OPRD.type_name == OPRD_1.type_name:
                    temporary_variable = self.new_temporary_variable()
                    left_token.lexeme = temporary_variable
                    left_token.type_name = OPRD.type_name
                    self.add_temporary_variable_to_object(temporary_variable, OPRD.type_name)
                    self.print_to_object(f"{temporary_variable} = {OPRD.lexeme} {opr.lexeme} {OPRD_1.lexeme};\n")
                else:
                    self.print_error_message('Operandos com tipos incompatíveis', OPRD_1)

            case 33:
                self.print_to_object("}\n")

            case 34:
                EXP_R = tokens['EXP_R']
                self.print_to_object(f"while ({EXP_R.lexeme}) " + "{\n")
