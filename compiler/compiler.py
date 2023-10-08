import InvokerReport
import InvokerRequest
import InvokerMultiRequest
import subprocess


class Compiler:
    def __init__(self, file_to_compile, file_name, id_of_file):
        self.file = file_to_compile
        self.ext = file_name.split(".")[-1]
        self.id = id_of_file
        self.compiled_file = ""
        self.results = []
        self.report = InvokerReport()
        self.commands = {'py': 'something',
                         'cpp': f"g++ -c {self.file} -o C:\\Users\\ddybr\\Desktop\\Compiled_files\\{self.id}"}
        self.compile()
        self.compiled_file = open(f"C:\\Users\\ddybr\\Desktop\\Compiled_files\\{self.id}")
        self.results.append(self.compiled_file)
        self.results.append(self.report)

    def do(self):
        subprocess.Popen(self.commands[self.ext])

    def compile(self):
        ireq = InvokerRequest(self.commands[self.ext], self.results, True)
        listireqs = [self.ireq]
        imr = InvokerMultiRequest(self.listireqs, "Compiler", 10)
        imr.run()

    def get_results(self):
        return self.results




a = Compiler("C:\\Users\\ddybr\\ciplusplus\\main.cpp", "main.cpp", 1)
print("f")
