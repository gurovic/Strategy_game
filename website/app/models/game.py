from django.db import models
import os


class Game(models.Model):
    name = models.CharField(max_length=50, default='')
    number_of_players = models.IntegerField(default=0, verbose_name="Number of players")
    win_point = models.IntegerField(default=0, null=True, blank=True, verbose_name='Point for winner')
    lose_point = models.IntegerField(default=0, null=True, blank=True, verbose_name='Point for loser')
    rules = models.FileField(null=True, blank=True, verbose_name='Rules')
    def __init__(self, *args, **kwargs):
        self.name = models.CharField(max_length=50, default='abcd')
        os.mkdir('../media/' + str(self))
        self.number_of_players = models.IntegerField(default=0, verbose_name="Number of players")
        self.ideal_solution = models.FileField(upload_to=str(self), null=True, verbose_name='Ideal strategy')
        self.play = models.FileField(upload_to=str(self), null=True, verbose_name='Play')
        self.win_point = models.IntegerField(default=0, null=True, blank=True, verbose_name='Point for winner')
        self.lose_point = models.IntegerField(default=0, null=True, blank=True, verbose_name='Point for loser')
        self.visualiser = models.FileField(upload_to=str(self), null=True, blank=True, verbose_name='Visualiser')
        self.rules = models.FileField(upload_to=str(self), null=True, blank=True, verbose_name='Rules')
    #folder = '../media'

    def summary(self):
        if self.name is None:
            return "start_game"
        return str(self.name)


    def __str__(self):
        try: return f"{self.name}"
        except: return "start_game"
