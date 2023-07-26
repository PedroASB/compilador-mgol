from analisador.lexico.Token import Token
from analisador.lexico.SymbolTable import SymbolTable
from analisador.semantico.ObjectFileManager import ObjectFileManager
from analisador.semantico.SemanticStack import SemanticStack
from analisador.sintatico.consts import productions

class SemanticRulesManager:

    def __init__(self, symbol_table: SymbolTable, obj_file_manager: ObjectFileManager):
        self.symbol_table = symbol_table
        self.obj_file_manager = obj_file_manager
        self.semantic_stack = SemanticStack()
        self.temporary_variable_counter = 0

    def print_stack(self):
        for item in self.semantic_stack.stack:
            print(item.class_name, item.lexeme, item.type_name)

    def push_token(self, token):
        self.semantic_stack.push(token)

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

    def run_rule(self, production_index, tokens: dict[str, Token], left_token: Token):
        match production_index:
            case 4:
                for _ in range(3):
                    self.print_to_object('\n')

            case 5:
                '''(A) Amarração de atributos, organizar a passagem de valores do atributo
                TIPO.tipo, para L.TIPO;'''

            case 6:
                '''(B) Amarração de atributos, organizar a passagem de valores do atributo.'''
            
            case 7:
                '''C) Ajustar o preenchimento de id.tipo na tabela de símbolos:
                Impressão do id no .obj'''

            case 8:
                inteiro = tokens['inteiro']
                left_token.type_name = inteiro.type_name

            case 9:
                real = tokens['real']
                left_token.type_name = real.type_name


            case 10:
                literal = tokens['literal']
                left_token.type_name = literal.type_name

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
                        print("Erro: Variável não declarada!", id_.get_formatted_line_and_column())

                # '''Verificar se o campo tipo do identificador está preenchido indicando a
                # declaração do identificador (execução da regra semântica de número 6).
                # Se sim, então:
                #     Se id.tipo = literal Imprimir ( scanf(“%s”, id.lexema); )
                #     Se id.tipo = inteiro Imprimir ( scanf(“%d”, &id.lexema); )
                #     Se id.tipo = real Imprimir ( scanf(“%lf”, &id.lexema); )
                # Caso Contrário:
                # Emitir na tela “Erro: Variável não declarada”, linha e coluna onde
                # ocorreu o erro no fonte.'''
            
            case 13:
                # Gerar código para o comando escreva no arquivo objeto.
                # Imprimir ( printf(“ARG.lexema”); )
                self.print_to_object(f'printf("{tokens["ARG"].lexeme}");\n')
            
            case 14:
                # ARG.atributos ← literal.atributos (Copiar todos os atributos de literal para os atributos de ARG).
                literal = tokens['literal']
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
                if id_.type_name == 'Nulo': # Variável não declarada
                    pass # Erro
                left_token.lexeme = id_.lexeme
                left_token.class_name = id_.class_name
                left_token.type_name = id_.type_name
                    
            
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
                id_, atr, LD = tokens['id'], tokens['atr'], tokens['LD']
                if id.type_name == 'Nulo':
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    print("Erro: Variável não declarada!", id_.get_formatted_line_and_column())
                if id_.type_name != LD.type_name:
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    print("Erro: Atribuição com tipos diferentes!", id_.get_formatted_line_and_column())
                self.print_to_object(f'{id_.lexeme} {atr.type_name} {LD.lexeme}\n')

            
            case 19:
                # Verificar se tipo dos operandos de de LD são equivalentes e diferentes de literal.
                # Se sim, então:
                #     Gerar uma variável numérica temporária Tx, em que x é um número gerado sequencialmente.
                #     LD.lexema ← Tx
                #     Imprimir (Tx = OPRD.lexema opm.tipo OPRD.lexema) no arquivo objeto.
                # Caso contrário emitir “Erro: Operandos com tipos incompatíveis” ”, linha e coluna onde ocorreu o erro no fonte.


                OPRD, OPRD_1 = tokens["OPRD"], tokens["OPRD_1"]
                if 'literal' in {OPRD.type, OPRD_1.type}:
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    print("Erro: Operação incompatível com operando(s) literal(is)!", id_.get_formatted_line_and_column())
                if OPRD.type != OPRD_1.type:
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    print("Erro: Operandos com tipos incompatíveis entre si!", id_.get_formatted_line_and_column())
                
            
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
                    print("Erro: Variável não declarada!", id_.get_formatted_line_and_column())
            
            case 22:
                # """OPRD.atributos ← num.atributos (Copiar todos os atributos de num para os atributos de OPRD)."""
                num = tokens['num']
                left_token.lexeme = num.lexeme
                left_token.class_name = num.class_name
                left_token.type_name = num.type_name
            
            case 24:
                # """Imprimir ( } ) no arquivo objeto."""
                self.print_to_object("}")
            
            case 25:
                # """Imprimir ( if (EXP_R.lexema) { ) no arquivo objeto."""
                EXP_R = tokens['EXP_R']
                self.print_to_object(f"if ({EXP_R.lexeme}) "+ "{")
            
            case 26:
                OPRD = tokens['OPRD']
                opr = tokens['opr']
                OPRD_1 = tokens['OPRD_1']

                if OPRD.type_name == OPRD_1.type_name:
                    temporary_variable = 'T' + str(self.temporary_variable_counter)
                    self.temporary_variable_counter += 1
                    left_token.lexeme = temporary_variable
                    self.print_to_object(f"{temporary_variable} = {OPRD.lexeme} {opr.type_name} {OPRD_1.lexeme}")
                else:
                    # TODO: Substituir por uma chamada a uma função mais genérica
                    # de tratamento de erros
                    print("Erro: Operandos com tipos incompatíveis!", id_.get_formatted_line_and_column())
                    
                # """
                # Verificar se os tipos de dados de OPRD são iguais ou equivalentes para a realização de comparação relacional.
                # Se sim, então:
                #     Gerar uma variável booleana temporária Tx, em que x é um número gerado sequencialmente.
                #     EXP_R.lexema ← Tx
                #     Imprimir (Tx = OPRD.lexema opr.tipo OPRD.lexema) no arquivo objeto.
                # Caso contrário emitir “Erro: Operandos com tipos incompatíveis” ”, linha e coluna onde ocorreu o erro no fonte.
                # """

            
            case 31:
                # """(D) Verificar as necessidades e gerar as regras semânticas e de tradução."""
                pass
            
            case 32:
                # """(E) Verificar as necessidades e gerar as regras semânticas e de tradução."""
                pass
            
            case 33:
                # """(F) Verificar as necessidades e gerar as regras semânticas e de tradução."""
                pass
            
            case 34:
                # """(G) Verificar as necessidades e gerar as regras semânticas e de tradução."""
                pass
            
            case 35:
                # """(H) Verificar as necessidades e gerar as regras semânticas e de tradução."""
                pass
            
            case 36:
                # """(I) Verificar as necessidades e gerar as regras semânticas e de tradução."""
                pass
            
            case 37:
                # """(J) Verificar a necessidade de atualizar o que será utilizado em EXP_R para teste no repita; verificar a necessidade de gerar outras regras semânticas e de tradução além desta."""
                pass
