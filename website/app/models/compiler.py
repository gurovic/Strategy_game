from django.db import models


class CompilerReport(models.Model):
    class Meta:
        verbose_name = "Репорт компилятора"
        verbose_name_plural = "Репорты компилятора"

    file = models.FileField(upload_to="compiler_report", verbose_name="Файл")
    time = models.PositiveIntegerField(verbose_name="Время выполнения")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    invoker_report = models.ForeignKey("app.InvokerReport", on_delete=models.CASCADE, verbose_name="Репорт инвокера")


__all__ = ["CompilerReport"]

