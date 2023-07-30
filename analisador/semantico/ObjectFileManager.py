class ObjectFileManager:
    def __init__(self):
        self.temp_file = open('./programa.temp', 'w+', encoding='utf-8')
        self.temporary_variables: list[(str, str)] = []

    def __del__(self):
        if self.temp_file:
            self.temp_file.close()

    def print(self, line: str):
        self.temp_file.write(line)

    def add_temporary_variable(self, name: str, type_name: str):
        self.temporary_variables.append((name, type_name))

    def generate_final(self):
        if not self.temp_file:
            return False
        with open('./PROGRAMA.c', 'w+', encoding='utf-8') as file:
            file.write("#include <stdio.h>\n\n")
            file.write('typedef char string[256];\n\n')
            file.write("int main() {\n")
            file.write("\t/*----Variaveis temporarias----*/\n")
            for temporary_variable in self.temporary_variables:
                name, type_name = temporary_variable[0], temporary_variable[1]
                file.write(f'\t{type_name} {name};\n')
            file.write("\t/*-----------------------------*/\n")
            lines = self.temp_file.readlines()
            for line in lines:
                file.write('\t' + line)
            file.write("\treturn 0;\n")
            file.write("}")
