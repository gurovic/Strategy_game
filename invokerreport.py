


class InvokerReport():

    def __init__(self):
        self.time_start = None
        self.time_end = None
        self.compile_status = None
        self.compile_error_text = None
        self.program_status = None
        self.program_error_text = None


    def add_values(self, time_start, time_end, compile_status, compile_error_text, program_status, program_eror_text):
        self.time_start = time_start
        self.time_end = time_end
        self.compile_status = compile_status
        self.compile_error_text = compile_error_text
        self.program_status = program_status
        self.program_error_text = program_eror_text


    def add_single_value(self, value, type):
        if (type == "time_start"):
            self.time_start = value
        if (type == "time_end"):
            self.time_end = value
        if (type == "compile_status"):
            self.compile_status = value
        if (type == "compile_error_text"):
            self.compile_error_text = value
        if (type == "program_status"):
            self.program_status = value
        if (type == "program_error_text"):
            self.program_error_text = value

