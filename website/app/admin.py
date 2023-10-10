from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Tournament)
admin.site.register(Game)
admin.site.register(PlayersInBattles)
admin.site.register(PlayersInTournament)
admin.site.register(Battle)
admin.site.register(TournamentSystem)
