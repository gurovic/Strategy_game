from django.db import models


class BattleReport(models.Model):
    invoker_report = models.ForeignKey('invoker.InvokerReport', on_delete=models.CASCADE, verbose_name='InvokerReport')
    battle_id = models.IntegerField(default=0, verbose_name='Battle id')