from django.db import models


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

    def __str__(self):
        return f"{self.name}"
