from django.db import models


class Visualizer(models.Model):
    class Meta:
        verbose_name = "Визуализатор"
        verbose_name_plural = "Визуализаторы"

    source = models.FileField(upload_to="visualizer", verbose_name="Исходный код")


class Asset(models.Model):
    class Meta:
        verbose_name = "Ассет"
        verbose_name_plural = "Ассеты"

    name = models.CharField(max_length=75, verbose_name="Имя")
    file = models.FileField(upload_to="assets", verbose_name="Файл")
    visualizer = models.ForeignKey(Visualizer, on_delete=models.CASCADE, verbose_name="Визуализатор")


__all__ = ["Visualizer", "Asset"]
