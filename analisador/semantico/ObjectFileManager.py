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
        with open('./PROGRAMA.c', 'w+', encoding='utf-8') as file:
            file.write("#include <stdio.h>\n\n")
            file.write('typedef char string[1024];\n\n')
            file.write("int main() {\n")

            file.write("\t/*----Variaveis temporarias----*/\n")
            for temporary_variable in self.temporary_variables:
                name = temporary_variable[0]
                type_name = 'int' if temporary_variable[1] == 'inteiro' else 'double'
                file.write(f'\t{type_name} {name};\n')
            file.write("\t/*-----------------------------*/\n")

            self.temp_file = open('./programa.temp', 'r', encoding='utf-8')
            lines = self.temp_file.readlines()
            indentation = 1
            for line in lines:
                # TODO: Implementar a tabulação sem esse "workaround"
                if '}' in line: indentation -= 1
                file.write('\t'*indentation + line)
                if '{' in line: indentation += 1

            file.write("\treturn 0;\n")
            file.write("}")
