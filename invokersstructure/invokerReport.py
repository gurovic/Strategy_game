class InvokerReport():

    def __init__(self):
        self.time_start = None
        self.time_end = None
        self.program_status = None
        self.program_error_text = None

    def add_values(self, time_start, time_end, program_status, program_eror_text):
        self.time_start = time_start
        self.time_end = time_end
        self.program_status = program_status
        self.program_error_text = program_eror_text

    def add_single_value(self, value, type):
        if (type == "time_start"):
            self.time_start = value
        if (type == "time_end"):
            self.time_end = value
        if (type == "program_status"):
            self.program_status = value
        if (type == "program_error_text"):
            self.program_error_text = value
