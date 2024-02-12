from .models.compiler_report import CompilerReport
from .models.game import Game
from .models.player_in_tournament import PlayerInTournament
from .models.battle import Battle
from .models.tournament import Tournament

from django.contrib import admin


admin.site.register(CompilerReport)
admin.site.register(Game)
admin.site.register(Tournament)
admin.site.register(PlayerInTournament)
admin.site.register(Battle)
