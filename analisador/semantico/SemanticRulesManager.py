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

    def print_stack(self):
        for item in self.semantic_stack.stack:
            print(f'Classe: {item.class_name}, Lexema: {item.lexeme}, Tipo: {item.type_name}')

    def push_token(self, token):
        self.semantic_stack.push(token)

    def get_token(self, lexeme: str) -> Token:
        return self.semantic_stack.get_token(lexeme)
    
    def set_id_type(self, lexeme: str, type_name: str):
        self.lexer.symbol_table.update_token_type(lexeme, type_name)

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
        # Obtêm-se os elementos do lado direito da produção
        tokens = self.semantic_stack.get_named_tokens(production.right)
        # Cria-se o token do lado esquerdo ao qual se foi reduzido o lado direito da produção
        left_token = Token.tokenify(production.left)
        # Executa a regra semântica
        self.run_rule(production_index, tokens, left_token)
        # Empilha o token a que se foi reduzido
        self.semantic_stack.push(left_token)
    
    def print_error_message(self, error_message: str):
        print('\033[1;31m◼\033[m' * 90)
        # TODO: Ajustar linha e coluna
        print("{:^100}".format('\033[31mERRO SEMÂNTICO - ' + self.lexer.get_formatted_line_and_column() + '\033[m'))
        print("{:^100}".format('\033[31;1m' + error_message + '\033[m'))
        print('\033[1;31m◼\033[m' * 90)

    def run_rule(self, production_index, tokens: dict[str, Token], left_token: Token):
        match production_index:
            case 4:
                self.print_to_object('\n')

            case 5:
                # D → TIPO L pt_v
                # (A) Amarração de atributos, organizar a passagem de valores do atributo
                # TIPO.tipo, para L.TIPO;
                self.print_to_object(';\n')

            case 6:
                # L → id vir L
                # (B) Amarração de atributos, organizar a passagem de valores do atributo.e)
                id_, L = tokens['id'], tokens['L']
                left_token.type_name = L.type_name
                self.set_id_type(id_.lexeme, left_token.type_name)

                # TODO: Corrigir a ordem das variáveis
                self.print_to_object(f', {id_.lexeme}')
            
            case 7:
                # L → id
                # C) Ajustar o preenchimento de id.tipo na tabela de símbolos:
                # Impressão do id no .obj
                left_token.type_name = self.get_token('TIPO').type_name
                id_ = tokens['id']
                self.set_id_type(id_.lexeme, left_token.type_name)

                # TODO: Corrigir a ordem das variáveis
                self.print_to_object(f' {id_.lexeme}')

            case 8:
                inteiro = tokens['inteiro']
                left_token.type_name = inteiro.type_name
                self.print_to_object('int')

            case 9:
                real = tokens['real']
                left_token.type_name = real.type_name
                self.print_to_object('double')

            case 10:
                literal = tokens['literal']
                left_token.type_name = literal.type_name
                self.print_to_object('string')

            case 12:
                id_ = tokens['id']
                match id_.type_name:
                    case 'literal':
                        self.print_to_object(f'scanf("%s", &{id_.lexeme});\n')
                    case 'inteiro':
                        self.print_to_object(f'scanf("%d", &{id_.lexeme});\n')
                    case 'real':
                        self.print_to_object(f'scanf("%lf", &{id_.lexeme});\n')
                    case _:
                        # TODO: Substituir por uma chamada a uma função mais genérica
                        # de tratamento de erros
                        # print("Erro: Variável não declarada!", id_.get_formatted_line_and_column())
                        self.print_error_message('Variável não declarada')

                # Verificar se o campo tipo do identificador está preenchido indicando a
                # declaração do identificador (execução da regra semântica de número 6).
                # Se sim, então:
                #     Se id.tipo = literal Imprimir ( scanf(“%s”, id.lexema); )
                #     Se id.tipo = inteiro Imprimir ( scanf(“%d”, &id.lexema); )
                #     Se id.tipo = real Imprimir ( scanf(“%lf”, &id.lexema); )
                # Caso Contrário:
                # Emitir na tela “Erro: Variável não declarada”, linha e coluna onde
                # ocorreu o erro no fonte.
            
            case 13:
                # Gerar código para o comando escreva no arquivo objeto.
                # Imprimir ( printf(“ARG.lexema”); )
                ARG = tokens["ARG"]
                if ARG.type_name == 'literal':
                    self.print_to_object(f'printf({ARG.lexeme});\n')
                else:
                    self.print_to_object(f'printf("{ARG.lexeme}");\n')
            
            case 14:
                # ARG.atributos ← literal.atributos (Copiar todos os atributos de literal para os atributos de ARG).
                literal = tokens['lit']
                left_token.lexeme = literal.lexeme
                left_token.class_name = literal.class_name
                left_token.type_name = literal.type_name
                

            case 15:
                # ARG.atributos ← num.atributos (Copiar todos os atributos de literal para os atributos de ARG).
                num = tokens['num']
                left_token.lexeme = num.lexeme
                left_token.class_name = num.class_name
                left_token.type_name = num.type_name
            
            case 16:
                # Verificar se o identificador foi declarado (execução da regra semântica de número 6).
                # Se sim, então:
                #     ARG.atributos ← id.atributos (copia todos os atributos de id para os de ARG).
                # Caso Contrário:
                #     Emitir na tela “Erro: Variável não declarada” , linha e coluna onde ocorreu o erro no fonte.
                
                id_ = tokens['id']
                if id_.type_name != 'Nulo':
                    left_token.lexeme = id_.lexeme
                    left_token.class_name = id_.class_name
                    left_token.type_name = id_.type_name
                else:
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    # print("Erro: Variável não declarada!", id_.get_formatted_line_and_column())
                    self.print_error_message('Variável não declarada')

            case 18:
                # Verificar se id foi declarado (execução da regra semântica de número 6). Se sim, então:
                # |   Realizar verificação do tipo entre os operandos id e LD (ou seja,
                # |   se ambos são do mesmo tipo).
                # |   Se sim, então:
                # | |      Imprimir (id.lexema rcb.tipo LD.lexema) no arquivo objeto.
                # | Caso contrário emitir: ”Erro: Tipos diferentes para atribuição”,
                # |__________linha e coluna onde ocorreu o erro no fonte.
                # Caso contrário emitir “Erro: Variável não declarada” ”, linha e coluna onde
                # ocorreu o erro no fonte.
                id_, LD = tokens['id'], tokens['LD']
                if id_.type_name != 'Nulo':
                    if id_.type_name == LD.type_name:
                        self.print_to_object(f'{id_.lexeme} = {LD.lexeme};\n')
                    else:
                        # TODO: Substituir por uma chamada a uma função mais genérica
                        # de tratamento de erros
                        # print("Erro: Atribuição com tipos diferentes!", id_.get_formatted_line_and_column())
                        self.print_error_message('Atribuição com tipos diferentes')
                else:
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    # print("Erro: Variável não declarada!", id_.get_formatted_line_and_column())
                    self.print_error_message('Variável não declarada')

            case 19:
                # Verificar se tipo dos operandos de de LD são equivalentes e diferentes de literal.
                # Se sim, então:
                #     Gerar uma variável numérica temporária Tx, em que x é um número gerado sequencialmente.
                #     LD.lexema ← Tx
                #     Imprimir (Tx = OPRD.lexema opm.tipo OPRD.lexema) no arquivo objeto.
                # Caso contrário emitir “Erro: Operandos com tipos incompatíveis” ”, linha e coluna onde ocorreu o erro no fonte.

                OPRD, opm, OPRD_1 = tokens["OPRD"], tokens['opm'], tokens["OPRD_1"]
                if OPRD.type_name == OPRD_1.type_name != 'literal':
                    temporary_variable = self.new_temporary_variable()
                    self.add_temporary_variable_to_object(temporary_variable, OPRD.type_name)
                    left_token.lexeme = temporary_variable
                    left_token.type_name = OPRD.type_name
                    self.print_to_object(f'{temporary_variable} = {OPRD.lexeme} {opm.lexeme} {OPRD_1.lexeme};\n')
                else:
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    # print("Erro: Operandos com tipos incompatíveis!", OPRD_1.get_formatted_line_and_column())
                    self.print_error_message('Operandos com tipos incompatíveis')
            
            case 20:
                # LD.atributos ← OPRD.atributos (Copiar todos os atributos de OPRD para os atributos de LD).
                left_token.lexeme = tokens['OPRD'].lexeme
                left_token.class_name = tokens['OPRD'].class_name
                left_token.type_name = tokens['OPRD'].type_name
            
            case 21:
                # Verificar se o identificador está declarado.
                #     Se sim, então:
                #         OPRD.atributos ← id.atributos
                #     Caso contrário emitir “Erro: Variável não declarada” ”, linha e coluna onde ocorreu o erro no fonte.
                id_ = tokens['id']
                
                if id_.type_name != 'Nulo':
                    left_token.lexeme = id_.lexeme
                    left_token.class_name = id_.class_name
                    left_token.type_name = id_.type_name
                else:
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    # print("Erro: Variável não declarada!", id_.get_formatted_line_and_column())
                    self.print_error_message('Variável não declarada')
            
            case 22:
                # OPRD.atributos ← num.atributos (Copiar todos os atributos de num para os atributos de OPRD).
                num = tokens['num']
                left_token.lexeme = num.lexeme
                left_token.class_name = num.class_name
                left_token.type_name = num.type_name
            
            case 24:
                # Imprimir ( } ) no arquivo objeto.
                self.print_to_object("}\n")
            
            case 25:
                # Imprimir ( if (EXP_R.lexema) { ) no arquivo objeto.
                EXP_R = tokens['EXP_R']
                self.print_to_object(f"if ({EXP_R.lexeme}) " + "{\n")
            
            case 26:
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
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    # print("Erro: Operandos com tipos incompatíveis!", OPRD_1.get_formatted_line_and_column())
                    self.print_error_message('Operandos com tipos incompatíveis')
                    
                #
                # Verificar se os tipos de dados de OPRD são iguais ou equivalentes para a realização de comparação relacional.
                # Se sim, então:
                #     Gerar uma variável booleana temporária Tx, em que x é um número gerado sequencialmente.
                #     EXP_R.lexema ← Tx
                #     Imprimir (Tx = OPRD.lexema opr.tipo OPRD.lexema) no arquivo objeto.
                # Caso contrário emitir “Erro: Operandos com tipos incompatíveis” ”, linha e coluna onde ocorreu o erro no fonte.
                #
            
            case 31:
                # A → R A
                # (D) Verificar as necessidades e gerar as regras semânticas e de tradução.
                # TODO: Remover caso (Aparentemente não há nenhuma regra semântica a ser executada)
                pass
            
            case 32:
                # R → CABR CPR
                # (E) Verificar as necessidades e gerar as regras semânticas e de tradução.
                self.print_to_object("}\n")
            
            case 33:
                # CABR → repita ab_p EXP_R fc_p 
                # (F) Verificar as necessidades e gerar as regras semânticas e de tradução.
                EXP_R = tokens['EXP_R']
                self.print_to_object(f"while ({EXP_R.lexeme}) " + "{\n")
            
            case 34:
                # CPR → ES CPR
                # (G) Verificar as necessidades e gerar as regras semânticas e de tradução.
                # TODO: Remover caso (Aparentemente não há nenhuma regra semântica a ser executada)
                pass
            
            case 35:
                # CPR → CMD CPR
                # (H) Verificar as necessidades e gerar as regras semânticas e de tradução.
                # TODO: Remover caso (Aparentemente não há nenhuma regra semântica a ser executada)
                pass
            
            case 36:
                # CPR → COND CPR
                # (I) Verificar as necessidades e gerar as regras semânticas e de tradução.
                # TODO: Remover caso (Aparentemente não há nenhuma regra semântica a ser executada)
                pass
            
            case 37:
                # CPR → fimrepita
                # (J) Verificar a necessidade de atualizar o que será utilizado em EXP_R para teste no repita;
                # verificar a necessidade de gerar outras regras semânticas e de tradução além desta.

                # TODO: Ver sobre "(J) Verificar a necessidade de atualizar o que será utilizado em EXP_R para teste no repita"
                pass
