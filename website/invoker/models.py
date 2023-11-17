from django.db import models


class File(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    file = models.FileField(upload_to="invoker_files", verbose_name="Файл")

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.name


class InvokerReport(models.Model):
    class Status(models.IntegerChoices):
        OK = 0
        RE = 1
        TL = 2

    command = models.TextField(verbose_name="Команда")

    time_start = models.DateTimeField(blank=True, verbose_name="Время начала")
    time_end = models.DateTimeField(blank=True, verbose_name="Время завершения")

    exit_code = models.IntegerField(blank=True, null=True, verbose_name="Код выхода")
    output = models.TextField(blank=True, verbose_name="Лог")

    timelimit = models.PositiveIntegerField(blank=True, null=True, verbose_name="Ограничение по времени")

    status = models.IntegerField(choices=Status.choices, default=Status.OK, verbose_name="Статус")
    error = models.TextField(editable=False, blank=True, null=True, verbose_name="Ошибка")

    input_files = models.ManyToManyField(File, blank=True, related_name="input_invoker", verbose_name="Загружённые файлы")
    preserved_files = models.ManyToManyField(File, blank=True, related_name="preserved_invoker", verbose_name="Сохранённые файлы")

    def __str__(self):
        return f"\"{self.command}\" - {self.get_status_display()}"

    def has_error(self):
        return self.status != self.Status.OK

    class Meta:
        verbose_name = "Репорт инвокера"
        verbose_name_plural = "Репорты инвокера"


__all__ = ["InvokerReport", "File"]
