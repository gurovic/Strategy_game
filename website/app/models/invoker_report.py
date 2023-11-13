from django.db import models

STATUS = {"IP": "In Progress", "F": "Finished", "NS": "Not Started"}


class ёInvokerReport(models.Model):
    time_start = models.ForeignKey(models.TimeField, default=None, on_delete=models.CASCADE)
    time_end = models.ForeignKey(models.TimeField, default=None, on_delete=models.CASCADE)
    program_status = models.ForeignKey(models.CharField, default=STATUS["NS"], on_delete=models.CASCADE)
    program_error_text = models.ForeignKey(models.CharField, default="", on_delete=models.CASCADE)

    def add_values(self, set_time_start, set_time_end, set_program_status, set_program_error_text):
        pass

    def add_single_value(self):
        pass
