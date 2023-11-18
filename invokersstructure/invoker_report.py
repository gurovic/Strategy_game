from django.db import models

STATUS = {"NS": "Not Started", "OK": "OK", "RE": "Runtime Error", "TL": "Time Limit Exceeded"}


class InvokerReport(models.Model):
    program_type = models.CharField(default='', max_length=80)
    invoker_id = models.IntegerField(default=-1)
    running_file = models.FileField(default=None)
    time_start = models.TimeField(default=None)
    time_end = models.TimeField(default=None)
    program_status = models.CharField(default=STATUS["NS"])
    program_error_text = models.CharField(default=None)

    def notify(self, program_type, invoker_id, running_file, time_start, time_end, program_status, program_error_text):
        self.program_type = program_type
        self.invoker_id = invoker_id
        self.running_file = running_file
        self.time_start = time_start
        self.time_end = time_end
        self.program_status = program_status
        self.program_error_text = program_error_text
