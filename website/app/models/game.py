from django.db import models
import os


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "game_{0}/{1}".format(instance.name, filename)


class Game(models.Model):

    name = models.CharField(max_length=50, default='')
    number_of_players = models.IntegerField(default=0, verbose_name="Number of players")
    ideal_solution = models.FileField(upload_to=user_directory_path, null=True, verbose_name='Ideal strategy')
    play = models.FileField(upload_to=user_directory_path, null=True, verbose_name='Play')
    win_point = models.IntegerField(default=0, null=True, blank=True, verbose_name='Point for winner')
    lose_point = models.IntegerField(default=0, null=True, blank=True, verbose_name='Point for loser')
    visualiser = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name='Visualiser')
    rules = models.FileField(upload_to=user_directory_path, null=True, blank=True, verbose_name='Rules')

    def __init__(self):
        self.addway()
    def addway(self):
        os.mkdir('../media/' + str(self))
        self.ideal_solution = models.FileField(upload_to=str(self), null=True, verbose_name='Ideal strategy')
        self.play = models.FileField(upload_to=str(self), null=True, verbose_name='Play')
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
