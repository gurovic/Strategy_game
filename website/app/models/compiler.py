from django.db import models


class CompilerReport(models.Model):

    class Status(models.IntegerChoices):
        OK = 0
        ERROR = 1

    compiled_file = models.FileField(upload_to="compiler_report", verbose_name="Файл")
    time = models.PositiveIntegerField(verbose_name="Время выполнения")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    status = models.IntegerField(choices=Status.choices, default=Status.OK, verbose_name="Статус")
    error = models.TextField(editable=False, blank=True, null=True, verbose_name="Ошибка")
    invoker_report = models.ForeignKey("app.InvokerReport", on_delete=models.CASCADE, verbose_name="Репорт инвокера")

    def __str__(self):
        return f"{self.id} - {self.get_status_display()} | {self.date_created if self.status == self.Status.OK else self.error}"

    class Meta:
        verbose_name = "Репорт компилятора"
        verbose_name_plural = "Репорты компилятора"


__all__ = ["CompilerReport"]

