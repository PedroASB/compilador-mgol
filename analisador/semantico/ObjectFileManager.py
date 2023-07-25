class ObjectFileManager:
    def __init__(self):
        self.temp_file = open('./programa.temp', 'w+', encoding='utf-8')
        self.temp_vars_counter = 0

    def __del__(self):
        if self.temp_file:
            self.temp_file.close()

    def print(self, line):
        self.temp_file.writelines([line])

    def generate_final(self):
        if not self.temp_file:
            return False
        with open('./PROGRAMA.c', 'w+', encoding='utf-8') as file:
            file.write("#include <stdio.h>\n\n")
            # typedefs
            file.write("int main() {\n")
            file.write("\t/*----Variaveis temporarias----*/\n")
            # Chamar método para inserir as variáveis temporárias
            file.write("\t/*-----------------------------*/\n")
            lines = self.temp_file.readlines()
            file.write("\treturn 0;\n")
            file.write("}")
