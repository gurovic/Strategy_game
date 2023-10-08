class Compiler:
    def __init__(self, file_to_compile, name_of_file):
        self.file = file_to_compile
        self.ext = name_of_file.split(".")[-1]
        self.commands = {'py': 'something',
                         'cpp': 'g++'}


a = Compiler("print(f)", "print.py")
print("f")