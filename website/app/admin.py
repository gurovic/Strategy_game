from .models import CompilerReport, Tournament, Game, PlayerInTournament

from django.contrib import admin


admin.site.register(CompilerReport)
admin.site.register(Game)
admin.site.register(Tournament)
admin.site.register(PlayerInTournament)
