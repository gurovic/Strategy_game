from django.db import models


class Visualizer(models.Model):
    class Meta:
        verbose_name = "Визуализатор"
        verbose_name_plural = "Визуализаторы"

    source = models.FileField(upload_to="visualizer", verbose_name="Исходный код")

