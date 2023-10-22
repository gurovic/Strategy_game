from django.db import models
from django.utils import timezone


class CompilerReport(models.Model):
    id_of_compiled_file = models.IntegerField(max_length=60)
    path_of_compiled_file = models.CharField(max_length=60)
    time = models.CharField(max_length=60)
    compile_status = models.CharField(max_length=60)
    compile_error_text = models.CharField(max_length=60)
