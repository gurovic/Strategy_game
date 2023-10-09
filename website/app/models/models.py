from django.db import models
from django.shortcuts import get_object_or_404


class Invoker(models.Model):
    status = models.CharField(max_length=7, default="Free")
