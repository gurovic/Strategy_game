from .models import CompilerReport, Tournament, Game, PlayerInTournament
from .models.tournament_system_round_robin import TournamentSystemRoundRobin

from django.contrib import admin


admin.register(CompilerReport)
admin.site.register(Game)
admin.site.register(Tournament)
admin.site.register(PlayerInTournament)
admin.site.register(TournamentSystemRoundRobin)
