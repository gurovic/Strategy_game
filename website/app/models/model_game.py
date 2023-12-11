from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=50)
    number_of_players = models.IntegerField()
    ideal_strategy = models.FileField(upload_to=name, null=True, blank=True, verbose_name='Ideal_strategy')
    play = models.FileField(upload_to=name, null=True, blank=True, verbose_name='Play')
    visualiser = models.FileField(upload_to=name, null=True, blank=True, verbose_name='Visualiser')
    rules = models.FileField(upload_to=name, null=True, blank=True, verbose_name='Rules')

