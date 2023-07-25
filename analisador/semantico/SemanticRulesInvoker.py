from analisador.lexico.SymbolTable import SymbolTable
from analisador.semantico.ObjectFileManager import ObjectFileManager
from analisador.semantico.SemanticStack import SemanticStack

class SemanticRulesInvoker:

    def __init__(self, symbol_table: SymbolTable, obj_file_manager: ObjectFileManager):
        self.symbol_table = symbol_table
        self.obj_file_manager = obj_file_manager
        self.stack = SemanticStack()

    def invoke_rule(self, production_index):
        match production_index:
            case 4:
                for _ in range(0, 3):
                    self.obj_file_manager.print('')

            case 5:
                '''(A) Amarração de atributos, organizar a passagem de valores do atributo
                TIPO.tipo, para L.TIPO;'''

            case 6:
                '''(B) Amarração de atributos, organizar a passagem de valores do atributo.'''
            
            case 7:
                '''C) Ajustar o preenchimento de id.tipo na tabela de símbolos:
                Impressão do id no .obj'''

            case 8:
                '''TIPO.tipo ← inteiro.tipo
                Imprimir ( TIPO.tipo);'''

            case 9:
                '''TIPO.tipo ← real.tipo
                Imprimir ( TIPO.tipo);'''

            case 10:
                '''TIPO.tipo ← literal.tipo
                Imprimir ( TIPO.tipo);'''

            case 12:
                '''Verificar se o campo tipo do identificador está preenchido indicando a
                declaração do identificador (execução da regra semântica de número 6).
                Se sim, então:
                    Se id.tipo = literal Imprimir ( scanf(“%s”, id.lexema); )
                    Se id.tipo = inteiro Imprimir ( scanf(“%d”, &id.lexema); )
                    Se id.tipo = real Imprimir ( scanf(“%lf”, &id.lexema); )
                Caso Contrário:
                Emitir na tela “Erro: Variável não declarada”, linha e coluna onde
                ocorreu o erro no fonte.'''
            
            case 13:
                '''Gerar código para o comando escreva no arquivo objeto.
                Imprimir ( printf(“ARG.lexema”); )'''
            
            case 14:
                '''ARG.atributos ← literal.atributos (Copiar todos os atributos de literal para os
                atributos de ARG).'''

            case 15:
                """ARG.atributos ← num.atributos (Copiar todos os atributos de literal para os atributos de ARG)."""
            
            case 16:
                """Verificar se o identificador foi declarado (execução da regra semântica de número 6).
                Se sim, então:
                    ARG.atributos ← id.atributos (copia todos os atributos de id para os de ARG).
                Caso Contrário:
                    Emitir na tela “Erro: Variável não declarada” , linha e coluna onde ocorreu o erro no fonte."""
            
            case 18:
                """Verificar se id foi declarado (execução da regra semântica de número 6). Se sim, então:
                |   Realizar verificação do tipo entre os operandos id e LD (ou seja,
                |   se ambos são do mesmo tipo).
                |   Se sim, então:
                | |      Imprimir (id.lexema rcb.tipo LD.lexema) no arquivo objeto.
                | Caso contrário emitir: ”Erro: Tipos diferentes para atribuição”,
                |__________linha e coluna onde ocorreu o erro no fonte.
                Caso contrário emitir “Erro: Variável não declarada” ”, linha e coluna onde
                ocorreu o erro no fonte."""
            
            case 19:
                """Verificar se tipo dos operandos de de LD são equivalentes e diferentes de literal.
                Se sim, então:
                    Gerar uma variável numérica temporária Tx, em que x é um número gerado sequencialmente.
                    LD.lexema ← Tx
                    Imprimir (Tx = OPRD.lexema opm.tipo OPRD.lexema) no arquivo objeto.
                Caso contrário emitir “Erro: Operandos com tipos incompatíveis” ”, linha e coluna onde ocorreu o erro no fonte."""
            
            case 20:
                """LD.atributos ← OPRD.atributos (Copiar todos os atributos de OPRD para os atributos de LD)."""
            
            case 21:
                """Verificar se o identificador está declarado.
                    Se sim, então:
                        OPRD.atributos ← id.atributos
                    Caso contrário emitir “Erro: Variável não declarada” ”, linha e coluna onde ocorreu o erro no fonte."""
            
            case 22:
                """OPRD.atributos ← num.atributos (Copiar todos os atributos de num para os atributos de OPRD)."""
            
            case 24:
                """Imprimir ( } ) no arquivo objeto."""
            
            case 25:
                """Imprimir ( if (EXP_R.lexema) { ) no arquivo objeto."""
            
            case 26:
                """
                Verificar se os tipos de dados de OPRD são iguais ou equivalentes para a realização de comparação relacional.
                Se sim, então:
                    Gerar uma variável booleana temporária Tx, em que x é um número gerado sequencialmente.
                    EXP_R.lexema ← Tx
                    Imprimir (Tx = OPRD.lexema opr.tipo OPRD.lexema) no arquivo objeto.
                Caso contrário emitir “Erro: Operandos com tipos incompatíveis” ”, linha e coluna onde ocorreu o erro no fonte.
                """
            
            case 31:
                """(D) Verificar as necessidades e gerar as regras semânticas e de tradução."""
            
            case 32:
                """(E) Verificar as necessidades e gerar as regras semânticas e de tradução."""
            
            case 33:
                """(F) Verificar as necessidades e gerar as regras semânticas e de tradução."""
            
            case 34:
                """(G) Verificar as necessidades e gerar as regras semânticas e de tradução."""
            
            case 35:
                """(H) Verificar as necessidades e gerar as regras semânticas e de tradução."""    
            
            case 36:
                """(I) Verificar as necessidades e gerar as regras semânticas e de tradução."""
            
            case 37:
                """(J) Verificar a necessidade de atualizar o que será utilizado em EXP_R para teste no repita; verificar a necessidade de gerar outras regras semânticas e de tradução além desta."""
