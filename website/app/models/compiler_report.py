import datetime

from django.db import models
#from django_q import *


class CompilerReport(models.Model):

    class Status(models.IntegerChoices):
        OK = 0
        COMPILER_ERROR = 1
        COMPILATION_ERROR = 2
        TIMELIMIT = 3

    compiled_file = models.FileField(upload_to="compiler_report", null=True, blank=True, verbose_name="Файл")
    time = models.DurationField(default=datetime.timedelta, verbose_name="Время выполнения")
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    status = models.IntegerField(choices=Status.choices, default=Status.OK, verbose_name="Статус")
    error = models.TextField(editable=False, blank=True, null=True, verbose_name="Ошибка")
    invoker_report = models.ForeignKey("invoker.InvokerReport", null=True, blank=True, on_delete=models.CASCADE, verbose_name="Репорт инвокера")

    def __str__(self):
        if self.status == self.Status.OK:
            return f"{self.id} - {self.get_status_display()}"
        return f"{self.id} - {self.get_status_display()} | {self.error}"

    def has_error(self):
        return self.status != self.Status.OK

    class Meta:
        verbose_name = "Репорт компилятора"
        verbose_name_plural = "Репорты компилятора"


__all__ = ["CompilerReport"]

