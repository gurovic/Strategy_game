from django.db import models


class Invoker(models.Model):
    status = models.CharField(max_length=7, default="Free")
