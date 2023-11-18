from django.db import models

STATUS = {"NS": "Not Started", "OK": "OK", "RE": "Runtime Error", "TL": "Time Limit Exceeded"}


class InvokerReport(models.Model):
    program_type = models.ForeignKey(models.CharField, default=None, on_delete=models.CASCADE)
    invoker_id = models.ForeignKey(models.IntegerField, default=None, on_delete=models.CASCADE)
    running_file = models.ForeignKey(models.FileField, default=None, on_delete=models.CASCADE)
    time_start = models.ForeignKey(models.TimeField, default=None, on_delete=models.CASCADE)
    time_end = models.ForeignKey(models.TimeField, default=None, on_delete=models.CASCADE)
    program_status = models.ForeignKey(models.CharField, default=STATUS["NS"], on_delete=models.CASCADE)
    program_error_text = models.ForeignKey(models.CharField, default=None, on_delete=models.CASCADE)

    def notify(self, program_type, invoker_id, running_file, time_start, time_end, program_status, program_error_text):
        self.program_type = program_type
        self.invoker_id = invoker_id
        self.running_file = running_file
        self.time_start = time_start
        self.time_end = time_end
        self.program_status = program_status
        self.program_error_text = program_error_text
