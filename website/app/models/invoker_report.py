from django.db import models


class InvokerReport(models.Model):
    class Status(models.IntegerChoices):
        OK = 0
        ERROR = 1

    time = models.PositiveIntegerField(verbose_name="Время выполнения")
    status = models.IntegerField(choices=Status.choices, default=Status.OK, verbose_name="Статус")

    def __str__(self):
        if self.status == self.Status.OK:
            return f"{self.id} - {self.get_status_display()}"
        return f"{self.id} - {self.get_status_display()} | {self.error}"

    class Meta:
        verbose_name = "InvokerReport"
        verbose_name_plural = "InvokerReports"


__all__ = ["InvokerReport"]
