from django.db import models


class InvokerReport(models.Model):
    class Status(models.IntegerChoices):
        OK = 0
        RE = 1
        TL = 2

    command = models.TextField(verbose_name="Команда")

    time_start = models.DateTimeField(blank=True, verbose_name="Время начала")
    time_end = models.DateTimeField(blank=True, verbose_name="Время завершения")

    exit_code = models.IntegerField(verbose_name="Код выхода")
    log = models.TextField(blank=True, verbose_name="Лог")

    status = models.IntegerField(choices=Status.choices, default=Status.OK, verbose_name="Статус")
    error = models.TextField(editable=False, blank=True, null=True, verbose_name="Ошибка")

    def __str__(self):
        return f"\"{self.command}\" - {self.get_status_display()}"

    def has_error(self):
        return self.status != self.Status.OK

    class Meta:
        verbose_name = "Репорт инвокера"
        verbose_name_plural = "Репорты инвокера"


class File(models.Model):
    invoker_report = models.ForeignKey(InvokerReport, on_delete=models.CASCADE, verbose_name="Инвокер репорт")
    file = models.FileField(upload_to="invoker_report_files", verbose_name="Файл")

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return f"{self.file.name} | {self.invoker_report}"


__all__ = ["InvokerReport", "File"]
